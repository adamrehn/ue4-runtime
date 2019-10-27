ARG BASEIMAGE
FROM adamrehn/ue4-runtime:${BASEIMAGE}-cudagl10.0

# Ensure we are using a UTF-8 locale, as per the official TensorFlow Dockerfiles
ENV LANG C.UTF-8

# Install the TensorFlow dependencies not provided by the base image
# (Adapted from <https://github.com/tensorflow/tensorflow/blob/v1.13.1/tensorflow/tools/dockerfiles/dockerfiles/gpu.Dockerfile>)
USER root
RUN distro=$(bash -c 'distro=$(. /etc/os-release;echo $VERSION_ID); echo ${distro/./}') && \
	apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	libcudnn7=7.4.1.5-1+cuda10.0 \
	libfreetype6-dev \
	libhdf5-serial-dev \
	libpng-dev \
	libzmq3-dev \
	"nvinfer-runtime-trt-repo-ubuntu${distro}-5.0.2-ga-cuda10.0" \
	pkg-config \
	python3 \
	python3-pip \
	software-properties-common \
	unzip && \
	apt-get update && apt-get install -y --no-install-recommends libnvinfer5=5.0.2-1+cuda10.0 && \
rm -rf /var/lib/apt/lists/*

# Install the GPU-enabled version of TensorFlow
# (We split this into two calls to pip to avoid erroring out with "No module named 'setuptools'")
RUN pip3 install setuptools wheel && pip3 install tensorflow-gpu==1.13.1 

# Revert to our non-root user
USER ue4
