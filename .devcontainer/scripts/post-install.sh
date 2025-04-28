#!/bin/bash
#
# These must be installed as a user and therefore need to be run
# after the container has been created.
#
echo "**********************************************************************"
echo "Setting up Docker user development environment..."
echo "**********************************************************************"

echo "Setting up registry.local..."
sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"

echo "Making git stop complaining about unsafe folders"
git config --global --add safe.directory /app

echo "Adding ~/.local/bin to PATH..."
echo 'export PATH=$PATH:/home/vscode/.local/bin' >> $HOME/.bashrc

echo "**********************************************************************"
echo "Setup complete"
echo "**********************************************************************"
