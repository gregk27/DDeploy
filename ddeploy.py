import argparse
import sys

# Register command line arguments
parser = argparse.ArgumentParser(description="Deploy docker container to remote server using docker context. A configuration file is required ports and environment variables. Command line arguments will override configuration file.")
parser.add_argument('path', metavar='Path', type=str, nargs='?', \
    help="Path to folder with dockerfile", default=".")
parser.add_argument('--config', metavar='config', type=str, \
    help='Path to configuration file, defaults to ./ddeploy.yml', default='./ddeploy.yml')
parser.add_argument('-c', '--context', metavar="context", type=str, \
    help="Docker context to use")
parser.add_argument('-n', '--name', metavar="name", type=str, \
    help="Name for image and container, defaults to folder name")
parser.add_argument('--restart', metavar="flag", type=str, \
    help="Restart policy for the continer, defaults to always", default="always")

# Parse the arguments
parser.parse_args(sys.argv)

args = parser.parse_args()
print(args)