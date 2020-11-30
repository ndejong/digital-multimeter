# Digital Multimeter

## Development
The following tools are used to create and manage this package.

### shut 
Package release and management tools - https://pypi.org/project/shut - [documentation](https://github.com/NiklasRosenstein/shut/blob/develop/docs/docs/index.md)
```shell script
# Update package files
$ shut pkg update

# Create a changelog entry for a fix
$ shut changelog --add fix --stage --message "Fixes bug"

# Create a changelog entry for a feature
$ shut changelog --add feature --stage --message "Initial version"

# Patch release with push dry run
$ shut pkg bump --patch --tag --push --dry

# Patch release with push
$ shut pkg bump --patch --tag --push

# Minor release with push dry run
$ shut pkg bump --minor --tag --push

# Minor release with push dry run
$ shut pkg bump --major --tag --push
```

### pydoc-markdown
Documentation generation tools - https://pydoc-markdown.readthedocs.io/en/latest/
```shell script
# Render documentation
$ pydoc-markdown docs/pydoc-markdown.yml 

# Provide a local live review server 
$ pydoc-markdown --server docs/pydoc-markdown.yml
```
