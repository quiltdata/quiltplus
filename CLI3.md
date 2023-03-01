# Proposed quilt3+git MVP Workflow

_Draft 2_

## Objectives

1. Create and use a local `quilt.yaml` file that can be checked into git
> Should we consider a more neutral name like `data.yaml` or dependencies.yaml?
2. Do it all via the command-line (without worrying about browse, etc.)
3. Extend semantics of existing `quilt3` operations
   1. `browse`, `install`, `push`
   2. Do NOT change existing semantics of any operation
   > Specifically all commands should be backwards-compatible without new flags
4. Address urgent use cases now while enabling richer functionality later
   1. Support creating configurations for both old and new packages
   2. Enable creating configurations without having to install
   3. Support multiple packages (with their own paths) in a single config
   4. Support multiple configuration files (e.g., input versus output)

Inspired by [this gist](https://gist.github.com/akarve/db4b8d5c032030df30b371127bc82e15)

## QuickStart

Creating repo from a working local pipeline:

```bash
git init
quilt3 push pkg/new --registry reg --dir data --to-config # new package
quilt3 install pkg/exist --registry reg --dir exist_data --to-config # existing package
git add *
quilt3 browse pkg/out --registry reg --dir data/out --to-config output.yaml
quilt3 browse pkg/dbout --registry reg --dir database/db1 --to-config output.yaml
git add output.yaml .gitignore 
git commmit -m "Ready to run"
```

Using repo with a generic production workflow:

```bash
git clone $MYREPO/first-test.git
cd first-test
quilt3 install --from-config # input data
quilt3 browse --from-config output.yaml 
poetry run main.py # or equivalent
quilt3 push --from-config output.yaml # appends new output data
```

## Specification

### --to-config: create/update configuration file

```bash
quilt3 [browse | install | push] --to-config [<config-file>]
```

* new option on `browse`, `install`, `push`
* creates ./quilt.yaml configuration file by default
  * or other name, if specified as an argument
  * or extends it, if exists
* stores directory AND the fully-qualified Quilt+ URI for that package and registry
> Isn't it more correc to say the URI is a pure function of what's in the file?
> I don't see any reason to be redundant and also include the URI
  * key-value pairs of "uri: path"
  * may use the short form URI: `quilt+s3://reg/package/name`
* creates/updates `.quiltignore` with the configuration file
* automatically adds package files to `.gitignore` (create if it does not exist)

> specifically how does `browse`, if it only copies the manifest, 
> know how to patch local-only files into the existing package tree?

### --from-config: get package data from configuration file

```bash
quilt3 [browse | install | push] --from-config [<config-file>]
```

* new option on `browse`, `install`, `push`
* error if user also specifies a package name
* creates `./quilt.yaml` configuration file by default [else config-file]
  * error if config file malformed or does not exist
* automatically adds package files to `.gitignore` (create if it does not exist)

### quilt.yaml configuration file formal

Each package is associated with a particular folder.
Use Quilt+ URIs as the canonical format for fully-qualified packages.

> The children of packages should be dicts not strings, so we have
*a lot* more flexibility.

```yaml
# last time we looked at this version works better at the top
version: 0.2.1 
packages:
  # prefer canonical URI; Sergey put a lot of thought into its correctness
  - uri: quilt+s3://bucket#package=foo/bar 
    local_folder: ./data
  - uri: quilt+s3://bucket#package=foo/baz
    local_folder: ./exist_data
```
