IMAGE_TAG := test
RESOURCE_GROUP := ProjektBadawczyRG
STORAGE_ACCOUNT := projektbadawczystorage


.PHONY: build

build:
	echo "Getting access key for ${STORAGE_ACCOUNT} in ${RESOURCE_GROUP}..."
	az storage account keys list --resource-group $(RESOURCE_GROUP) --account-name $(STORAGE_ACCOUNT) --query '[0].value' --output tsv
	echo ${ACCESS_KEY}

