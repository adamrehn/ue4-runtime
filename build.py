#!/usr/bin/env python3
import argparse, requests, shutil, subprocess
from itertools import chain
from natsort import natsorted
from packaging.version import Version
from pathlib import Path


# The base name of our generated images
PREFIX = 'adamrehn/ue4-runtime'

# The list of supported Ubuntu LTS releases
RELEASES = ['20.04', '22.04']

# The Ubuntu release that our alias tags point to
ALIAS_RELEASE = '20.04'


# Prints and runs a command
def run(command, dryRun):
	print([str(c) for c in command], flush=True)
	if dryRun == False:
		subprocess.run(command, check=True)
	print()

# Builds a container image
def buildImage(context, tag, buildArgs, dryRun):
	flags = [['--build-arg', '{}={}'.format(k,v)] for k, v in buildArgs.items()]
	command = ['docker', 'buildx', 'build', '--progress=plain', '-t', tag, context] + list(chain.from_iterable(flags))
	run(command, dryRun=dryRun)

# Builds a specific container image variant and returns the tag
def buildVariant(context, baseImage, tag, dryRun):
	buildArgs = {'BASEIMAGE': baseImage} if baseImage is not None else {}
	buildImage(context, tag, buildArgs, dryRun)
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
parser.add_argument('--readme', action='store_true', help='Generate descriptive tag list for README file')
args = parser.parse_args()

# Compute the path to the root directory containing our Dockerfiles, and key subdirectories
rootDir = Path(__file__).parent
externalDir = rootDir / 'external'

# Keep track of the list of images we've built, descriptions for the built images, and alias tags we've generated
built = []
descriptions = {}
aliases = []

# Iterate over our supported Ubuntu LTS releases
for ubuntuRelease in RELEASES:
	
	# The base description string for all image tags within the current Ubuntu release
	releaseDescription = 'Ubuntu {} + OpenGL + Vulkan'.format(ubuntuRelease)
	
	# Retrieve the list of tags for the `nvidia/cuda` base image for the current Ubuntu release
	cudaSuffix = '-base-ubuntu{}'.format(ubuntuRelease)
	cudaTags = natsorted([tag for tag in listTags('nvidia/cuda') if tag.endswith(cudaSuffix)])
	
	# Identify the newest minor release for each major CUDA release
	cudaVersions = list([Version(tag.replace(cudaSuffix, '')) for tag in cudaTags])
	majorVersions = set([version.major for version in cudaVersions])
	minorVersions = {
		majorVersion: str(max([version for version in cudaVersions if version.major == majorVersion]))
		for majorVersion in majorVersions
	}
	
	# Clone the source code for the `nvidia/opengl` base image for the current Ubuntu release
	openglDir = externalDir / 'opengl_{}'.format(ubuntuRelease)
	if not openglDir.exists() and not args.dry_run:
		run(['git', 'clone', '--depth=1', '-b', 'ubuntu{}'.format(ubuntuRelease), 'https://gitlab.com/nvidia/container-images/opengl.git', str(openglDir)], False)
		shutil.copy2(openglDir / 'NGC-DL-CONTAINER-LICENSE', openglDir / 'base' / 'NGC-DL-CONTAINER-LICENSE')
	
	# Generate our list of ue4-runtime image variants and corresponding base images
	variants = {'vulkan': 'nvidia/opengl:1.2-glvnd-runtime-ubuntu{}'.format(ubuntuRelease)}
	variantDescriptions = {'vulkan': ''}
	for majorVersion, minorVersion in minorVersions.items():
		
		# Record the variant details
		variant = 'cudagl{}'.format(majorVersion)
		variants[variant] = 'nvidia/cudagl:{}-runtime-ubuntu{}'.format(majorVersion, ubuntuRelease)
		variantDescriptions[variant] = ' + CUDA {}'.format(minorVersion)
		
		# Build our own version of the `nvidia/cudagl` base image for the given version of CUDA, since NVIDIA is not currently updating the upstream image
		buildImage(openglDir / 'base', 'nvidia/cudagl:{}-base-ubuntu{}'.format(majorVersion, ubuntuRelease), {'from': 'nvidia/cuda:{}{}'.format(minorVersion, cudaSuffix)}, args.dry_run)
		buildImage(openglDir / 'glvnd' / 'runtime', variants[variant], {'from': 'nvidia/cudagl:{}-base-ubuntu{}'.format(majorVersion, ubuntuRelease), 'LIBGLVND_VERSION': '1.2'}, args.dry_run)
	
	# Build the base image for each variant (the "noaudio" version without PulseAudio)
	# (Add these to a temporary list so we can place them after the non-suffixed tags when we print our tag list)
	noAudio = []
	for suffix, baseImage in variants.items():
		tag = '{}:{}-{}-noaudio'.format(PREFIX, ubuntuRelease, suffix)
		noAudio.append(buildVariant(rootDir / 'base', baseImage, tag, args.dry_run))
		descriptions[noAudio[-1]] = releaseDescription + variantDescriptions[suffix] + ' (no audio support)'
	
	# Build a version of each image that supports audio by running a PulseAudio server inside the container
	# (This is the default recommended variant, so we tag it without a suffix)
	for baseImage in noAudio:
		tag = baseImage.replace('-noaudio', '')
		built.append(buildVariant(rootDir / 'pulseaudio', baseImage, tag, args.dry_run))
		descriptions[built[-1]] = descriptions[baseImage].replace(' (no audio support)', ' + PulseAudio Client + PulseAudio Server')
	
	# Add the "-noaudio" tags to our tag list immediately after the non-suffixed tags
	built.extend(noAudio)
	
	# Build a version of each image that supports audio by using the host system's PulseAudio server
	for baseImage in noAudio:
		tag = baseImage.replace('-noaudio', '-hostaudio')
		built.append(buildVariant(rootDir / 'hostaudio', baseImage, tag, args.dry_run))
		descriptions[built[-1]] = descriptions[baseImage].replace(' (no audio support)', ' + PulseAudio Client (uses host PulseAudio Server)')
	
	# Build a VirtualGL-enabled version of the non-suffixed images that run a PulseAudio server inside the container
	bases = [image for image in built.copy() if ubuntuRelease in image and not image.endswith('audio')]
	for baseImage in bases:
		tag = baseImage + '-virtualgl'
		built.append(buildVariant(rootDir / 'virtualgl', baseImage, tag, args.dry_run))
		descriptions[built[-1]] = descriptions[baseImage] + ' + VirtualGL'

# Tag the Vulkan variant of the Ubuntu 20.04 base image as our "latest" tag
latest = '{}:latest'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan'.format(PREFIX, ALIAS_RELEASE), latest, args.dry_run))

# Create OpenGL aliases for our OpenGL+Vulkan images, to maintain backwards compatibility with the tags for the old OpenGL-only images
for ubuntuRelease in RELEASES:
	aliases.append(tagImage('{}:{}-vulkan'.format(PREFIX, ubuntuRelease), '{}:{}-opengl'.format(PREFIX, ubuntuRelease), args.dry_run))

# Tag the Vulkan variant of the VirtualGL image with a non-suffixed tag
nonSuffixedVgl = '{}:virtualgl'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan-virtualgl'.format(PREFIX, ALIAS_RELEASE), nonSuffixedVgl, args.dry_run))

# Tag the Vulkan variant of the "noaudio" image with a non-suffixed tag
nonSuffixedNoAudio = '{}:noaudio'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan-noaudio'.format(PREFIX, ALIAS_RELEASE), nonSuffixedNoAudio, args.dry_run))

# Tag the Vulkan variant of the host audio image with a non-suffixed tag
nonSuffixedHostAudio = '{}:hostaudio'.format(PREFIX)
aliases.append(tagImage('{}:{}-vulkan-hostaudio'.format(PREFIX, ALIAS_RELEASE), nonSuffixedHostAudio, args.dry_run))

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
	for image in built + [alias for alias, _ in aliases]:
		pushImage(image, args.dry_run)

# Determine whether we are generating the descriptive tag list used to populate the repository's README file
if args.readme == True:
	
	print('----------------')
	print('README TAG LISTS')
	print('----------------')
	print()
	
	# Pretty-formats a tag
	formatTag = lambda tag: '**{}**'.format(tag.replace('adamrehn/ue4-runtime:', ''))
	
	# Print the descriptive details of our alias tags
	print('## Alias tags\n')
	print('The following tags are provided as convenient aliases for the fully-qualified tags of common image variants:\n')
	for alias, image in aliases:
		print('- {} is an alias for {}'.format(formatTag(alias), formatTag(image)))
	
	# Iterate over our supported Ubuntu LTS releases
	for ubuntuRelease in reversed(RELEASES):
		
		print('\n\n## Ubuntu {} tags\n'.format(ubuntuRelease))
		images = [image for image in built.copy() if ubuntuRelease in image]
		for image in images:
			print('- {}: {}'.format(formatTag(image), descriptions[image]))
	
	print()
