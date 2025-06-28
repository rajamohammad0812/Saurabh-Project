import click
import boto3
import json
import datetime
 
# ─── Move Nothing to See here ==> You Can't See Me ─────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = "***"
AWS_SECRET_ACCESS_KEY = "****"
ROLE_TO_ASSUME    = "arn:aws:iam::***:role/MAASRole"
REGION                = "me-central-1"
 
# ─── StepFunctionn ARN ────────────────────────────
CREATE_STATE_MACHINE_ARN = "arn:aws:states:me-central-1:***:stateMachine:MAAS-EKS"
ADD_STATE_MACHINE_ARN    = "arn:aws:states:me-central-1:***:stateMachine:MAAS-ADD"
# ─────────────────────────────────────────────────────────────────────────────

def _get_sfn_client():
    """AssumeRole via STS et renvoie un client StepFunctions."""
    sts = boto3.client(
        "sts",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION
    )
    session_name = f"maas-cli-{int(datetime.datetime.utcnow().timestamp())}"
    resp = sts.assume_role(
        RoleArn=ROLE_TO_ASSUME,
        RoleSessionName=session_name
    )
    creds = resp["Credentials"]
    return boto3.client(
        "stepfunctions",
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=REGION
    )
 
@click.group()
def maas():
    """Maas CLI — handle AWS command."""
    pass
 
@maas.group()
def aws():
    """AWS command subgroup."""
    pass
 
@aws.command("create")
@click.option('--app_name',    required=True, help="Application Name")
@click.option('--account_id',  required=True, help="AWS Account Id")
@click.option('--owner',       required=True, help="Owner Repository")
@click.option('--env',         required=True, help="Environnement (dev,prod)")
@click.option('--s3_name',     default=None,  help="(opt) S3 bucket name")
@click.option('--cluster_name',default=None,  help="(opt) EKS Cluster Name")
@click.option('--rdsmysql_name',default=None, help="(opt) RDS Mysql Instance Name")

def create(app_name, account_id, owner, env, s3_name, cluster_name, rdsmysql_name):
    """Trigger the Create Step Function."""
    payload = {
        "Application_Name":    app_name,
        "AccountId":           account_id,
        "Owner_of_Repository": owner,
        "env":                 env
    }
    if s3_name:      payload["s3_name"]      = s3_name
    if cluster_name: payload["cluster_name"] = cluster_name
    if rdsmysql_name: payload["rdsmysql_name"] = rdsmysql_name

 
    try:
        client = _get_sfn_client()
        resp = client.start_execution(
            stateMachineArn=CREATE_STATE_MACHINE_ARN,
            input=json.dumps(payload)
        )
        click.echo("Step Function 'create' démarrée !")
        click.echo(f"  Execution ARN : {resp['executionArn']}")
        click.echo(f"  Début         : {resp['startDate']}")
    except Exception as e:
        click.echo("[ERROR] " + str(e))
 
@aws.command("add")
@click.option('--account_id',          required=True, help="AWS Account Id")
@click.option('--app_name',            required=True, help="Application Name")
@click.option('--env',                 required=True, help="Environnement (dev,prod)")
@click.option('--cluster_name',        default=None,  help="(opt) EKS Cluster Name")
@click.option('--s3_name',             default=None,  help="(opt) S3 bucket name")
@click.option('--rdsmysql_name',       default=None,  help="(opt) RDS Mysql Instance name")
@click.option('--branch',              default=None,  help="(opt) Dedicated branch Name")
def add(account_id, app_name, env, cluster_name, s3_name, rdsmysql_name,branch):
    """"Trigger the Add Step Function."""
    payload = {
        "AccountId":         account_id,
        "Application_Name":  app_name,
        "env":               env
    }
    if cluster_name:   payload["cluster_name"]  = cluster_name
    if s3_name:        payload["s3_name"]       = s3_name
    if rdsmysql_name:  payload["rdsmysql_name"] = rdsmysql_name
    if branch:         payload["branch"]        = branch
 
    try:
        client = _get_sfn_client()
        resp = client.start_execution(
            stateMachineArn=ADD_STATE_MACHINE_ARN,
            input=json.dumps(payload)
        )
        click.echo("Step Function 'add' démarrée !")
        click.echo(f"  Execution ARN : {resp['executionArn']}")
        click.echo(f"  Début         : {resp['startDate']}")
    except Exception as e:
        click.echo("[ERROR] " + str(e))
 
if __name__ == "__main__":
    maas()
