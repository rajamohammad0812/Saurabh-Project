# Durable Functions with GitHub Repo and Key Vault Creation

This repository contains:
- Azure Durable Functions in PowerShell that:
  - Creates a GitHub repository.
  - Creates an Azure Key Vault.
- Infrastructure-as-Code (Terraform) to deploy the function app.
- GitHub Actions workflow to trigger the deployment.

---

## 📂 Structure

```
functions/             # Durable Functions (Orchestrator + Activities)
infra/                 # Terraform config for Function App
.github/workflows/     # GitHub Actions workflow
README.md
```
---

## 🔑 Prerequisites
- Azure account & subscription
- GitHub account with personal access token (PAT) for repo creation
- Set the following **repository secrets**:
  - `GH_TOKEN`: GitHub Personal Access Token with `repo` scope
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`

---

## 🚀 Deployment Steps
1. Commit and push your code.
2. Go to GitHub Actions tab.
3. Run the `Deploy Durable Functions Infra` workflow manually.
4. The workflow will:
   - Deploy the Azure Durable Function App.
   - Durable function will create GitHub repo and Key Vault at runtime.

---

## 🧪 Test the Orchestrator
Trigger the Durable Functions orchestrator using the Azure Functions HTTP endpoint or Azure portal.

Use curl or Postman to send a POST request to the durable function:

``` curl -X POST https://<your-function-app>.azurewebsites.net/api/orchestrators/CreateRepoAndKeyVaultOrchestrator ```

If your durable orchestrator expects a payload like repo and key vault names, send a JSON payload too:

```
curl -X POST https://<your-function-app>.azurewebsites.net/api/orchestrators/CreateRepoAndKeyVaultOrchestrator \
    -H "Content-Type: application/json" \
    -d '{"repo_name":"my-new-repo","keyvault_name":"myNewKeyvault"}'
```

## Check the status of the Orchestration

The POST request will give you back:
	•	a statusQueryGetUri
	•	a sendEventPostUri

Copy the statusQueryGetUri and hit it in a browser or with curl:

```
curl https://<your-function-app>.azurewebsites.net/runtime/webhooks/durabletask/instances/<your-instance-id>?code=<your-function-key>

```
This will show:
	•	"runtimeStatus": "Completed" once all tasks have run successfully.
	•	output will contain any output data.
 
✅ Verify Resources

After the status says Completed:
	1.	Go to your GitHub account — verify that the new repository was created.
	2.	Go to your Azure Portal — verify that the Key Vault resource exists.

If everything is present ✅ then your setup worked!


---

## ✅ Success
You will see:
- A new GitHub repo under your account.
- A new Key Vault in your Azure resource group.

---

## 🧠 Notes
- Durable Functions orchestrator and activity functions are implemented in PowerShell (`run.ps1` files).
- Adjust region, names, and any other variables in `infra/variables.tf`.

