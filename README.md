# lol_analytics

Predicts what team will win a specific League of Legends game.

## Source code structure

./src/analytics
./src/client: In progress. Client for an android device.
./src/cloud: In progress. Spin up a server using AWS and lambda.

## Analytics

Uses a makefile for starting the pipeline.
Read the README.md inside the folder.
For storing files, initially Mongodb was used, but there were some
perfomance issues. As a workaround, files are being stored in locally mounted server.
Check out init.sh script.

The input of the pipeline is a hand-made pseudolanguage for describing what markers the app should take into account. See markers.ini.
There are still performance issues that should be addressed, since the whole thing runs like an interpreted language.
The pipeline yields a neural network model used for classifying data automatically.
More on this on the README.md of analytics.

## Client

In progress. Client for the service using Angular.

## Cloud

In progress. Script for deploying the server. Ideally, should be done with Terraform.
