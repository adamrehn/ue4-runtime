ARG BASEIMAGE
FROM ${BASEIMAGE}

# This Dockerfile is adapted from NVIDIA's VirtualGL + TurboVNC sample:
# <https://gitlab.com/nvidia/samples/blob/master/opengl/ubuntu16.04/turbovnc-virtualgl/Dockerfile>)

# Install the dependencies for VirtualGL
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
	ca-certificates \
	curl \
	libfontconfig1 \
	libfreetype6 \
	libglu1 \
	libsm6 \
	libxcomposite1 \
	libxcursor1 \
	libxi6 \
	libxrandr2 \
	libxrender1 \
	libxss1 \
	libxv1 \
	x11-xkb-utils \
	xauth \
	xfonts-base \
	xkb-data && \
rm -rf /var/lib/apt/lists/*

# Install VirtualGL
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES},display
ARG VIRTUALGL_VERSION=2.6.1
RUN cd /tmp && \
	curl -fsSL -O https://svwh.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb && \
	dpkg -i *.deb && \
	rm -f /tmp/*.deb
USER ue4
