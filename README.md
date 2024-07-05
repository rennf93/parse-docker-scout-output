# parse-docker-scout-output

`parse-docker-scout-output` is a GitHub Action designed to parse the output from Docker Scout. It processes Docker Scout's recommendations, CVEs, and SBOM outputs, and uploads the results as images to your GitHub repository. This action is ideal for enhancing the visibility of Docker image security within your projects.

## Features

- Parses Docker Scout recommendations, CVEs, and SBOM outputs
- Uploads the results as images to your GitHub repository
- Sets environment variables with the URLs of these images

## Outputs

This action does not produce direct outputs but uploads images to the repository and sets environment variables with the URLs of these images.

## Usage

To use this action in your workflow, add the following step:

```yaml
- name: Parse Docker Scout Output
  uses: rennf93/parse-docker-scout-output@v1
  with:
    GITHUB_REPOSITORY: ${{ secrets.GITHUB_REPOSITORY }}
    GITHUB_REF_NAME: ${{ secrets.GITHUB_REF_NAME }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    REPO_FOLDER: ${{ secrets.REPO_FOLDER }}
    RECOMMENDATIONS: ${{ steps.docker-scout.outputs.recommendations }}
    CVES_OUTPUT: ${{ steps.docker-scout.outputs.cves }}
    SBOM_OUTPUT: ${{ steps.docker-scout.outputs.sbom }}
    IMAGE_DETAILS: ${{ steps.docker-scout.outputs.image_details }}
```

## Inputs

| Input Name         | Description                              | Required |
|--------------------|------------------------------------------|----------|
| `GITHUB_REPOSITORY`| Target GitHub Repo to upload images to   | true     |
| `GITHUB_REF_NAME`  | Target Repo's Branch to upload images to | true     |
| `GITHUB_TOKEN`     | GitHub token for authentication          | true     |
| `REPO_FOLDER`      | Folder in the repository to upload images to | true     |
| `RECOMMENDATIONS`  | Docker Scout recommendations HTML output | true     |
| `CVES_OUTPUT`      | Docker Scout CVEs HTML output            | false    |
| `SBOM_OUTPUT`      | Docker Scout SBOM HTML output            | false    |
| `IMAGE_DETAILS`    | Docker image details JSON                | false    |

## Example Workflow

Here is an example of how to integrate this action into a GitHub workflow:

```yaml
name: Example Workflow

on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Docker Scout Analysis
        id: docker-scout
        uses: docker/scout-action@v1.9.3
        with:
          command: cves,recommendations,compare
          image: <image-name>:<image-tag>

      - name: Parse Docker Scout Output
        uses: rennf93/parse-docker-scout-output@v1.0
        with:
          GITHUB_REPOSITORY: ${{ secrets.GITHUB_REPOSITORY }}
          GITHUB_REF_NAME: ${{ secrets.GITHUB_REF_NAME }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPO_FOLDER: ${{ secrets.REPO_FOLDER }}
          RECOMMENDATIONS: ${{ steps.docker-scout.outputs.recommendations }}
          CVES_OUTPUT: ${{ steps.docker-scout.outputs.cves }}
          SBOM_OUTPUT: ${{ steps.docker-scout.outputs.sbom }}
          IMAGE_DETAILS: ${{ steps.docker-scout.outputs.image_details }}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.