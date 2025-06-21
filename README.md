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
# ├── functions/
# │   ├── CreateResourcesOrchestrator/
# │   │   ├── function.json
# │   │   └── run.ps1
# │   ├── CreateGithubRepoActivity/
# │   │   ├── function.json
# │   │   └── run.ps1
# │   ├── CreateKeyVaultActivity/
# │   │   ├── function.json
# │   │   └── run.ps1
# ├── infra/
# │   ├── main.tf
# │   ├── variables.tf
# │   ├── outputs.tf
# │   ├── provider.tf
# │   ├── appservice.tf
# │   ├── durable_function.tf
# │   ├── keyvault.tf
# │   ├── identity.tf
# ├── .github/
# │   └── workflows/
# │       └── deploy.yml
# ├── README.md

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

---

## ✅ Success
You will see:
- A new GitHub repo under your account.
- A new Key Vault in your Azure resource group.

---

## 🧠 Notes
- Durable Functions orchestrator and activity functions are implemented in PowerShell (`run.ps1` files).
- Adjust region, names, and any other variables in `infra/variables.tf`.

