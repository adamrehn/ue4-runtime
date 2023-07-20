# Container images for running packaged Unreal Engine projects

The various tags of the [adamrehn/ue4-runtime](https://hub.docker.com/r/adamrehn/ue4-runtime) image provide minimal, pre-configured environments for running packaged Unreal Engine projects with full GPU acceleration via the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker). (For more details on the NVIDIA Container Toolkit, see the [NVIDIA Container Toolkit primer](https://unrealcontainers.com/docs/concepts/nvidia-docker) on the Unreal Containers community hub.) Note that these images will work with packaged Linux builds **from any source**, not just builds packaged using the container images from the [ue4-docker](https://github.com/adamrehn/ue4-docker) project.

Both OpenGL+Vulkan and OpenGL+Vulkan+CUDA variants are provided. Each image variant is also available in a configuration with the X11 runtime libraries bundled for displaying the output of packaged Unreal Engine projects on the host system's display. See the section [Using the X11 images](#using-the-x11-images) for usage details.

For details on using these images to perform cloud rendering via the NVIDIA Container Toolkit, see the [Cloud rendering guide](https://unrealcontainers.com/docs/use-cases/cloud-rendering) on the Unreal Containers community hub. There are also [example Dockerfiles](https://github.com/adamrehn/ue4-example-dockerfiles) available that demonstrate various uses of Unreal Engine containers, including multi-stage build workflows that encapsulate packaged projects in variants of the `ue4-runtime` image.


## Alias tags

The following tags are provided as convenient aliases for the fully-qualified tags of common image variants:

- **latest** is an alias for **20.04-vulkan**
- **20.04-opengl** is an alias for **20.04-vulkan**
- **22.04-opengl** is an alias for **22.04-vulkan**
- **noaudio** is an alias for **20.04-vulkan-noaudio**
- **hostaudio** is an alias for **20.04-vulkan-hostaudio**
- **x11** is an alias for **20.04-vulkan-x11**


## Ubuntu 22.04 tags

- **22.04-vulkan**: Ubuntu 22.04 + OpenGL + Vulkan + PulseAudio Client + PulseAudio Server
- **22.04-cudagl11**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client + PulseAudio Server
- **22.04-cudagl12**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client + PulseAudio Server
- **22.04-vulkan-noaudio**: Ubuntu 22.04 + OpenGL + Vulkan (no audio support)
- **22.04-cudagl11-noaudio**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 11.8.0 (no audio support)
- **22.04-cudagl12-noaudio**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 12.2.0 (no audio support)
- **22.04-vulkan-hostaudio**: Ubuntu 22.04 + OpenGL + Vulkan + PulseAudio Client (uses host PulseAudio Server)
- **22.04-cudagl11-hostaudio**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client (uses host PulseAudio Server)
- **22.04-cudagl12-hostaudio**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client (uses host PulseAudio Server)
- **22.04-vulkan-x11**: Ubuntu 22.04 + OpenGL + Vulkan + PulseAudio Client (uses host PulseAudio Server) + X11
- **22.04-cudagl11-x11**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client (uses host PulseAudio Server) + X11
- **22.04-cudagl12-x11**: Ubuntu 22.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client (uses host PulseAudio Server) + X11


## Ubuntu 20.04 tags

- **20.04-vulkan**: Ubuntu 20.04 + OpenGL + Vulkan + PulseAudio Client + PulseAudio Server
- **20.04-cudagl11**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client + PulseAudio Server
- **20.04-cudagl12**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client + PulseAudio Server
- **20.04-vulkan-noaudio**: Ubuntu 20.04 + OpenGL + Vulkan (no audio support)
- **20.04-cudagl11-noaudio**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 11.8.0 (no audio support)
- **20.04-cudagl12-noaudio**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 12.2.0 (no audio support)
- **20.04-vulkan-hostaudio**: Ubuntu 20.04 + OpenGL + Vulkan + PulseAudio Client (uses host PulseAudio Server)
- **20.04-cudagl11-hostaudio**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client (uses host PulseAudio Server)
- **20.04-cudagl12-hostaudio**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client (uses host PulseAudio Server)
- **20.04-vulkan-x11**: Ubuntu 20.04 + OpenGL + Vulkan + PulseAudio Client (uses host PulseAudio Server) + X11
- **20.04-cudagl11-x11**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 11.8.0 + PulseAudio Client (uses host PulseAudio Server) + X11
- **20.04-cudagl12-x11**: Ubuntu 20.04 + OpenGL + Vulkan + CUDA 12.2.0 + PulseAudio Client (uses host PulseAudio Server) + X11


## Vulkan rendering

**Offscreen rendering with Vulkan requires projects built with Unreal Engine 4.25.0 or newer.** To render offscreen, specify the `-RenderOffscreen` flag when running your packaged Unreal project.

Vulkan rendering under Unreal Engine 4.24 or older will require bind-mounting the X11 socket from the host system and propagating the `DISPLAY` environment variable so that output can be rendered to a window. See the section [Using the X11 images](#using-the-x11-images) for details on the required `docker run` flags.


## Audio output

By default, the container images are configured to spawn a PulseAudio server on demand when packaged Unreal projects initialise audio output. This allows the Unreal Engine to produce audio output inside the container which can then be captured (e.g. using Pixel Streaming for Linux.) However, this behaviour may be undesirable for use cases where the host system's X11 socket is bind-mounted and output is displayed on the host, since audio output will not be propagated alongside the rendered output. The `hostaudio` configuration of each image variant overrides this default behaviour and instructs the Unreal Engine to instead use a PulseAudio socket bind-mounted from the host system, thus allowing audio output to be heard on the host. To bind-mount the PulseAudio socket from the host system, use the following flag:

```bash
"-v/run/user/$UID/pulse:/run/user/1000/pulse"
```


## Using the X11 images

The `x11` configuration of each image variant extends the `hostaudio` configuration and adds the X11 libraries needed for running applications that create X11 windows. These images are designed for running containers locally and displaying the output of a packaged Unreal project directly on the host system's display.

To run a container using an X11-enabled image, the Docker host system will need to be running an X11 server and you will need to bind-mount the host's X11 socket inside the container like so:

```bash
# Replace "adamrehn/ue4-runtime:x11" with your chosen image tag
docker run --gpus=all -v/tmp/.X11-unix:/tmp/.X11-unix:rw -e DISPLAY adamrehn/ue4-runtime:x11 bash
```

If you want audio output then you will need to bind-mount the host system's PulseAudio socket as well:

```bash
# Replace "adamrehn/ue4-runtime:x11" with your chosen image tag
docker run --gpus=all -v/tmp/.X11-unix:/tmp/.X11-unix:rw "-v/run/user/$UID/pulse:/run/user/1000/pulse" -e DISPLAY adamrehn/ue4-runtime:x11 bash
```


## Building the images from source

Building the container images from source requires Python 3.5 or newer and the dependency packages listed in [requirements.txt](https://github.com/adamrehn/ue4-runtime/blob/master/requirements.txt).

To build the images, simply run `build.py`. This will automatically query Docker Hub to retrieve the list of available [nvidia/cuda](https://hub.docker.com/r/nvidia/cuda) base images based on Ubuntu LTS releases and build all variants of the `adamrehn/ue4-runtime` image accordingly.


## Legal

Copyright &copy; 2019 - 2023, Adam Rehn. Licensed under the MIT License, see the file [LICENSE](https://github.com/adamrehn/ue4-runtime/blob/master/LICENSE) for details.

The file [pulseaudio-default.pa](./base/pulseaudio-default.pa) is adapted from the [default PulseAudio configuration data](https://github.com/pulseaudio/pulseaudio/blob/v12.2/src/daemon/default.pa.in), which is part of PulseAudio and is licensed under the [GNU Lesser General Public License version 2.1 or newer](https://github.com/pulseaudio/pulseaudio/blob/master/LGPL).
