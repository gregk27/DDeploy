# DDeploy
Small CLI utility which automatically builds and runs docker containers on a remote server.

# Usage
To deploy a container, run DDeploy with a path to the folder containing the dockerfile or a configuration file with `path` set. A config file path can also be specfied with `--config`.

DDeploy is configured using YAML, and will automatically look for `ddeploy.yml` in the specified folder.

## Configuration Options
### Can be specified in command or config file
`context`: The name of the [docker context](https://docs.docker.com/engine/reference/commandline/context/) to use

`name`: The name to be used for the image and container. If the conainer is running, it will be restarted with the new image

`restart`: Docker [restart policy](https://docs.docker.com/config/containers/start-containers-automatically/) to use

### Can only be specified in config file
`path`: Alternate path to locate dockerfile

`network`: Docker [--network flag](https://docs.docker.com/engine/reference/commandline/run/#connect-a-container-to-a-network---network)

`env`: Environment variables to be set, in the format `var:value`

`env-file`: Environment variables file, as specified in the [Docker documentation](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file)

`ports`: List of ports to be mapped, in the format `container:machine`

## Example Config
```yaml
context: "remote"
# Name the image/container Example
name: "Example"
# Restart the container if it stops
restart: "always"
# Use machine's localhost
network: "host"
# Set the production flag
env:
  - prod: "true"
# Map container port 80 to the machine's port 8080
ports:
  - 80: 8080
```