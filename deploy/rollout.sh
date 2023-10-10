#!/bin/bash

export AZURE_STORAGE_KEY="change-me"
export AZURE_STORAGE_ACCOUNT="projektbadawczystorage"
export API_KEY="change-me"


if [ $# -eq 0 ]; then
  echo "Usage: $0 <image_tag>"
  exit 1
fi

IMAGE_TAG="$1"
IMAGE_NAME="malajski/dataset-director:${IMAGE_TAG}"

CONTAINER_NAME="dataset-director"

if [[ "$(docker ps -q -f name=${CONTAINER_NAME})" ]]; then
  echo "Stopping the existing container..."
  docker stop ${CONTAINER_NAME}
fi

sleep 1 # I know that is not the best solution, but it works XD. Bash too fast
echo "Removing old image..."
docker rmi "${IMAGE_NAME}"

echo "Pulling the Docker image: ${IMAGE_NAME}"
docker pull "${IMAGE_NAME}"

echo "Starting the updated container..."
sudo docker run --rm --name ${CONTAINER_NAME} -d -p 80:8000 --env API_KEY=${API_KEY} --env AZURE_STORAGE_KEY=${AZURE_STORAGE_KEY} --env AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT} "${IMAGE_NAME}"
