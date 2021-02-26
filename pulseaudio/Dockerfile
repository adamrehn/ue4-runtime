ARG BASEIMAGE
FROM ${BASEIMAGE}

# Install the full PulseAudio package (client + server)
USER root
RUN apt-get update && \
	apt-get install -y --no-install-recommends pulseaudio && \
	rm -rf /var/lib/apt/lists/*
USER ue4

# Configure the PulseAudio server to work correctly inside the container
COPY pulseaudio-client.conf /etc/pulse/client.conf
COPY pulseaudio-daemon.conf /etc/pulse/daemon.conf
COPY pulseaudio-default.pa /etc/pulse/default.pa
