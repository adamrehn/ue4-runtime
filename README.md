Container images for running packaged Unreal Engine projects
============================================================

The various tags of the [adamrehn/ue4-runtime](https://hub.docker.com/r/adamrehn/ue4-runtime) image provide minimal, pre-configured environments for running packaged Unreal Engine projects with full GPU acceleration via [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker). (For more details on NVIDIA Docker, see the [NVIDIA Docker primer](https://adamrehn.com/docs/ue4-docker/read-these-first/nvidia-docker-primer) from the ue4-docker documentation.) Note that these images will work with packaged Linux builds **from any source**, not just builds packaged using the container images from the [ue4-docker](https://github.com/adamrehn/ue4-docker) project.

Both OpenGL and OpenGL+CUDA variants are provided, along with preconfigured images for common GPU-accelerated frameworks such as [TensorFlow](https://www.tensorflow.org/). Each image variant is also available in a configuration with [VirtualGL](https://www.virtualgl.org/) bundled for displaying the output of OpenGL applications using the host system's display.

The following variants are available:

- `adamrehn/ue4-runtime:`**base-opengl** is a base image with OpenGL support
- `adamrehn/ue4-runtime:`**base-cudagl9.2** is a base image with OpenGL + CUDA 9.2 support
- `adamrehn/ue4-runtime:`**base-cudagl10.0** is a base image with OpenGL + CUDA 10.0 support
- `adamrehn/ue4-runtime:`**virtualgl-opengl** extends the base OpenGL image with VirtualGL
- `adamrehn/ue4-runtime:`**virtualgl-cudagl9.2** extends the base CUDA 9.2 image with VirtualGL
- `adamrehn/ue4-runtime:`**virtualgl-cudagl10.0** extends the base CUDA 10.0 image with VirtualGL
- `adamrehn/ue4-runtime:`**tensorflow-1.13.1** extends the base CUDA 10.0 image with TensorFlow 1.13.1
- `adamrehn/ue4-runtime:`**tensorflow-1.13.1-virtualgl** extends the TensorFlow 1.13.1 image with VirtualGL

The following tags are merely concise aliases for more specific tags:

- `adamrehn/ue4-runtime:`**latest** is an alias for `adamrehn/ue4-runtime:`**base-opengl**
- `adamrehn/ue4-runtime:`**tensorflow** is an alias for `adamrehn/ue4-runtime:`**tensorflow-1.13.1**
- `adamrehn/ue4-runtime:`**virtualgl** is an alias for `adamrehn/ue4-runtime:`**virtualgl-opengl**
- `adamrehn/ue4-runtime:`**tensorflow-virtualgl** is an alias for `adamrehn/ue4-runtime:`**tensorflow-1.13.1-virtualgl**


## Building the images from source

Building the container images from source requires Python 3.5 or newer and the dependency packages listed in [requirements.txt](https://github.com/adamrehn/ue4-runtime/blob/master/requirements.txt).

To build the images, simply run `build.py`. This will automatically query Docker Hub to retrieve the list of available [nvidia/cudagl](https://hub.docker.com/r/nvidia/cudagl) base images based on Ubuntu 18.04 and build all variants of the `adamrehn/ue4-runtime` image accordingly.


## Legal

Copyright &copy; 2019, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/ue4-runtime/blob/master/LICENSE) for details.

Development of the TensorFlow image was funded by [Deepdrive, Inc](https://deepdrive.io/).
