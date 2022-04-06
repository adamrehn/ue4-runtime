ARG BASEIMAGE
FROM ${BASEIMAGE}

# This Dockerfile is adapted from NVIDIA's VirtualGL + TurboVNC sample:
# <https://gitlab.com/nvidia/samples/blob/master/opengl/ubuntu16.04/turbovnc-virtualgl/Dockerfile>)

# Install the dependencies for VirtualGL
USER root
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
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
		xkb-data

# Install VirtualGL
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES},display
ARG VIRTUALGL_VERSION=2.6.1
RUN cd /tmp && \
	curl -fsSL -O https://sourceforge.net/projects/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb && \
	dpkg -i *.deb && \
	rm -f /tmp/*.deb
USER ue4
