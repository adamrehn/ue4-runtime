ARG BASEIMAGE
FROM ${BASEIMAGE}

# Instruct PulseAudio to connect to the host's server using a bind-mounted UNIX socket
COPY pulseaudio-client.conf /etc/pulse/client.conf
