ARG BASEIMAGE
FROM ${BASEIMAGE}

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Enable NVENC support for use by Unreal Engine plugins that depend on it (e.g. Pixel Streaming).
# Also enable CUDA support (even when not using a CUDA base image), since evidently some versions of UE assume `libcuda.so.1`
# always exists when using the NVIDIA proprietary GPU drivers, and will fail to initialise the Vulkan RHI if it is missing.
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES},compute,video

# Enable Vulkan support
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends libvulkan1 && \
	VULKAN_API_VERSION=`dpkg -s libvulkan1 | grep -oP 'Version: [0-9|\.]+' | grep -oP '[0-9|\.]+'` && \
	mkdir -p /etc/vulkan/icd.d/ && \
	echo \
	"{\
		\"file_format_version\" : \"1.0.0\",\
		\"ICD\": {\
			\"library_path\": \"libGLX_nvidia.so.0\",\
			\"api_version\" : \"${VULKAN_API_VERSION}\"\
		}\
	}" > /etc/vulkan/icd.d/nvidia_icd.json

# Install the `xdg-user-dir` tool so the Unreal Engine can use it to locate the user's Documents directory
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends xdg-user-dirs

# Since the Unreal Engine refuses to run as the root user under Linux, create a non-root user
RUN useradd --create-home --home /home/ue4 --shell /bin/bash --uid 1000 ue4 && \
	usermod -a -G audio,video ue4
USER ue4
