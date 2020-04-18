#!/usr/bin/env python3
from os.path import abspath, basename, dirname, join
import argparse, glob, packaging, requests, subprocess, sys
from packaging.version import parse


# The base name of our generated images
PREFIX = 'adamrehn/ue4-runtime'

# The list of supported Ubuntu LTS releases
RELEASES = ['16.04', '18.04']

# The Ubuntu release that our alias tags point to
ALIAS_RELEASE = '18.04'


# Prints and runs a command
def run(command, dryRun):
	print(command, flush=True)
	if dryRun == False:
		subprocess.run(command, check=True)
	print()

# Builds a specific image variant and returns the tag
def buildImage(context, baseImage, tag, dryRun):
	buildArgs = ['--build-arg', 'BASEIMAGE=' + baseImage] if baseImage is not None else []
	run(['docker', 'build', '-t', tag] + buildArgs + [context], dryRun)
	return tag

# Adds a new tag for an image and returns a tuple of (alias, original)
def tagImage(source, target, dryRun):
	run(['docker', 'tag', source, target], dryRun)
	return (target, source)

# Pushes an image to Docker Hub
def pushImage(image, dryRun):
	run(['docker', 'push', image], dryRun)

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


# Parse our command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true', help='Print Docker commands without running them')
parser.add_argument('--push', action='store_true', help='Push tagged images to Docker Hub')
args = parser.parse_args()

# Compute the absolute path to the root directory containing our Dockerfiles
rootDir = dirname(abspath(__file__))

# Determine which versions of TensorFlow that we have a Dockerfile for and what the newest version is
tfVersions = [basename(dirname(v)) for v in glob.glob(join(rootDir, 'tensorflow', '*', 'Dockerfile'))]
newestTF = sorted([parse(v) for v in tfVersions])[-1]

# Keep track of the list of images we've built and alias tags we've generated
built = []
aliases = []

# Iterate over our supported Ubuntu LTS releases
for ubuntuRelease in RELEASES:
	
	# Retrieve the list of tags for the `nvidia/cudagl` development image for the current Ubuntu release
	cudaSuffix = '-devel-ubuntu{}'.format(ubuntuRelease)
	cudaTags = [tag for tag in listTags('nvidia/cudagl') if tag.endswith(cudaSuffix)]
	
	# Generate our list of ue4-runtime image variants and corresponding base images
	variants = {'vulkan': 'nvidia/opengl:1.0-glvnd-runtime-ubuntu{}'.format(ubuntuRelease)}
	for tag in cudaTags:
		variants['cudagl{}'.format(tag.replace(cudaSuffix, ''))] = 'nvidia/cudagl:{}'.format(tag)
	
	# Build the base image for each variant
	for suffix, baseImage in variants.items():
		tag = '{}:{}-{}'.format(PREFIX, ubuntuRelease, suffix)
		built.append(buildImage(join(rootDir, 'base'), baseImage, tag, args.dry_run))
	
	# Build each version of TensorFlow for which we have a Dockerfile
	# (Note that each Dockerfile has a hardcoded base image to match the required version of CUDA, so we don't specify one here)
	for tfVersion in tfVersions:
		tag = '{}:{}-tensorflow-{}'.format(PREFIX, ubuntuRelease, tfVersion)
		built.append(buildImage(join(rootDir, 'tensorflow', tfVersion), ubuntuRelease, tag, args.dry_run))
	
	# Build a VirtualGL-enabled version of each image
	vglBases = [image for image in built.copy() if ubuntuRelease in image]
	for baseImage in vglBases:
		tag = baseImage + '-virtualgl'
		built.append(buildImage(join(rootDir, 'virtualgl'), baseImage, tag, args.dry_run))

# Create OpenGL aliases for our OpenGL+Vulkan images, to maintain backwards compatibility with the tags for the old OpenGL-only images
for ubuntuRelease in RELEASES:
	aliases.append(tagImage('{}:{}-vulkan'.format(PREFIX, ubuntuRelease), '{}:{}-opengl'.format(PREFIX, ubuntuRelease), args.dry_run))

# Tag the Vulkan variant of the Ubuntu 18.04 base image as our "latest" tag
latest = '{}:latest'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan'.format(PREFIX, ALIAS_RELEASE), latest, args.dry_run))

# Tag the latest version of TensorFlow without a version suffix
unversionedTF = '{}:tensorflow'.format(PREFIX)
aliases.append(tagImage('{}:{}-tensorflow-{}'.format(PREFIX, ALIAS_RELEASE, newestTF), unversionedTF, args.dry_run))

# Tag the Vulkan variant of the VirtualGL image with a non-suffixed tag
nonSuffixedVgl = '{}:virtualgl'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan-virtualgl'.format(PREFIX, ALIAS_RELEASE), nonSuffixedVgl, args.dry_run))

# Tag the latest version of `ue4-runtime:tensorflow-virtualgl` without a version suffix
unversionedVgl = '{}:tensorflow-virtualgl'.format(PREFIX)
aliases.append(tagImage('{}:{}-tensorflow-{}-virtualgl'.format(PREFIX, ALIAS_RELEASE, newestTF), unversionedVgl, args.dry_run))

# Print the list of built images
print('The following images were built:\n')
for image in built:
	print(' - ' + image)
print()

# Print the list of tagged aliases
print('The following aliases were tagged:\n')
for alias, image in aliases:
	print(' - ' + alias + ' => ' + image)
print()

# Push the built images up to Docker Hub if requested
if args.push == True:
	for image in built + [alias for alias, original in aliases]:
		pushImage(image, args.dry_run)
