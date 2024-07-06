#!/bin/sh -l

# Extract inputs from 'with' GitHub context using the INPUT_ prefix
export TARGET_REPO="${TARGET_REPO}"
export TARGET_BRANCH="${TARGET_BRANCH}"
export TARGET_FOLDER="${TARGET_FOLDER}"
export RECOMMENDATIONS="${INPUT_RECOMMENDATIONS}"
export CVES_OUTPUT="${INPUT_CVES_OUTPUT}"
export SBOM_OUTPUT="${INPUT_SBOM_OUTPUT}"
export IMAGE_DETAILS="${INPUT_IMAGE_DETAILS}"

# Check if required inputs are provided
if [ -z "$TARGET_REPO" ]; then
  echo "TARGET_REPO is a required input and must be set."
  exit 1
fi

if [ -z "$TARGET_BRANCH" ]; then
  echo "TARGET_BRANCH is a required input and must be set."
  exit 1
fi

if [ -z "$TARGET_FOLDER" ]; then
  echo "TARGET_FOLDER is a required input and must be set."
  exit 1
fi

if [ -z "$RECOMMENDATIONS" ]; then
  echo "RECOMMENDATIONS is a required input and must be set."
  exit 1
fi

if [ -z "$CVES_OUTPUT" ]; then
  echo "CVES_OUTPUT is a required input and must be set."
  exit 1
fi

if [ -z "$SBOM_OUTPUT" ]; then
  echo "SBOM_OUTPUT is a required input and must be set."
  exit 1
fi

if [ -z "$IMAGE_DETAILS" ]; then
  echo "IMAGE_DETAILS is a required input and must be set."
  exit 1
fi

# Run the Python script with the provided inputs
python /usr/src/app/run.py