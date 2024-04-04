import requests, subprocess, os, dotenv

dotenv.load_dotenv()

webhook_url = os.getenv('WEBHOOK')
fqdn=os.uname()[1]

# def update_package_list():
#     """Updates the package lists for available packages."""
#     command = "sudo apt update -qqq >/dev/null 2>&1"
#     os.system(command)

def update_package_list():
    """Updates the package lists for available packages."""
    output = subprocess.check_output(["apt", "update", "-qqq"], text=True)


def check_for_updates():
    """Checks for available Debian package updates and returns a list of those with new versions."""
    output = subprocess.check_output(["apt", "list", "--upgradable"], text=True)
    updates = []
    for line in output.splitlines():
        if line.startswith(line):
            updates.append(line)
            # updates.append(line.split()[0])
    return updates

def send_update_message(update_list):
  """Sends a message containing the list of updates to the Discord channel."""
  message = "Available Updates: on " "**" + fqdn + "**" + "\n" + "\n".join(update_list)
  data = {"content": message}
  response = requests.post(webhook_url, json=data)
  if not response.status_code == 204:
      print(f"Error sending message: {response.status_code}")


if __name__ == "__main__":
    update_package_list()  # Update package lists first
    available_updates = check_for_updates()
    if available_updates:
        update_list = check_for_updates()  # Replace with your function call
        send_update_message(update_list)
        # print("The following packages have updates available:")
        # for package in available_updates:
        #     print(package)
