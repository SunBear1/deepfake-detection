variable "resource_group_properties" {
  type = object({
    name     = string
    location = string
  })
  default = {
    name     = "ProjektBadawczyPlaygroundRG"
    location = "eastus2"
  }
}

variable "storage_account_name" {
    type = string
    default = "projektbadawczy"
}

variable "storage_container_name" {
    type = string
    default = "deepfake-dataset"
}

variable "default_tags" {
  type       = map(string)
  default    = {
    "project" = "projekt badawczy"
    "managed_by" = "terraform"
  }
}
