#!/usr/bin/env bash

setup_hatch(){
  local install_url='https://github.com/pypa/hatch/releases/download/hatch-v1.16.2/hatch-x86_64-unknown-linux-gnu.tar.gz'
  local outfilename='hatch-x86_64-unknown-linux-gnu.tar.gz'
  wget "$install_url"
  sudo tar -C /usr/bin/ -xzvf "$outfilename"
  rm "$outfilename"
}

setup_ssl(){
  sudo certbot --nginx --agree-tos --redirect --hsts --staple-ocsp --email antics-fade-raven@duck.com -d haridwar.geerivana.in
}
