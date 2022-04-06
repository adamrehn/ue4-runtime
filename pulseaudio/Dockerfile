ARG BASEIMAGE
FROM ${BASEIMAGE}

# Install the full PulseAudio package (client + server)
USER root
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
	apt-get update && apt-get install -y --no-install-recommends pulseaudio
USER ue4

# Configure the PulseAudio server to work correctly inside the container
COPY pulseaudio-client.conf /etc/pulse/client.conf
COPY pulseaudio-daemon.conf /etc/pulse/daemon.conf
COPY pulseaudio-default.pa /etc/pulse/default.pa

# Instruct the Unreal Engine to use the SDL audio driver for PulseAudio
# (This will prevent SDL from attempting to try other audio drivers if PulseAudio fails to initialise)
ENV SDL_AUDIODRIVER pulse
