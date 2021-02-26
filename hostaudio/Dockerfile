ARG BASEIMAGE
FROM ${BASEIMAGE}

# Install the PulseAudio command line tools package (client only, no server)
USER root
RUN apt-get update && \
	apt-get install -y --no-install-recommends pulseaudio-utils && \
	rm -rf /var/lib/apt/lists/*
USER ue4

# Configure the PulseAudio client to connect to the host system's server using a bind-mounted UNIX socket
COPY pulseaudio-client.conf /etc/pulse/client.conf
