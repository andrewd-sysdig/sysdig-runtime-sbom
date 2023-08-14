# Getting Runtime SBOMs from Vulnerability Management #

## Purpose ##

Search all runtime images for a specific package by name or export all packages/versions across runtime
infrastructure (workloads only as of 3/22/2023). Feature of Inventory will 
deprecate this script once they support searching by package.


### Usage ###

To utilize this script it is recommended to operate within a Python Virtual Environment. Included in the package
is a `pipenv` definition. To set up `pipenv` visit https://pipenv.pypa.io/en/latest/.

Running the script takes 3 inputs all available via the included `--help` function.

```
usage: runtime-get-packages-csv.py [-h] --sysdig_uri U --sysdig_token T [--package V]

Query runtime images for a package

optional arguments:
  -h, --help        show this help message and exit
  --sysdig_uri U    Sysdig Secure URI
  --sysdig_token T  Sysdig Secure Token to authenticate against the URI
  --package V       Package name to search.
```

When running the script it will parse all runtime packages across your infrastructure workloads and generate a CSV 
report similar to the following titled with `<packageName>-runtime-image-packages.csv`

```shell
./runtime-get-packages-csv.py --sysdig_uri https://us2.app.sysdig.com --sysdig_token <token> --package python   
Processing: 174ea49dd913aa2fc179c53c452592e2
Processing: 174ea49dd913aa2f0dcf7e9536b2ca12
Processing: 174ea49dd913aa2fec8dc9e1208c0282
Processing: 174ea49dd913aa2f9f882996e2c24e92
Processing: 174ea49dd913aa2ff516c64dbc37f112
Processing: 174ea444d3e2e916d747437d0408a682
Processing: 174ea49dd913aa2f6b74d6437103dcc2
Processing: 174ea49dd913aa2f45aca4c3edb1d182
Processing: 174ea49dd913aa2f2ba6782cda5105b2
Processing: 174ea49dd913aa2f6e4df73371a3a922
Processing: 174ea49dd913aa2fe97a24c3a2e410e2
Processing: 174ea49dd913aa2f66aa989f9e59ef12
Generating CSV for package query: python
```

```csv
image,package,packageVersion,kubernetes_cluster_name,kubernetes_namespace,kubernetes_workload_name
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python,2.7.18,sysdig-dev-cluster-1,kube-system,aws-node
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python-libs,2.7.18,sysdig-dev-cluster-1,kube-system,aws-node
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python2-rpm,4.11.3,sysdig-dev-cluster-1,kube-system,aws-node
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python-iniparse,0.4,sysdig-dev-cluster-1,kube-system,aws-node
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python-pycurl,7.19.0,sysdig-dev-cluster-1,kube-system,aws-node
602401143452.dkr.ecr.us-west-2.amazonaws.com/amazon-k8s-cni:v1.11.4-eksbuild.1,python-urlgrabber,3.10,sysdig-dev-cluster-1,kube-system,aws-node
quay.io/sysdig/agent-slim:12.12.0,python38,3.8.13,sysdig-dev-cluster-1,sysdig-agent,sysdig-agent
quay.io/sysdig/agent-slim:12.12.0,python38-libs,3.8.13,sysdig-dev-cluster-1,sysdig-agent,sysdig-agent
quay.io/sysdig/agent-slim:12.12.0,python38-setuptools-wheel,41.6.0,sysdig-dev-cluster-1,sysdig-agent,sysdig-agent
```

If you do not specify a package it will generate a CSV report for all packages in your environment titled `all-runtime-image-packages.csv` in your current working directory.


