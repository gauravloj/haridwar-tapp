#!/usr/bin/env bash

def import_env_file(){
  echo "Reading '.env' file for required environment variables"
  if [ -f "./.env" ]; then
    source ./.env
  else
    echo "Env variable not provided in '.env' file, set it up before running this script" >&2
  fi
}

log_error(){
  echo "$1" >&2
}

validate_env(){
  isvalid="true"
  if [ -z "${NEWUSER+x}" ]; then
      log_error "Username not provided in 'NEWUSER' environment variable"
      isvalid="false"
  fi

  if [ -z "${PASSWD+x}" ]; then
      log_error "Password for new user is not available"
      isvalid="false"
  fi


  if [ "$isvalid" != "true" ]; then
      exit 1
  fi
}

update_all(){
  sudo apt update -y && sudo apt upgrade -y
}

install_package(){
  local package=$1
  if ! command -v $package /dev/null; then
      echo "Installing $package ..."
      sudo apt install -y $package
  else
      echo "$package is already installed."
  fi
}

update_sshd(){
  sudo sed -i '' "s/$1/$2/' /etc/sshd_config"
  sudo sed -i '' "s/# $1/$2/' /etc/sshd_config"
}


disable_root(){
  # Refer: https://www.naturalborncoder.com/2024/10/how-to-configure-ssh/
  update_sshd 'PermitRootLogin no' 'PermitRootLogin yes'
  update_sshd 'PasswordAuthentication no' 'PasswordAuthentication no'
  update_sshd 'UsePAM no' 'UsePAM yes'
  update_sshd 'KbdInteractiveAuthentication no' 'KbdInteractiveAuthentication yes'
}


install_all_pkg(){
  #  List of packages to install
  packages=(
    "ufw"
    "tmux"
    "fail2ban"
    "net-tools"
    "git"
    "nginx"
    "certbot"
    "python3-certbot-nginx"
    # Note: this might only be available on Debian
    # "gunicorn"
  )

  # Loop through the list of packages and install each one
  for package in "${packages[@]}"; do
    install_package "$package"
  done
}

setup_fail2ban(){
  # Refer https://www.naturalborncoder.com/2024/10/installing-and-configuring-fail2ban/
  sudo systemctl enable --now fail2ban.service
}

setup_user(){
  if id $NEWUSER &> /dev/null ;
  then
    echo "User $NEWUSER already exists" 
    return
  fi

  sudo useradd -m $NEWUSER
  sudo usermod -aG sudo $NEWUSER
  echo $PASSWD | sudo passwd --stdin $NEWUSER
}

import_env_file
validate_env
update_all
install_all_pkg
setup_fail2ban

