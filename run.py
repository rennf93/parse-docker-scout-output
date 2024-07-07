import json
import os
import base64
import requests
from xhtml2pdf import pisa
from datetime import datetime


def generate_pdf_from_html(html_content, output_filename):
    with open(output_filename, "wb") as output_file:
        pisa_status = pisa.CreatePDF(html_content.encode('utf-8'), dest=output_file)
        if pisa_status.err:
            raise Exception("Error generating PDF")
    return output_filename


def generate_pdf_from_json(json_content, output_filename):
    html_content = f"<html><body><pre>{json.dumps(json_content, indent=4)}</pre></body></html>"
    with open(output_filename, "wb") as output_file:
        pisa_status = pisa.CreatePDF(html_content.encode('utf-8'), dest=output_file)
        if pisa_status.err:
            raise Exception("Error generating PDF")
    return output_filename


def upload_image_to_github(image_path, repo, token, branch, folder):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    url = f"https://api.github.com/repos/{repo}/contents/{folder}/{image_path}?ref={branch}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": f"Add {image_path}",
        "content": base64.b64encode(image_data).decode('utf-8'),
        "branch": branch
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()

    pages_url = f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/{folder}/{image_path}"
    return pages_url


def parse_recommendations(recommendations, repo, token, branch, folder):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = generate_pdf_from_html(recommendations, f'recommendations_output_{timestamp}.pdf')
    return upload_image_to_github(image_path, repo, token, branch, folder)


def parse_cves(cves_output, repo, token, branch, folder):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = generate_pdf_from_html(cves_output, f'cves_output_{timestamp}.pdf')
    return upload_image_to_github(image_path, repo, token, branch, folder)


def parse_sbom(sbom_output, repo, token, branch, folder):
    sbom_json = json.loads(sbom_output)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = generate_pdf_from_json(sbom_json, f'sbom_output_{timestamp}.pdf')
    return upload_image_to_github(image_path, repo, token, branch, folder)


def parse_image_details(image_details, repo, token, branch, folder):
    image_details_json = json.loads(image_details)
    parsed_details = []
    for image in image_details_json:
        details = {
            "Id": image.get("Id"),
            "RepoTags": image.get("RepoTags"),
            "RepoDigests": image.get("RepoDigests"),
            "Size": image.get("Size"),
            "Vulnerabilities": image.get("Config", {}).get("Labels", {}).get("vulnerabilities")
        }
        parsed_details.append(details)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = generate_pdf_from_json(parsed_details, f'image_details_{timestamp}.pdf')
    return upload_image_to_github(image_path, repo, token, branch, folder)


def main():
    recommendations = os.getenv('RECOMMENDATIONS')
    cves_output = os.getenv('CVES_OUTPUT')
    sbom_output = os.getenv('SBOM_OUTPUT')
    image_details = os.getenv('IMAGE_DETAILS')
    repo = os.getenv('TARGET_REPO')
    token = os.getenv('PAT')
    branch = os.getenv('TARGET_BRANCH')
    folder = os.getenv('TARGET_FOLDER')

    if not all([recommendations, cves_output, sbom_output, image_details, repo, token, branch, folder]):
        raise ValueError("One or more environment variables are missing")

    parsed_recommendations = parse_recommendations(recommendations, repo, token, branch, folder)
    parsed_cves = parse_cves(cves_output, repo, token, branch, folder)
    parsed_sbom = parse_sbom(sbom_output, repo, token, branch, folder)
    parsed_image_details = parse_image_details(image_details, repo, token, branch, folder)

    with open(os.getenv('GITHUB_ENV'), 'a') as env_file:
        env_file.write(f"PARSED_RECOMMENDATIONS_IMAGE={parsed_recommendations}\n")
        env_file.write(f"PARSED_CVES_IMAGE={parsed_cves}\n")
        env_file.write(f"PARSED_SBOM_IMAGE={parsed_sbom}\n")
        env_file.write(f"PARSED_IMAGE_DETAILS={parsed_image_details}\n")


if __name__ == "__main__":
    main()