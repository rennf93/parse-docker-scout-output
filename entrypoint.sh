#!/bin/sh -l

# Extract inputs from 'with' GitHub context using the INPUT_ prefix
export GITHUB_TOKEN="${GITHUB_TOKEN}"
export GITHUB_REPOSITORY="${GITHUB_REPOSITORY}"
export GITHUB_REF_NAME="${GITHUB_REF_NAME}"
export REPO_FOLDER="${REPO_FOLDER}"
export RECOMMENDATIONS="${INPUT_RECOMMENDATIONS}"
export CVES_OUTPUT="${INPUT_CVES_OUTPUT}"
export SBOM_OUTPUT="${INPUT_SBOM_OUTPUT}"
export IMAGE_DETAILS="${INPUT_IMAGE_DETAILS}"

# Check if required inputs are provided
if [ -z "$GITHUB_REPOSITORY" ]; then
  echo "GITHUB_REPOSITORY is a required input and must be set."
  exit 1
fi

if [ -z "$GITHUB_REF_NAME" ]; then
  echo "GITHUB_REF_NAME is a required input and must be set."
  exit 1
fi

if [ -z "$RECOMMENDATIONS" ]; then
  echo "RECOMMENDATIONS is a required input and must be set."
  exit 1
fi

if [ -z "$FOLDER_NAME" ]; then
  echo "FOLDER_NAME is a required input and must be set."
  exit 1
fi

# Run the Python script with the provided inputs
python /usr/src/app/run.py