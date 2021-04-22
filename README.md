<p align="center">
  <a href="https://github.com/RazKissos/SeniorBot">
    <img src="https://cdn.discordapp.com/attachments/591367551892586635/809507213365608494/LogoWithBorder.png" alt="Logo" width="280" height="280">
  </a>
</p>

<p align="center">
  <a href="https://github.com/RazKissos/SeniorBot">
    <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username=razkissos&repo=seniorbot&theme=dracula" />
  </a>
</p>

# SeniorBot

## Table of Contents

* [About](#about)
* [Installation](#installation-and-setup)
* [Config](#config)
  * [The Config File](#the-config-file)


## About
**Created by Raz Kissos**
### v1.0.0 released at 6/13/2020.
### A Discord bot made using the discord.py python module.

This was my first shot at creating a full fledged [discord](https://discord.com) bot.
I implemented some basic functions (kick, mute, delete messages, etc...)
>NOTE: Bot is online 24/7. You can add SeniorBot to your server via this link: https://bit.ly/3jG5SwM. if you do add it make sure to place his role at the top so he can manage things correctly with no errors.

****

## Installation And Setup
The bot works on any platform that has python 3 installed and `discord.py` configured correctly.  
Here is the installation guide for all operating systems that have git:

1. First, `clone` the repository:
```sh
git clone "https://github.com/RazKissos/SeniorBot.git"
```

2. After cloning, step into the folder and create a `botconfig.cfg` file, the bot will receive it's token and prefix from this file.
> NOTE: you can learn more about this by reading below or clicking [this link](#config).

3. When you have selected all your bot's credentials you should make sure python3 is installed: [python](https://www.python.org/downloads/)

4. After installing python use the pip command and give it the `requirements.txt` file included with the repository:
```sh
python pip install -r requirements.txt
```
> NOTE: make sure you are doing this in the main folder to ensure you are specifying the correct requirements.txt file path. Please also note that in some linux distributions `python` would be replaced with `python3`, please make sure to check which one is correct for you.

5. After all required modules have been installed you can finally run the bot by typing:
```sh
python SeniorBot.py
```
> NOTE: the bot will always run in a seperate window. if you wish to run it as a process you can use nohup which only works on linux, if you want windows solutions you will have to find them on your own.

## Config
### The Config File:
The bot receives all of it's data from the config file (Token, Prefix). In order to create this file just copy this format and paste your correct information in the corresponding place.
```cfg
[data]
token = **<your bot token>**
prefix = **<your bot prefix>**
```
>NOTE: place the config file in the folder you run your bot file in. Also make sure you `pip install` each and every module used in the code to avoid errors!

## If you need any help I will be happy to supply it.
