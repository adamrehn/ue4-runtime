ARG BASEIMAGE
FROM ${BASEIMAGE}

# Install the X11 runtime libraries so we can display the output of Unreal Engine projects on the host system's display
USER root
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends \
		libfontconfig1 \
		libfreetype6 \
		libglu1 \
		libsm6 \
		libxcomposite1 \
		libxcursor1 \
		libxdamage1 \
		libxi6 \
		libxkbcommon-x11-0 \
		libxrandr2 \
		libxrender1 \
		libxss1 \
		libxtst6 \
		libxv1 \
		x11-xkb-utils \
		xauth \
		xfonts-base \
		xkb-data
USER ue4
