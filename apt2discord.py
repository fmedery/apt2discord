import requests
import subprocess
import os
import datetime
import logging
import argparse
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def update_package_list() -> None:
    """Updates the package lists for available packages."""
    try:
        subprocess.run(["apt", "update"], 
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL, 
                      check=True,
                      text=True)
        logger.debug("Package list updated successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to update package list: {e}")
        raise

def check_for_updates() -> List[str]:
    """Checks for available Debian package updates.
    
    Returns:
        List[str]: List of package names with available updates
    """
    try:
        output = subprocess.check_output(
            ["apt", "list", "--upgradable"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, 
            text=True
        )
        updates = [
            line.split()[0] for line in output.splitlines() 
            if not line.startswith("Listing...")
        ]
        logger.debug(f"Found {len(updates)} packages with available updates")
        return updates
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to check for updates: {e}")
        raise

def send_update_message(update_list: List[str], webhook_url: str) -> None:
    """Sends a message containing the list of updates to the Discord channel.
    
    Args:
        update_list (List[str]): List of package names with updates
        webhook_url (str): Discord webhook URL
    """
    fqdn = os.uname()[1]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = (
        f"🔄 Available Updates on **{fqdn}** at {timestamp}\n"
        f"Found {len(update_list)} package(s) to update:\n"
        f"```\n{chr(10).join(update_list)}```"
    )
    
    try:
        response = requests.post(webhook_url, json={"content": message})
        response.raise_for_status()
        logger.debug("Update message sent successfully to Discord")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to Discord: {e}")
        raise

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Check for system updates and send notifications to Discord.')
    parser.add_argument('--webhook', '-w',
                       help='Discord webhook URL. Can also be set via WEBHOOK environment variable.')
    return parser.parse_args()

def get_webhook_url(args) -> str:
    """Get webhook URL from command line args or environment variable.
    
    Args:
        args: Parsed command line arguments

    Returns:
        str: The webhook URL

    Raises:
        ValueError: If webhook URL is not provided via args or environment
    """
    webhook_url = args.webhook or os.getenv('WEBHOOK')
    if not webhook_url:
        logger.error("Webhook URL not provided. Use --webhook parameter or set WEBHOOK environment variable")
        raise ValueError("Webhook URL must be provided")
    return webhook_url

def main() -> None:
    """Main function to orchestrate the update check and notification process."""
    args = parse_args()
    
    try:
        webhook_url = get_webhook_url(args)
        update_package_list()
        available_updates = check_for_updates()
        
        if available_updates:
            send_update_message(available_updates, webhook_url)
        else:
            logger.info("No updates available")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
