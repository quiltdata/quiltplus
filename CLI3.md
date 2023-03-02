# Proposed quilt3+git MVP Workflow

## Draft 2

1. Create and use a local `data.yaml` file that can be checked into git
2. Do it all via the command-line
3. Extend semantics of existing `quilt3` operations
   1. `browse`, `install`, `push`
   2. Without new flags, all commands have identical behavior as today
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
quilt3 browse pkg/out --registry reg --dir data/out --to-config output
quilt3 browse pkg/dbout --registry reg --dir database/db1 --to-config output
git add data.yaml .gitignore 
git commmit -m "Ready to run"
```

Using repo with a generic production workflow:

```bash
git clone $REPO/my/project.git
cd project
quilt3 install --from-config # input data
quilt3 browse --from-config output 
poetry run main.py # or equivalent
quilt3 push --from-config output # appends new output data
```

## Specification

### --to-config: create/update configuration file

```bash
quilt3 [browse | install | push] --to-config [<config-key>]
```

* new option on `browse`, `install`, `push`
* creates ./data.yaml configuration file by default
  * or other name, if specified as an argument
  * or extends it, if exists
* stores directory AND the fully-qualified Quilt+ URI for that package and registry
  under 'packages' or _config-key_
* creates/updates `.quiltignore` with the configuration file
* automatically adds package files to `.gitignore` (create if it does not exist)

### --from-config: get package data from configuration file

```bash
quilt3 [browse | install | push] --from-config [<config-key>]
```

* new option on `browse`, `install`, `push`
* error if user also specifies a package name
* creates `./data.yaml` configuration file by default [else _config-key_]
  * error if config file malformed or does not exist
* automatically adds package files to `.gitignore` (create if doesn't exist)

### data.yaml configuration file formal

Each package is associated with a particular folder
inside the `quiltdata.io` namespace.
Use Quilt+ URIs as the canonical format for fully-qualified packages.

```yaml
data:
  version: 0.2.1
  quiltdata.io: 
    packages:
    - uri: quilt+s3://reg#package=pkg/new 
      dir: ./data
    - uri: quilt+s3://reg#package=pkg/exist
      dir: ./exist_data
    output:
    - uri: quilt+s3://reg#package=pkg/out 
      dir: ./data/out
    - uri: quilt+s3://reg#package=pkg/dbout
      dir: ./database/db1
  ```

## FAQ

* Q: How does `browse`, if it only copies the manifest,
  know how to patch local-only files into the existing package tree?

  * Quilt does not need to "patch" files the way DVC does.
    It just needs to get the list of files from the manifest
    and add them to `.gitignore` so git does not try to check them in.
