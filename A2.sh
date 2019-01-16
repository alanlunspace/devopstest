# /usr/bin/env bash
HOME_DIR=/home/ec2-user
WORK_DIR=/home/ec2-user/devopstest
mkdir -p ${HOME_DIR}
cd ${HOME_DIR}
sudo yum install git python3 -y
git clone https://github.com/alanlunspace/devopstest.git
cd ${WORK_DIR}
sudo pip3 install Flask
sudo pip3 install requests

# Replace your Slack Webhook URL in A2.py
python3 A2.py &
ssh -oStrictHostKeyChecking=no -R 80:localhost:5000 serveo.net

# Test GitHub webhook and wait for Slack message
