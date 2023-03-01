# Proposed Git-Centric Workflow

## quilt new
```bash
quilt new $NEW_URI
```
* creates .quilt/config.yaml configuration file (error if already exists)
* creates empty package on the remote registry (error if already exists)
* creates empty package on the local registry (error if already exists)
* creates .quiltignore that ignores the configuration folder (error if already exists)
* creates .gitignore if it does not already exist

## quilt get
```bash
quilt get [-r | -t] [$OLD_URI]
```
* downloads package from remote registry to local directory
* caches package in local registry
* if OLD_URI not specified, use uri from config.yaml (error if not exists)
* creates/updates .quilt/config.yaml configuration file (unless -t temporary)
* if '-r', recursively gets 'deps' from local configuration file 
* (warn if file/deps don't exists)

## quilt add
```bash
quilt add [$FILES | -a | -s ]
```
* add files from local filesystem to local package (error if no config.yaml)
* if -a, instead add all files from current directory
* if -s, sync: add new/modified files, remove deleted files
* (from current directory)

## quilt push
```bash
quilt push [-u $NEW_URI]
```
* sync local package to remote 
* (or NEW_URI if -u, else error if no config.yaml)

## quilt remote
```bash
quilt remote [-u $NEW_URI]
```
* lists files currently in remote package 
* (or NEW_URI if -u, else error if no config.yaml)

## quilt local
```bash
quilt local
```
* lists files currently in local package 
* (error if no config.yaml)

## quilt status
```bash
quilt status [-u $NEW_URI]
```
* lists files that differ between local and remote package
* (or NEW_URI instead of remote, if -u)
* (previews `push`)
* (error if no config.yaml or -u)

## quilt diff
```bash
quilt diff
```
* lists files that differ between current directory and local package 
* (previews `add -s`)
* (error if no config.yaml)

## quilt config
```bash
quilt config [-d]
```
* print local configuration file 
* delete if -d




