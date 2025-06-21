resource "azurerm_storage_account" "storage" {
  name                     = "${replace(var.function_name, "-", "")}stg"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "plan" {
  name                = "${var.function_name}-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "durable_function" {
  name                       = var.function_name
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  app_service_plan_id        = azurerm_app_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  version                    = "~4"
  app_settings = {
    GITHUB_TOKEN     = var.github_token
    KEYVAULT_RG      = azurerm_resource_group.rg.name
    KEYVAULT_LOCATION= var.location
  }
}