param($name)

$token = $env:GITHUB_TOKEN
$body = @{ name = $name } | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
  -Method POST `
  -Headers @{ Authorization = "token $token"; "User-Agent" = "AzureFunction" } `
  -Body $body