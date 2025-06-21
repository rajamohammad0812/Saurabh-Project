param($name)

$keyVaultRg = $env:KEYVAULT_RG
$keyVaultLocation = $env:KEYVAULT_LOCATION

az keyvault create --name $name --resource-group $keyVaultRg --location $keyVaultLocation | ConvertFrom-Json