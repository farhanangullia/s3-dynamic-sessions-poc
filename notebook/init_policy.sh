#!/bin/bash

echo "Retrieving session tokens"
tokens=$(curl <INVOKE_URL>)
echo "Exporting credentials to env variables..."
export AWS_ACCESS_KEY_ID=$(echo $tokens | jq -r .AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(echo $tokens | jq -r .SecretAccessKey)
export AWS_SESSION_TOKEN=$(echo $tokens | jq -r .SessionToken)
echo "Successfully exported credentials..."