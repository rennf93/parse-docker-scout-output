import unittest
import json
import os
from unittest.mock import patch, mock_open
from run import generate_image_from_html, upload_image_to_github, parse_recommendations, parse_cves, parse_sbom, parse_image_details

class TestRunFunctions(unittest.TestCase):

    def tearDown(self):
        # Clean up any files created during the tests
        test_files = [
            "test_output.png",
            "recommendations_output.png",
            "cves_output.png",
            "sbom_output.png"
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    @patch('imgkit.from_string')
    def test_generate_image_from_html(self, mock_from_string):
        html_content = "<h2>Test HTML</h2>"
        output_filename = "test_output.png"
        result = generate_image_from_html(html_content, output_filename)
        mock_from_string.assert_called_once_with(html_content, output_filename)
        self.assertEqual(result, output_filename)

    @patch('run.requests.put')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test_image_data')
    def test_upload_image_to_github(self, mock_file, mock_put):
        mock_put.return_value.status_code = 201
        mock_put.return_value.json.return_value = {
            'content': {'download_url': 'https://example.com/test_output.png'}
        }
        image_path = "test_output.png"
        repo = "rennf93/project-assets"
        token = "test_token"
        branch = "master"
        folder = "tests"
        result = upload_image_to_github(image_path, repo, token, branch, folder)
        self.assertEqual(result, f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/{folder}/{image_path}")

    @patch('run.upload_image_to_github')
    def test_parse_recommendations(self, mock_upload):
        mock_upload.return_value = "https://example.com/recommendations_output.png"
        recommendations = "<h2>Recommendations</h2>"
        repo = "rennf93/project-assets"
        token = "test_token"
        branch = "master"
        folder = "tests"
        result = parse_recommendations(recommendations, repo, token, branch, folder)
        self.assertEqual(result, "https://example.com/recommendations_output.png")

    @patch('run.upload_image_to_github')
    def test_parse_cves(self, mock_upload):
        mock_upload.return_value = "https://example.com/cves_output.png"
        cves_output = "<h2>CVEs</h2>"
        repo = "rennf93/project-assets"
        token = "test_token"
        branch = "master"
        folder = "tests"
        result = parse_cves(cves_output, repo, token, branch, folder)
        self.assertEqual(result, "https://example.com/cves_output.png")

    @patch('run.upload_image_to_github')
    def test_parse_sbom(self, mock_upload):
        mock_upload.return_value = "https://example.com/sbom_output.png"
        sbom_output = "<h2>SBOM</h2>"
        repo = "rennf93/project-assets"
        token = "test_token"
        branch = "master"
        folder = "tests"
        result = parse_sbom(sbom_output, repo, token, branch, folder)
        self.assertEqual(result, "https://example.com/sbom_output.png")

    def test_parse_image_details(self):
        image_details = json.dumps([{
            "Id": "123",
            "RepoTags": ["test_repo:latest"],
            "RepoDigests": ["sha256:abc123"],
            "Size": 123456,
            "Config": {
                "Labels": {
                    "vulnerabilities": "5"
                }
            }
        }])
        result = parse_image_details(image_details)
        expected = [{
            "Id": "123",
            "RepoTags": ["test_repo:latest"],
            "RepoDigests": ["sha256:abc123"],
            "Size": 123456,
            "Vulnerabilities": "5"
        }]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()