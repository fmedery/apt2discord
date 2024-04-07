import requests, subprocess, os, datetime

def update_package_list():
    """Updates the package lists for available packages."""
    output = subprocess.check_output(["apt", "update"], stderr=subprocess.DEVNULL, text=True) # Capture as text

def check_for_updates():
    """Checks for available Debian package updates and returns a list of those with new versions."""
    output = subprocess.check_output(["apt", "list", "--upgradable"], stderr=subprocess.DEVNULL, text=True)
    updates = []
    for line in output.splitlines():
        if not line.startswith("Listing..."):
            updates.append(line)
            # updates.append(line.split()[0])
    return updates

def send_update_message(update_list):
    fqdn=os.uname()[1]
    """Sends a message containing the list of updates to the Discord channel."""
    message = "Available Updates: on " "**" + fqdn + "**" + "\n" + "\n".join(update_list)
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if not response.status_code == 204:
        print(f"Error sending message: {response.status_code}")

if __name__ == "__main__":
    webhook_url = os.getenv('WEBHOOK')
    
    current_date = datetime.datetime.now().strftime("%b %d %H:%M:%S")

    update_package_list()  # Update package lists first

    available_updates = check_for_updates()
    if available_updates:
        update_list = check_for_updates()  # Replace with your function call
        send_update_message(update_list)
