#!/bin/bash
rm -rf /home/python-site-packages
ln -sf "$PWD"/local-site-package-cache /home/python-site-packages
