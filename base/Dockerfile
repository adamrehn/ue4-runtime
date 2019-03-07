ARG BASEIMAGE
FROM ${BASEIMAGE}

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Enable PulseAudio support
RUN apt-get update && apt-get install -y --no-install-recommends pulseaudio-utils && \
	rm -rf /var/lib/apt/lists/*
COPY pulseaudio-client.conf /etc/pulse/client.conf

# Since UE4 refuses to run as the root user under Linux, create a non-root user
RUN useradd --create-home --home /home/ue4 --shell /bin/bash --uid 1000 ue4 && \
	usermod -a -G audio,video ue4
USER ue4
