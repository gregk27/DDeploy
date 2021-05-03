import argparse
import sys
import os
import re
import yaml

# Register command line arguments
parser = argparse.ArgumentParser(description="Deploy docker container to remote server using docker context. A configuration file is required ports and environment variables. Command line arguments will override configuration file.")
parser.add_argument('path', metavar='Path', type=str, nargs='?', \
    help="Path to folder with dockerfile")
parser.add_argument('--config', metavar='config', type=str, \
    help='Path to configuration file, defaults to ./ddeploy.yml', default='./ddeploy.yml')
parser.add_argument('-c', '--context', metavar="context", type=str, \
    help="Docker context to use")
parser.add_argument('-n', '--name', metavar="name", type=str, \
    help="Name for image and container, defaults to folder name")
parser.add_argument('--restart', metavar="flag", type=str, \
    help="Restart policy for the continer, defaults to always")

# Parse the arguments
args = vars(parser.parse_args())
# print(args)

# Read from config file if present
if(not os.path.isfile(args['config'])):
    print("Configuration file not found, deploying from cli arguments.")
else:
    data = yaml.load(open(args['config'], 'r'), Loader=yaml.Loader)
    # Set path if not overriden, otherwise default
    if(args['path']==None and 'path' in data):
        args['path'] = data['path']
    elif(args['path']==None and 'path' not in data):
        args['path'] = '.'
    # Set context if not overriden
    if(args['context']==None and 'context' in data):
        args['context'] = data['context']
    # Set name if not overriden
    if(args['name']==None and 'name' in data):
        args['name'] = data['name']
    # Set restart if not overriden, otherwise default
    if(args['restart']==None and 'restart' in data):
        args['restart'] = data['restart']
    elif(args['restart']==None and 'restart' not in data):
        args['restart'] = 'always'
    if('ports' in data):
        args['ports'] = ""
        for port in data['ports']:
            args['ports'] += " -p "+str(list(port)[0])+":"+str(port[list(port)[0]])+" "
    else:
        args['ports'] = None
    if('env' in data):
        args['env'] = ""
        for env in data['env']:
            args['env'] += " -e "+str(list(env)[0])+"=\""+str(env[list(env)[0]])+"\" "
    else:
        args['env'] = None
    if('env-file' in data):
        args['env-file'] = data['env-file']
    else:
        args['env-file'] = None
    
FOLDER_PATTERN = re.compile("([^/\\\\]*)$")

# Validate inputs
if(args['name'] == None):
    args['name'] = FOLDER_PATTERN.findall(os.getcwd())[0]
if(args['context'] == None):
    print("A context is required to deploy. Please provide on in a configuration or as an argument.")
    sys.exit(1)
args['name'] = args['name'].lower().replace(" ", "-")

# print(args)
# Build the image
print("Building image", args['name'], "from", args['path']+"/Dockerfile")
os.system("docker --context "+args['context']+" build -t "+args['name']+" "+args['path'])

# Remove exsiting container
print("Stopping and removing existing container")
os.system("docker --context "+args['context']+" stop "+args['name'])
os.system("docker --context "+args['context']+" rm "+args['name'])

# Run the image
print("Running image", args['name'], "on", args['context'])
command = "docker --context "+args['context']+" run -d --name "+args['name']+" "+" --restart "+args['restart']
if(args['ports']!=None):
    command += " "+args['ports']
if(args['env']!=None):
    command += " "+args['env']
if(args['env-file']!=None):
    command += " --env-file "+args['env-file']
command += " "+args['name']
os.system(command)