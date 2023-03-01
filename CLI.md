# Proposed Git-Friendly Workflow

* create/manage local configuration file that can be checked into git
* explicitly manage status of local registry
* do it all via the command-line
* use Quilt+ URIs as the common currency

## QuickStart
```bash
# From a working local pipeline
quilt init "quilt+s3://ml-demos#package=ml-demo/first-test"
quilt add data/* --push
git add *
git commmit -m "Ready to run"

# In a production workflow
git pull https://github.com/ml-demo/first-test
quilt pull
poetry run main.py # or equivalent
```

## quilt new
```bash
quilt init $NEW_URI
```
* creates .quilt/config.yaml configuration file (error if already exists)
* creates empty package on the remote registry (error if already exists)
* creates empty package on the local registry (error if already exists)
* creates .quiltignore that ignores the configuration folder (error if already exists)
* creates .gitignore if it does not already exist

## quilt get
```bash
quilt get [-r | -t | -d] $OLD_URI
```
* downloads package from remote registry to local directory
* caches package in local registry
* creates .quilt/config.yaml configuration file (unless -t temporary)
* (error if already exists)
* if '-r', recursively gets 'deps' from local configuration file
* (warn if file/deps don't exists)
* if -d, add as 'deps' to config.yaml

## quilt pull
```bash
quilt pull [-n]
```
* downloads package from remote registry to local directory
* (error if config.yaml does not exist)
* caches package in local registry
* recursively gets 'deps' from local configuration file (unless -n)

## quilt add
```bash
quilt add [$FILES | -a | -s ] [-p]
```
* add files from local filesystem to local package (error if no config.yaml)
* automatically updates .gitignore
* if -a, instead add all files from current directory
* if -s, sync directory: add new/modified files, remove deleted files
* MAYBE: if -p, immediately push to remote

## quilt push
```bash
quilt push [-u $NEW_URI]
```
* sync local package to remote
* (or NEW_URI if -u, else error if no config.yaml)

## quilt config
```bash
quilt config [-d]
```
* print local configuration file
* delete if -d
* (warn if no config.yaml)


## quilt stat
```bash
quilt stat [-r* | -R | -l | -L | -i -I]
```
* "stat" current files
* returns list of files, with status:
  * A: added
  * D: deleted
  * M: modified
  * X: unknown/missing
* (error if no config.yaml)

### -r, --remote-diff (default)

* lists only files that differ between local and remote package
* (previews `push`)

### -R, --remote-all

* lists all files currently in remote package, by local status

### -l, --local-diff

* lists only files that differ between current directory and local package
* (previews `add -s`)

### -L, --local-all
* lists all files currently in local package, by diff status

### -i, --ignored-diff

* lists only files in local package that are NOT in .gitignore

### -I, --ignored-all
* lists all files in local package, by .gitignore status:
* I: ignored, U: un-ignored

