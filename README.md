# Odoo Project Setup Guide

## Getting Started
First, let's make sure you have everything you need:

## Prerequisites
- Docker and Docker Compose installed on your machine.

## Installation
1. Copy the sample configuration file to get started with the default settings:
```shell
cp config/odoo.conf.sample config/odoo.conf
```
2. Use Docker Compose to run your Odoo instance:
```shell
docker compose up
```
3. Open your browser and go to http://localhost:9001 to access the Odoo web interface.

## Initial Setup
1. Fill in the database creation form. Do not check the demo data option.
2. Take note of the "Email" and "Password" you use; these will be your admin login credentials.
   > **Note:** If you encounter a `Database creation error` stating that the database already exists, simply ignore it. Click on the existing database name shown under the error message to proceed.
3. Log in using the email and password you set during the database creation.

## Configuring Odoo
1. Navigate to `Apps` and search for the `Website` app.
2. Click `Activate` to install the Website app.
3. Click on the menu icon in the top left corner and select `Settings`.
4. Navigate to `General settings` > `Developer Tools` and activate the developer mode.
5. Ensure the addons_path parameter in `config/odoo.conf` includes `/mnt/extra-addons`.
6. Go to `Apps` and click on `Update apps list`. 
7. Clear the search prompt, search for `Custom file manager`, and install it.
8. Click on the menu icon in the top left corner and navigate to `File manager`.

Congratulations! You have successfully set up your Odoo instance. Explore the vast features and capabilities of Odoo to tailor it to your business needs.