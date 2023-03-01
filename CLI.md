# Proposed Git-Friendly Workflow

* create/manage local configuration file that can be checked into git
* explicitly manage status of local registry
* do it all via the command-line

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
quilt add [$FILES | -a | -s ]
```
* add files from local filesystem to local package (error if no config.yaml)
* if -a, instead add all files from current directory
* if -s, sync directory: add new/modified files, remove deleted files
* MAYBE: if -p, immediately push to remote

## quilt push
```bash
quilt push [-u $NEW_URI]
```
* sync local package to remote 
* (or NEW_URI if -u, else error if no config.yaml)

## quilt remote
```bash
quilt remote [-u $OLD_URI]
```
* lists files currently in remote package 
* (or OLD_URI if -u, else error if no config.yaml)

## quilt config
```bash
quilt config [-d]
```
* print local configuration file 
* delete if -d
* (warn if no config.yaml)


## quilt stat
```bash
quilt stat [-r* | -l | -i | -R | -L | -I]
```
* "stat" current files
* (error if no config.yaml)

### -r: --remote-diff

* (default): lists files that differ between local and remote package
* (previews `push`)

### -R: --remote-all

* lists files currently in remote package 

### -l: --local-diff

* lists files that differ between current directory and local package 
* (previews `add -s`)

### -L: --local-all
* lists files currently in local package 
* (error if no config.yaml)

### -i: --ignored-diff

* lists files in local package that are NOT in .gitignore 

### -I: --ignored-all
* lists all files in local package, by .gitignore status 
* I: ignored, U: un-ignored

