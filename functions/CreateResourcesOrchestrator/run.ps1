param($Context)

$repoName = "my-new-repo"
$keyVaultName = "my-keyvault-$(Get-Random)"

$repoResult = Invoke-DurableActivity -FunctionName "CreateGithubRepoActivity" -Input $repoName
$keyVaultResult = Invoke-DurableActivity -FunctionName "CreateKeyVaultActivity" -Input $keyVaultName

return @{ 
  githubRepo = $repoResult
  keyVault = $keyVaultResult
}