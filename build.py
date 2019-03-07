#!/usr/bin/env python3
from os.path import abspath, basename, dirname, join
import glob, packaging, requests, subprocess, sys
from packaging.version import parse


# The base name of our generated images
IMAGE = 'adamrehn/ue4-runtime'


# Prints and runs a command
def run(command):
	print(command, flush=True)
	subprocess.run(command, check=True)
	print()

# Builds a specific image variant
def buildImage(context, baseImage, tag):
	buildArgs = ['--build-arg', 'BASEIMAGE=' + baseImage] if baseImage is not None else []
	run(['docker', 'build', '-t', tag] + buildArgs + [context])

# Adds a new tag for an image
def tagImage(source, target):
	run(['docker', 'tag', source, target])

# Pushes an image to Docker Hub
def pushImage(image):
	run(['docker', 'push', image])

# Retrieves the list of tags for an image on Docker Hub
def listTags(image):
	
	# Compute the v2 HTTP API endpoint for listing the image's tags
	endpoint = 'https://index.docker.io/v2/{}/tags/list'.format(image)
	
	# Retrieve an authentication token for the registry
	auth = dict([
		field.split('=')
		for field in
		requests.get(endpoint).headers['Www-Authenticate'].replace('"', '').split(',')
	])
	token = requests.get(auth['Bearer realm'], params=auth).json()['token']
	
	# Retrieve the list of tags for the image
	return requests.get(endpoint, headers={'Authorization': 'Bearer {}'.format(token)}).json()['tags']


# Compute the absolute path to the root directory containing our Dockerfiles
rootDir = dirname(abspath(__file__))

# Retrieve the list of Ubuntu 18.04-based tags for the `nvidia/cudagl` development image
cudaSuffix = '-devel-ubuntu18.04'
cudaTags = [tag for tag in listTags('nvidia/cudagl') if tag.endswith(cudaSuffix)]

# Generate our list of ue4-runtime image variants and corresponding base images
variants = {'opengl': 'nvidia/opengl:1.0-glvnd-runtime-ubuntu18.04'}
for tag in cudaTags:
	variants['cudagl{}'.format(tag.replace(cudaSuffix, ''))] = 'nvidia/cudagl:{}'.format(tag)

# Keep track of the list of images we've built
built = []

# Build the `ue4-runtime:base` image for each variant
for suffix, baseImage in variants.items():
	tag = '{}:base-{}'.format(IMAGE, suffix)
	buildImage(join(rootDir, 'base'), baseImage, tag)
	built.append(tag)

# Build each version of TensorFlow for which we have a Dockerfile
# (Note that each Dockerfile has a hardcoded base image to match the required version of CUDA, so we don't specify one here)
tfVersions = [basename(dirname(v)) for v in glob.glob(join(rootDir, 'tensorflow', '*', 'Dockerfile'))]
for tfVersion in tfVersions:
	tag = '{}:tensorflow-{}'.format(IMAGE, tfVersion)
	buildImage(join(rootDir, 'tensorflow', tfVersion), None, tag)
	built.append(tag)

# Build a VirtualGL-enabled version of each image
vglBases = built.copy()
for baseImage in vglBases:
	if 'latest' in baseImage:
		tag = baseImage.replace('latest', 'virtualgl')
	elif 'base' in baseImage:
		tag = baseImage.replace('base', 'virtualgl')
	else:
		tag = baseImage + '-virtualgl'
	buildImage(join(rootDir, 'virtualgl'), baseImage, tag)
	built.append(tag)

# Tag the OpenGL variant of `ue4-runtime:base` as our "latest" tag
latest = '{}:latest'.format(IMAGE)
tagImage('{}:base-opengl'.format(IMAGE), latest)
built.append(latest)

# Tag the latest version of `ue4-runtime:tensorflow` without a version suffix
newestTF = sorted([parse(v) for v in tfVersions])[-1]
unversionedTF = '{}:tensorflow'.format(IMAGE)
tagImage('{}:tensorflow-{}'.format(IMAGE, newestTF), unversionedTF)
built.append(unversionedTF)

# Tag the OpenGL variant of `ue4-runtime:virtualgl` with a non-suffixed tag
nonSuffixedVgl = '{}:virtualgl'.format(IMAGE)
tagImage('{}:virtualgl-opengl'.format(IMAGE), nonSuffixedVgl)
built.append(nonSuffixedVgl)

# Tag the latest version of `ue4-runtime:tensorflow-virtualgl` without a version suffix
unversionedVgl = '{}:tensorflow-virtualgl'.format(IMAGE)
tagImage('{}:tensorflow-{}-virtualgl'.format(IMAGE, newestTF), unversionedVgl)
built.append(unversionedVgl)

# Print the list of built images
print('The following images were built/tagged:\n')
for image in built:
	print(' - ' + image)
print()

# If `--push` was specified, push the built images up to Docker Hub
if (len(sys.argv) > 1 and sys.argv[1].lower() == '--push'):
	for image in built:
		pushImage(image)
