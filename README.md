# Pod User App Report

## Overview
This Python script is built based on the [Symphony Python SDK](https://github.com/SymphonyPlatformSolutions/symphony-api-client-python)

The script will retrieve All Active Users from the pod.
For each user, it will retrieve list of installed app.

The script will produce one CSV file per app containing list of all the users who have got the app installed.

## Output Columns
The CSV file will contain following columns:
- User Name
- First Name
- Last Name
- Email
- App Subscription

The output file(s) will be saved in the root directory in format - ``App Name (app-id).csv``

## Environment Setup
This client is compatible with **Python 3.6 or above**

Create a virtual environment by executing the following command **(optional)**:
``python3 -m venv ./venv``

Activate the virtual environment **(optional)**:
``source ./venv/bin/activate``

Install dependencies required for this client by executing the command below.
``pip install -r requirements.txt``


## Getting Started
### 1 - Prepare the service account
The Python client operates using a [Symphony Service Account](https://support.symphony.com/hc/en-us/articles/360000720863-Create-a-new-service-account), which is a type of account that applications use to work with Symphony APIs. Please contact with Symphony Admin in your company to get the account.

The client currently supports two types of Service Account authentications, they are
[Client Certificates Authentication](https://symphony-developers.symphony.com/symphony-developer/docs/bot-authentication-workflow#section-authentication-using-client-certificates)
and [RSA Public/Private Key Pair Authentication](https://symphony-developers.symphony.com/symphony-developer/docs/rsa-bot-authentication-workflow).

**RSA Public/Private Key Pair** is the recommended authentication mechanism by Symphony, due to its robust security and simplicity.

**Important** - The service account must have **User Provisioning** role in order to work.

### 2 - Upload Service Account Private Key
Please copy the Service Account private key file (*.pem) to the **rsa** folder. You will need to configure this in the next step.

### 3 - Update resources/config.json

To run the bot, you will need to configure **config.json** provided in the **resources** directory. 

**Notes:**
Most of the time, the **port numbers** do not need to be changed.

You should replace **pod** with your actual Pod URL.

You also need to update based on the service account created above:
- botPrivateKeyPath (ends with a trailing "/"))
- botPrivateKeyName
- botUsername
- botEmailAddress

Sample:

    {
      "sessionAuthHost": "<pod>.symphony.com",
      "sessionAuthPort": 443,
      "keyAuthHost": "<pod>.symphony.com",
      "keyAuthPort": 443,
      "podHost": "<pod>.symphony.com",
      "podPort": 443,
      "agentHost": "<pod>.symphony.com",
      "agentPort": 443,
      "authType": "rsa",
      "botPrivateKeyPath":"./rsa/",
      "botPrivateKeyName": "bot-private-key.pem",
      "botCertPath": "",
      "botCertName": "",
      "botCertPassword": "",
      "botUsername": "<bot-user>",
      "botEmailAddress": "<bot-email>",
      "appCertPath": "",
      "appCertName": "",
      "appCertPassword": "",
      "authTokenRefreshPeriod": "30",
      "proxyURL": "",
      "proxyUsername": "",
      "proxyPassword": "",
      "podProxyURL": "",
      "podProxyUsername": "",
      "podProxyPassword": "",
      "agentProxyURL": "",
      "agentProxyUsername": "",
      "agentProxyPassword": "",
      "keyManagerProxyURL": "",
      "keyManagerProxyUsername": "",
      "keyManagerProxyPassword": "",
      "truststorePath": ""
    }

### 4 - Run script
The script can be executed by running
``python3 main.py`` 



# Release Notes

## 0.1
- Initial Release

