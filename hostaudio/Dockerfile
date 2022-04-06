ARG BASEIMAGE
FROM ${BASEIMAGE}

# Install the PulseAudio command line tools package (client only, no server)
USER root
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends pulseaudio-utils
USER ue4

# Configure the PulseAudio client to connect to the host system's server using a bind-mounted UNIX socket
COPY pulseaudio-client.conf /etc/pulse/client.conf

# Instruct the Unreal Engine to use the SDL audio driver for PulseAudio
# (This will prevent SDL from attempting to try other audio drivers if PulseAudio fails to initialise)
ENV SDL_AUDIODRIVER pulse
