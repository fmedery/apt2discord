# apt2discord

A lightweight Python script that monitors APT package updates and sends notifications to Discord via webhooks. Designed for automated running via cron.

> ⚠️ **Important**: This tool only works on Debian-based systems (Debian, Ubuntu, Linux Mint, etc.) as it relies on the APT package manager. It will not work on non-Debian based distributions like Fedora, RHEL, Arch Linux, etc.

## Features
- Automatic package list updates using `apt update`
- Detection of available package upgrades
- Discord notifications including:
  - Server hostname
  - Timestamp
  - Number of upgradeable packages
  - Detailed package list
- Silent operation mode for cron jobs
- Configurable via command line arguments or environment variables
- Error handling and logging

## Requirements
- Debian-based Linux distribution
- Python 3.6+
- `requests` library
- Root/sudo access (for apt commands)
- Discord webhook URL

## Installation

### Option 1: Pre-built Binaries (Recommended)

Download the appropriate binary for your system architecture from the [Releases page](https://github.com/fmedery/apt2discord/releases):

- `apt2discord-x86_64`: For 64-bit x86 systems
- `apt2discord-arm64`: For ARM64 systems

### Option 2: From Source
```bash
# Clone the repository
git clone https://github.com/fmedery/apt2discord.git
cd apt2discord

# Install dependencies
pip install requests

# Optional: Build binary
pip install pyinstaller
pyinstaller --name apt2discord --onefile apt2discord.py
```

## Usage

### Command Line Arguments
```bash
# Using webhook argument
./apt2discord --webhook YOUR_WEBHOOK_URL

# Show help
./apt2discord --help
```

### Environment Variable
```bash
# Set webhook URL
export WEBHOOK=YOUR_WEBHOOK_URL

# Run script
./apt2discord
```

### Example Output
Discord message format:
```
🔄 Available Updates on hostname at 2024-03-21 08:00:00
Found 3 package(s) to update:
nginx/stable 1.24.0-1
python3.11/stable 3.11.8-1
openssh-server/stable 9.4p1-1
```

### Cron Setup
Add to crontab (`crontab -e`):
```bash
# Daily at 8 AM using webhook argument
0 8 * * * /path/to/apt2discord --webhook YOUR_WEBHOOK_URL >/dev/null 2>&1

# OR using environment variable
0 8 * * * WEBHOOK=YOUR_WEBHOOK_URL /path/to/apt2discord >/dev/null 2>&1
```

## Development

### Building New Release
```bash
# Create and push new tag
git tag v1.x.x
git push origin v1.x.x
```
This triggers GitHub Actions to:
- Build x86_64 and ARM64 binaries
- Create release with binaries
- Generate release notes

### Error Handling
- Script uses WARNING level logging
- Only errors and warnings are logged
- Check system logs (`/var/log/syslog` or `/var/log/messages`) for issues

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License
MIT License