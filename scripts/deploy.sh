#!/bin/sh

DIR=`dirname "$0"`
HOST="garage.local"

rsync -av $DIR/../ $HOST:~/garage_bot
ssh $HOST "bash -s" << EOF
  cd ~/garage_bot &&
  sudo python3 setup.py install && \
  sudo systemctl restart garage_bot
EOF

