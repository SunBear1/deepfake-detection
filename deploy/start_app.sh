#!/bin/bash

export AZURE_STORAGE_KEY="change-me"
export AZURE_STORAGE_ACCOUNT="projektbadawczystorage"
export API_KEY="change-me"
sudo docker run --rm --name dataset-director -p 80:8000 --env API_KEY=${API_KEY} --env AZURE_STORAGE_KEY=${AZURE_STORAGE_KEY} --env AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT} malajski/dataset-director:latest
