#!/usr/bin/env bash

echo "Reading '.env' file for required environment variables"
if [ -f "./.env" ]; then
  source ./.env
else
  echo "Env variable not provided in '.env' file, set it up before running this script" >&2
fi

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
  sudo apt update && apt upgrade
}

install_package(){
  sudo apt install $1
}

update_sshd(){
  sed -i '' "s/$1/$2/' /etc/sshd_config"
  sed -i '' "s/# $1/$2/' /etc/sshd_config"
}


disable_root(){
  # Refer: https://www.naturalborncoder.com/2024/10/how-to-configure-ssh/
  update_sshd 'PermitRootLogin no' 'PermitRootLogin yes'
  update_sshd 'PasswordAuthentication no' 'PasswordAuthentication no'
  update_sshd 'UsePAM no' 'UsePAM yes'
  update_sshd 'KbdInteractiveAuthentication no' 'KbdInteractiveAuthentication yes'
}


install_all_pkg(){
  install_package ufw
  install_package tmux
  install_package fail2ban
  install_package net-tools
}

setup_fail2ban(){
  # Refer https://www.naturalborncoder.com/2024/10/installing-and-configuring-fail2ban/
  sudo systemctl enable --now fail2ban.service
}

setup_user(){
  sudo useradd -m $NEWUSER
  sudo usermod -aG sudo $NEWUSER
  echo $PASSWD | passwd --stdin $NEWUSER
}

validate_env
update_all
install_all_pkg
setup_fail2ban
