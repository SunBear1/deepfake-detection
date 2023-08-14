IMAGE_TAG := malajski/dataset-director:latest
CONTAINER_NAME := dataset-director
RESOURCE_GROUP := ProjektBadawczyRG
STORAGE_ACCOUNT := projektbadawczystorage
# AZURE_STORAGE_ACCOUNT := $(shell az storage account keys list --resource-group $(RESOURCE_GROUP) --account-name $(STORAGE_ACCOUNT) --query '[0].value' --output tsv)

.PHONY: build

run:
	@docker run --name dataset-director -p 80:8000 \
	--env AZURE_STORAGE_KEY=${ACCESS_KEY} \
	--env AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT} \
	--env AZURE_RESOURCE_GROUP=${RESOURCE_GROUP} \
	${IMAGE_TAG}
