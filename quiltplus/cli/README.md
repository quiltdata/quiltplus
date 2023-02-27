# qp
## The quiltplus command-line tool

A more git-like and git-friendly wrapper (versus the exising Docker-centric CLI).

Stores configuration information in a folder that can be checked into source control.

This enables generic pipelines and automation that can transparently pull and create the right packages.

## QuickStart

```bash
pip install quiltplus
export WRITE_BUCKET=writeable_s3_bucket
qp -U "quilt+s3://$(WRITE_BUCKET)#package=test/quiltplus"
qp call -x post # create empty package
time > README.md
qp stage -a README.md
qp stage # displays staged files
qp call -x patch # uploads staged files
```

## qp commands

Currently must be specified explicitly
### qp echo

Show configuration parameters

### qp call

Package commands: get list diff patch put post

TBD: verify

### qp stage

Pending edits: add rm status

## Future Ideas

### qp config

Configuration and dependencies: show dep deps

### qp catalog

Call/open catalog: view revise registries

## Configuration File Formats

`config.yml` stored inside a `.quilt` folder.

Includes potential keys not yet implemented.

```yaml
quiltconfig:
  version: 0.7.0
  uri: quilt+s3://_bucket_#package=_prefix/suffix_
  catalog: catalog.dns.name
  deps: []
  pipeline:
    inputs: [uri]
    outputs: [uri]
  stage:
    filename:
      path: filename
      action: add
      created: timestamp
      updated: timestamp
      entered: timestamp
      hash: base65
      hash_type: enum
```