import click
import requests
import json
import os
from azure.identity import ClientSecretCredential

# ─── Azure App Registration Info ───────────────────────────────────────────────
TENANT_ID     = os.getenv("AZURE_TENANT_ID")
CLIENT_ID     = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

# ─── Logic App HTTP Triggers ───────────────────────────────────────────────────
LOGICAPP_CREATE_URL = "https://<your_logicapp_region>.logic.azure.com:443/workflows/<logicapp_name>/triggers/manual/paths/invoke?...sig=..."
LOGICAPP_ADD_URL    = "https://<your_logicapp_region>.logic.azure.com:443/workflows/<logicapp_name>/triggers/manual/paths/invoke?...sig=..."

def get_token():
    """Get Azure access token using service principal credentials."""
    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    token = credential.get_token("https://management.azure.com/.default")
    return token.token

@click.group()
def maas():
    """Maas CLI — handle Azure command."""
    pass

@maas.group()
def azure():
    """Azure command subgroup."""
    pass

@azure.command("create")
@click.option('--app_name',    required=True)
@click.option('--subscription_id',  required=True)
@click.option('--owner',       required=True)
@click.option('--env',         required=True)
@click.option('--storage_account', default=None)
@click.option('--aks_cluster',     default=None)
@click.option('--mysql_instance', default=None)
def create(app_name, subscription_id, owner, env, storage_account, aks_cluster, mysql_instance):
    """Trigger the Create Logic App."""
    payload = {
        "Application_Name":    app_name,
        "SubscriptionId":      subscription_id,
        "Owner_of_Repository": owner,
        "env":                 env
    }
    if storage_account: payload["storage_account"] = storage_account
    if aks_cluster:     payload["aks_cluster"] = aks_cluster
    if mysql_instance:  payload["mysql_instance"] = mysql_instance

    try:
        headers = {"Content-Type": "application/json"}
        resp = requests.post(LOGICAPP_CREATE_URL, headers=headers, json=payload)
        resp.raise_for_status()
        click.echo("Logic App 'create' triggered successfully!")
        click.echo(f"  Response: {resp.text}")
    except Exception as e:
        click.echo("[ERROR] " + str(e))

@azure.command("add")
@click.option('--subscription_id',  required=True)
@click.option('--app_name',         required=True)
@click.option('--env',              required=True)
@click.option('--aks_cluster',      default=None)
@click.option('--storage_account',  default=None)
@click.option('--mysql_instance',   default=None)
@click.option('--branch',           default=None)
def add(subscription_id, app_name, env, aks_cluster, storage_account, mysql_instance, branch):
    """Trigger the Add Logic App."""
    payload = {
        "SubscriptionId":     subscription_id,
        "Application_Name":   app_name,
        "env":                env
    }
    if aks_cluster:     payload["aks_cluster"] = aks_cluster
    if storage_account: payload["storage_account"] = storage_account
    if mysql_instance:  payload["mysql_instance"] = mysql_instance
    if branch:          payload["branch"] = branch

    try:
        headers = {"Content-Type": "application/json"}
        resp = requests.post(LOGICAPP_ADD_URL, headers=headers, json=payload)
        resp.raise_for_status()
        click.echo("Logic App 'add' triggered successfully!")
        click.echo(f"  Response: {resp.text}")
    except Exception as e:
        click.echo("[ERROR] " + str(e))

if __name__ == "__main__":
    maas()