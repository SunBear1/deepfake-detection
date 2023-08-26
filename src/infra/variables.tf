variable "resource_group_properties" {
  type = object({
    name     = string
    location = string
  })
  default = {
    name     = "ProjektBadawczyRG"
    location = "eastus2"
  }
}

variable "storage_account_name" {
    type = string
    default = "projektbadawczystorage"
}

variable "output_container_name" {
    type = string
    default = "deepfake-audio-dataset"
}

variable "input_container_name" {
    type = string
    default = "raw-audio-dataset"
}

variable "default_tags" {
  type       = map(string)
  default    = {
    "project" = "projekt badawczy"
    "managed_by" = "terraform"
  }
}
