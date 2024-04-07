# apt2discord

## info
Send the list of upgradeable debian packages available to discord using webhook

## Requirements
* discord wekhook
* pyevnv
* conf_file_location with the discord webhook
* sudo to run apt commands

## How-to
```sh
cd apt2discord

# setup python env
pyenv install 3.12.3
pyenv virtualenv 3.12.3 apt2discord
pyenv local apt2discord

# install depencies
pip install -r requirements.txt

#compile code
pyinstaller --onefile apt2discord.py
```

## Usage
```sh
# code need to be run as root
sudo dist/apt2discord conf_file_location
```
