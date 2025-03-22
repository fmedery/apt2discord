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
pyinstaller --name apt2discord --onefile apt2discord.py
```

## Usage
```sh
# code need to be run as root
sudo dist/apt2discord conf_file_location
```

## Installation

### Pre-built Binaries
Download the appropriate binary for your system architecture from the [Releases page](https://github.com/yourusername/apt2discord/releases):

- `apt2discord-x86_64`: For 64-bit x86 systems (most desktop/server computers)
- `apt2discord-arm64`: For ARM64 systems (like Raspberry Pi running 64-bit OS)
