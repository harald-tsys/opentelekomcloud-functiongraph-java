import os
import requests
import json

# Define the necessary variables
# see: https://docs.github.com/en/rest/packages/packages?apiVersion=2022-11-28#list-package-versions-for-a-package-owned-by-a-user
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
USER = os.environ.get("USER")
PACKAGE_TYPE = os.environ.get("PACKAGE_TYPE", "maven")
PACKAGE_NAME = os.environ.get("PACKAGE_NAME")
PACKAGE_VERSION_NAME = os.environ.get("PACKAGE_VERSION")
OUTPUT_NAME=os.environ.get("OUTPUT_NAME","PACKAGE_EXISTS")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

url = f"https://api.github.com/users/{USER}/packages/{PACKAGE_TYPE}/{PACKAGE_NAME}/versions"

# Make the GET request to the API
response = requests.get(url, headers=HEADERS)

print(response)
print(response.text)

exists = "false"

# Check if the request was successful
if response.status_code == 200:
    packages = json.loads(response.text)

    for package in packages:
        if package["name"] == PACKAGE_VERSION_NAME:
            exists = "true"
            break
else:
    print(f"response {response.text}")

with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"{OUTPUT_NAME}={exists}\n")
