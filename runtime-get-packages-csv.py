#!/usr/bin/env python

import requests
import argparse
import json
import csv
import time

class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request

class ImageResult:
   def __init__(self, image, packages):
    self.image = image
    self.packages = packages

def generate_csv(images, packageName):
    if packageName == "":
        fileName = "all-runtime-image-packages.csv"
    else:
        fileName = f'{packageName}-runtime-image-packages.csv'
    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        packageReport = []
        packageReport.append(["image", "package", "packageVersion", "kubernetes_cluster_name", "kubernetes_namespace", "kubernetes_workload_name"])
        for imageObj in images:
           for package in imageObj.packages:
               packageReport.append([imageObj.image['recordDetails']['mainAssetName'], \
                   package['name'], \
                   package['version'], \
                   imageObj.image['recordDetails']['labels']['kubernetes.cluster.name'], \
                   imageObj.image['recordDetails']['labels']['kubernetes.namespace.name'], \
                   imageObj.image['recordDetails']['labels']['kubernetes.workload.name']]
               )
        writer.writerows(packageReport)
    return


def get_running_images(uri, auth, headers):
    imageReturn = []
    params = {
        "filter": 'asset.type = "workload"',
        "cursor": ""
    }
    cursor = ""
    iterate = True
    while iterate:
        queryResults = json.loads(requests.get(f'{uri}/api/scanning/runtime/v2/workflows/results', auth=auth, headers=headers, params=params).content)
        if queryResults['page']['next'] != None:
            cursor = queryResults['page']['next']
            queryResults = json.loads(requests.get(f'{uri}/api/scanning/runtime/v2/workflows/results', auth=auth, headers=headers, params=params).content)
            imageReturn.extend(queryResults['data'])
            params.update({"cursor": cursor})
        else:
            imageReturn.extend(queryResults['data'])
            iterate=False
    return imageReturn

def get_package(uri, auth, headers, packageName, resultId):
    offset = 0
    if packageName != "":
        params = {
             "filter": f'freeText in ("{packageName}")',
             "limit": "100",
             "offset": f'{offset}'
        }
    else:
        params = {
            "limit": "100",
            "offset": f'{offset}'
        }
    iterate = True
    packageReturn = []
    print(f'Processing: {resultId}')
    while iterate:
        imageResult = json.loads(requests.get(f'{uri}/api/scanning/scanresults/v2/results/{resultId}/packages', auth=auth, headers=headers, params=params).content)
        if "message" in imageResult:
            print(imageResult)
            print("Sleeping to handle rate limiting for 15s")
            time.sleep(30)
        else:
            if imageResult['page']['offset'] <= imageResult['page']['matched']:
                if "data" not in imageResult:
                    print(imageResult)
                packageReturn.extend(imageResult['data'])
                offset+=100
                params.update({"offset": f'{offset}'})
            elif imageResult['page']['offset'] >= imageResult['page']['matched']:
                iterate=False
    return packageReturn

def main():
    parser = argparse.ArgumentParser(description="Query runtime images for a package")
    parser.add_argument("--sysdig_uri", metavar='U', type=str, help="Sysdig Secure URI", required=True)
    parser.add_argument("--sysdig_token", metavar="T", type=str, help="Sysdig Secure Token to authenticate against the URI", required=True)
    parser.add_argument("--package", metavar="V", type=str, help="Package name to search.", required=False, default="")
    args = parser.parse_args()

    sysdig_token = args.sysdig_token
    sysdig_url = args.sysdig_uri
    package = args.package
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br"
    }
    auth = TokenAuth(sysdig_token)
    runningImages = get_running_images(uri=sysdig_url, auth=auth, headers=headers)
    imageResults = []
    for image in runningImages:
        packages = get_package(uri=sysdig_url, auth=auth, headers=headers, packageName=package, resultId=image['resultId'])
        imageResults.append(ImageResult(image, packages))
    print(f'Generating CSV for package query: {package}')
    generate_csv(imageResults, package)
    return
if __name__ == '__main__':
    main()