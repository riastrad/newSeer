# @Author: Josh Erb <josh.erb>
# @Date:   24-Apr-2017 22:04
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 24-Apr-2017 22:04

# NOTE: all of these commands must be run from the 'Repos' directory

# Code to pull data down from AWS EC2 instance and store it locally
scp -i .aws/Data-Ingester.pem -r ubuntu@35.165.12.174:~/data ~/repos/newSeer

# Clean the data
cd newSeer
python3 driver/cleaner.py

# Load the data into a local db
python3 driver/dum.py
