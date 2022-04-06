#!/usr/bin/env bash

# Remove any PulseAudio files leftover from previous runs of the Unreal Engine
# (Without this, PulseAudio will hang on startup if a container is restarted without a sufficient shutdown grace period)
rm -rf ~/.config/pulse /tmp/pulse-*

# Run the entrypoint command specified via our command-line parameters
"$@"
