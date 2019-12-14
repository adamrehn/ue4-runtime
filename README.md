Container images for running packaged UE4 projects
==================================================

The various tags of the [adamrehn/ue4-runtime](https://hub.docker.com/r/adamrehn/ue4-runtime) image provide minimal, pre-configured environments for running packaged Unreal Engine projects with full GPU acceleration via [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker). (For more details on NVIDIA Docker, see the [NVIDIA Docker primer](https://unrealcontainers.com/docs/concepts/nvidia-docker) on the Unreal Containers community hub.) Note that these images will work with packaged Linux builds **from any source**, not just builds packaged using the container images from the [ue4-docker](https://github.com/adamrehn/ue4-docker) project.

Both OpenGL and OpenGL+CUDA variants are provided, along with preconfigured images for common GPU-accelerated frameworks such as [TensorFlow](https://www.tensorflow.org/). Each image variant is also available in a configuration with [VirtualGL](https://www.virtualgl.org/) bundled for displaying the output of OpenGL applications using the host system's display. See the section [Using the VirtualGL images](#using-the-virtualgl-images) for usage details.

For details on using these images to perform cloud rendering via NVIDIA Docker, see the [Cloud rendering guide](https://unrealcontainers.com/docs/use-cases/cloud-rendering) on the Unreal Containers community hub.


## Alias tags

The following tags are provided as convenient aliases for the fully-qualified tags of common image variants:

- `adamrehn/ue4-runtime`:**latest** is an alias for `adamrehn/ue4-runtime`:**18.04-opengl**
- `adamrehn/ue4-runtime`:**tensorflow** is an alias for `adamrehn/ue4-runtime`:**18.04-tensorflow-1.13.1**
- `adamrehn/ue4-runtime`:**virtualgl** is an alias for `adamrehn/ue4-runtime`:**18.04-opengl-virtualgl**
- `adamrehn/ue4-runtime`:**tensorflow-virtualgl** is an alias for `adamrehn/ue4-runtime`:**18.04-tensorflow-1.13.1-virtualgl**


## Ubuntu 18.04 tags

- `adamrehn/ue4-runtime`:**18.04-opengl**: Ubuntu 18.04 + OpenGL
- `adamrehn/ue4-runtime`:**18.04-cudagl9.2**: Ubuntu 18.04 + OpenGL + CUDA 9.2
- `adamrehn/ue4-runtime`:**18.04-cudagl10.0**: Ubuntu 18.04 + OpenGL + CUDA 10.0
- `adamrehn/ue4-runtime`:**18.04-cudagl10.1**: Ubuntu 18.04 + OpenGL + CUDA 10.1
- `adamrehn/ue4-runtime`:**18.04-cudagl10.2**: Ubuntu 18.04 + OpenGL + CUDA 10.2
- `adamrehn/ue4-runtime`:**18.04-tensorflow-1.13.1**: Ubuntu 18.04 + OpenGL + CUDA 10.0 + TensorFlow 1.13.1
- `adamrehn/ue4-runtime`:**18.04-opengl-virtualgl**: Ubuntu 18.04 + OpenGL + VirtualGL
- `adamrehn/ue4-runtime`:**18.04-cudagl9.2-virtualgl**: Ubuntu 18.04 + OpenGL + CUDA 9.2 + VirtualGL
- `adamrehn/ue4-runtime`:**18.04-cudagl10.0-virtualgl**: Ubuntu 18.04 + OpenGL + CUDA 10.0 + VirtualGL
- `adamrehn/ue4-runtime`:**18.04-cudagl10.1-virtualgl**: Ubuntu 18.04 + OpenGL + CUDA 10.1 + VirtualGL
- `adamrehn/ue4-runtime`:**18.04-cudagl10.2-virtualgl**: Ubuntu 18.04 + OpenGL + CUDA 10.2 + VirtualGL
- `adamrehn/ue4-runtime`:**18.04-tensorflow-1.13.1-virtualgl**: Ubuntu 18.04 + OpenGL + CUDA 10.0 + TensorFlow 1.13.1 + VirtualGL


## Ubuntu 16.04 tags

- `adamrehn/ue4-runtime`:**16.04-opengl**: Ubuntu 16.04 + OpenGL
- `adamrehn/ue4-runtime`:**16.04-cudagl9.0**: Ubuntu 16.04 + OpenGL + CUDA 9.0
- `adamrehn/ue4-runtime`:**16.04-cudagl9.1**: Ubuntu 16.04 + OpenGL + CUDA 9.1
- `adamrehn/ue4-runtime`:**16.04-cudagl9.2**: Ubuntu 16.04 + OpenGL + CUDA 9.2
- `adamrehn/ue4-runtime`:**16.04-cudagl10.0**: Ubuntu 16.04 + OpenGL + CUDA 10.0
- `adamrehn/ue4-runtime`:**16.04-cudagl10.1**: Ubuntu 16.04 + OpenGL + CUDA 10.1
- `adamrehn/ue4-runtime`:**16.04-cudagl10.2**: Ubuntu 16.04 + OpenGL + CUDA 10.2
- `adamrehn/ue4-runtime`:**16.04-tensorflow-1.13.1**: Ubuntu 16.04 + OpenGL + CUDA 10.0 + TensorFlow 1.13.1
- `adamrehn/ue4-runtime`:**16.04-opengl-virtualgl**: Ubuntu 16.04 + OpenGL + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl9.0-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 9.0 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl9.1-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 9.1 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl9.2-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 9.2 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl10.0-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 10.0 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl10.1-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 10.1 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-cudagl10.2-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 10.2 + VirtualGL
- `adamrehn/ue4-runtime`:**16.04-tensorflow-1.13.1-virtualgl**: Ubuntu 16.04 + OpenGL + CUDA 10.0 + TensorFlow 1.13.1 + VirtualGL


## Using the VirtualGL images

The `virtualgl` configuration of each image variant adds the following components:

- The X11 libraries needed for running applications that create X11 windows
- [VirtualGL](https://www.virtualgl.org/) itself, which provides the `vglrun` command for interposing OpenGL function calls

To run a container using a VirtualGL-enabled image, the Docker host system will need to be running an X11 server and you will need to bind-mount the host's X11 socket inside the container like so:

```bash
# Replace "adamrehn/ue4-runtime:virtualgl" with your chosen image tag
docker run --runtime=nvidia -v/tmp/.X11-unix:/tmp/.X11-unix:rw -e DISPLAY adamrehn/ue4-runtime:virtualgl bash
```

The manner in which you need to invoke UE4 projects inside the container depends on your use case:

- If you are running the container locally on a machine with an OpenGL-enabled X11 configuration (e.g. a standard desktop installation of Ubuntu 18.04) then the [GLVND](https://github.com/NVIDIA/libglvnd) dispatch library provided by the NVIDIA base images will handle the relevant OpenGL function calls without the need to use VirtualGL. **Running UE4 projects via `vglrun` in this scenario will actually reduce performance** due to the additional interposition overheads, so be sure to run projects directly. (e.g. `./MyProject.sh`)

- If you are running the container on a remote host and are using X11 forwarding to display the window on your local machine then you will need to run UE4 projects via `vglrun` in order to ensure OpenGL functionality will work from within an SSH session. (e.g. `vglrun ./MyProject.sh`)


## Building the images from source

Building the container images from source requires Python 3.5 or newer and the dependency packages listed in [requirements.txt](https://github.com/adamrehn/ue4-runtime/blob/master/requirements.txt).

To build the images, simply run `build.py`. This will automatically query Docker Hub to retrieve the list of available [nvidia/cudagl](https://hub.docker.com/r/nvidia/cudagl) base images based on Ubuntu LTS releases and build all variants of the `adamrehn/ue4-runtime` image accordingly.


## Legal

Copyright &copy; 2019, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/ue4-runtime/blob/master/LICENSE) for details.

Initial development of the TensorFlow 1.13.1 image variant was funded by [Deepdrive, Inc](https://deepdrive.io/).
