# Proposed quilt3+git MVP Workflow

## Objectives
* create and use local quilt.yaml file that can be checked into git
* do it all via the command-line (without worrying about browse, et al)
* build on top of `quilt3` install and push
* do NOT change existing semantics of any operation

## QuickStart
```bash
# From a working local pipeline 
git init
quilt push package/name --registry reg -dir data --init-config # new package from data
# OR  
quilt install package/name --registry reg -dir data --init-config existing package to data:
git add *
git commmit -m "Ready to run"

# In a production workflow
git pull https://github.com/ml-demo/first-test
quilt install --using-config
poetry run main.py # or equivalent
```

## --init-config: create and configure quilt.yaml
* new option on both `install` (existing packages) and `push` (new packages)
* creates ./quilt.yaml configuration file
* stores the fully-qualified Quilt+ URI for that package and registry
* creates .quiltignore that ignores the configuration folder (error if already exists)
* automatially adds package files to .gitignore (create if it does not exist)
* optional argument -> alternate path to config file
* error if quilt.yaml already exists: suggest "--extend-config" for appending packages


## --using-config: get default package from quilt.yaml
* new option on both `install` (existing packages) and `push` (existing packages)
* error if user also specifies a package name
* reads ./quilt.yaml configuration file (error if not exists)
* uses first URI entry from packages as the default
* automatially adds package files to .gitignore (error if it does not exist)
* optional argument -> alternate path to config file

## quilt.yaml: configuration file formal

Propose using Quilt+ URIs as our canonical storage format for fully-qualified packages.
Users would continue to use the existing CLI to create them.
```yaml
quilt_config:
  version: 0.1.0
  packages:
  - quilt+s3://reg#package=package/name
```


