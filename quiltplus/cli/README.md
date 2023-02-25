# qp
## The quiltplus command-line tool

A more git-like and git-friendly wrapper (versus the exising Docker-centric CLI).

Stores configuration information in a folder that can be checked into source control.

This enables generic pipelines and automation that can transparently pull and create the right packages

# qp commands

Should try to infer group from subcommand

## qp info

Read and list all configuration files

## qp call

Package commands: get put post list diff

## qp stage

Pending edits: add rm status

## qp config

Configuration and dependencies: show dep deps 

## qp catalog

Call/open catalog: view revise registries

# Configuration Files

Stored inside a `.quilt` folder.

## config.yaml

```
quilt_config:
  version: 0.7.0
  uri: quilt+s3://_bucket_#package=_prefix/suffix_
  catalog: dns
  deps: []
  pipeline:
    inputs: [uri]
    outputs: [uri]
```

## stage.yaml

```
quilt_stage:
  version: 0.7.0
  entries:
  - path: p
    action: add
    created: timestamp
    updated: timestamp
    entered: timestamp
    hash: base65
    hash_type: enum

   
