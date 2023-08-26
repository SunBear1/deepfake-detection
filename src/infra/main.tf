resource "azurerm_resource_group" "main-rg" {
  location = var.resource_group_properties.location
  name     = var.resource_group_properties.name
  tags = var.default_tags
}

resource "azurerm_storage_account" "main-sa" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.main-rg.name
  location                 = var.resource_group_properties.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind = "StorageV2"
  access_tier = "Hot"
  enable_https_traffic_only = true
  min_tls_version = "TLS1_2"
  is_hns_enabled = true
  large_file_share_enabled = false
  allow_blob_public_access = true
  nfsv3_enabled = false
  tags = var.default_tags
  blob_properties {
    delete_retention_policy {
      days = 3
    }
    container_delete_retention_policy {
      days = 3
    }
  }
}

resource "azurerm_storage_container" "output-storage-container" {
  name                  = var.output_container_name
  storage_account_name  = azurerm_storage_account.main-sa.name
  container_access_type = "container"
  metadata = var.default_tags
}

resource "azurerm_storage_container" "input-storage-container" {
  name                  = var.input_container_name
  storage_account_name  = azurerm_storage_account.main-sa.name
  container_access_type = "container"
  metadata = var.default_tags
}

