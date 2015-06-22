#!/bin/bash
set -ef
sudo sh stop_fcgi.sh api.lemontu.com 
sudo sh install_fcgi.sh api.lemontu.com 
sudo sh start_fcgi.sh api.lemontu.com 
echo "done"
