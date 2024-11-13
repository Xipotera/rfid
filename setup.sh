#!/usr/bin/env bash

##########################################################################
# Automated Installer Program
#
# Author: Mathieu Vie
#
##########################################################################

VENV_DIR="env"  # Define virtual environment path

start () {
  echo "############################################"
  echo "# Automated installer for project pi       #"
  echo "############################################"
  echo ""
}

# takes msg ($1) and status ($2) as args
end () {
  echo ""
  echo "############################################"
  echo "# Finished the setup script"
  echo "# Message: $1"
  echo "############################################"
  exit "$2"
}

# takes message ($1) and level ($2) as args
message () {
  echo "[$2] $1"
}

apt_install () {
  if ! apt update; then
    message "Unable to update APT." "ERROR"
    end "Check your Internet connection and try again." 1
  fi
  if ! apt install -y python3-pip python3-venv; then
    message "Failed to install python3-pip and python3-venv." "ERROR"
    end "Cannot proceed without these packages." 1
  fi
}

# Create and activate a Python virtual environment for installing packages
setup_virtualenv () {
  if [[ ! -d "$VENV_DIR" ]]; then
    message "Creating virtual environment at $VENV_DIR" "INFO"
    python3 -m venv "$VENV_DIR"
    if [[ $? -ne 0 ]]; then
      message "Failed to create a virtual environment." "ERROR"
      end "Could not set up the virtual environment." 1
    fi
  fi
  message "Virtual environment is set up at $VENV_DIR" "INFO"
}

# Install Python packages required for LCD and RFID within the virtual environment
pip_install () {
  # Source virtual environment for current shell session
  source "$VENV_DIR/bin/activate"
  pip install -r requirements.txt
  deactivate  # Deactivate environment after installations
}



############
# Main logic
start

# check again if user is root in case user is calling this script directly
if [[ "$(id -u)" -ne 0 ]]; then message "User is not root." 'ERROR'; end 'Re-run as root or append sudo.' 1; fi

trap "end 'Received a signal to stop.' 1" INT HUP TERM

message 'Installing packages via APT.' 'INFO'; apt_install

message "Setting up virtual environment for Python packages." 'INFO'; setup_virtualenv

message "Installing Python dependencies with pip in virtual environment." 'INFO'; pip_install

echo "#################################################################"
echo "# All finished! Press any key to REBOOT now or Ctrl+c to abort. #"
echo "#################################################################"

read -n1 -s; reboot now
