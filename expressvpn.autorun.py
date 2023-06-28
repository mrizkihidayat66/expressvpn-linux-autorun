import subprocess
import pexpect
import time
import logging
import sys

# My configuration
MY_PASSWD	= "" # Superuser password
MY_SERIAL	= "" # ExpressVPN serial key
MY_SERVER	= "" # Default server to connect

# Logger configuration
logging.basicConfig(filename='script.log', level=logging.INFO)

# Handle errors
def handle_error(error_message):
  logging.error(error_message)
  print("An error occurred: " + error_message)
  sys.exit(1)  # Exit with non-zero status on error

def run_script():
  # Restart ExpressVPN
  p = pexpect.spawn("su -c 'systemctl restart expressvpn'")
  p.maxread = 1000
  p.sendline(MY_PASSWD)
  p.expect(pexpect.EOF)

  p.wait()
  if p.exitstatus != 0:
    handle_error("Failed to restart ExpressVPN")
  print("Successfully restarted ExpressVPN.")
  p.close()

  time.sleep(8)  # Pause for 8 seconds

  # Activate ExpressVPN
  p = pexpect.spawn("expressvpn activate")
  p.maxread = 1000
  p.expect(bytes("Enter activation code: ", 'utf-8'))
  p.sendline(MY_SERIAL)
  print("Successfully entered the activation code.")


  while True:
    i = p.expect([
      b"Activating...",
      b"Activated",
      b"Help improve ExpressVPN: .*",
      b"Already activated\. Logout from your account \(y/N\)\? .*"
    ], timeout=500)
    if i == 0:
      pass
    elif i == 1:
      print("ExpressVPN successfully activated.")
      pass
    elif i == 2 or i == 3:
      p.sendline("n")
      print("Successfully denied sending statistical data.")
      break
    else:
      handle_error("An unexpected error has occurred.")
  p.expect(pexpect.EOF)

  p.wait()
  if p.exitstatus != 0:
    handle_error("Failed to activate ExpressVPN")
  p.close()

  time.sleep(2)  # Pause for 2 seconds

  # Set ExpressVPN preferences
  try:
    subprocess.run("expressvpn preferences set block_trackers false", shell=True, check=True)
    subprocess.run("expressvpn preferences set network_lock off", shell=True, check=True)
  except subprocess.CalledProcessError as e:
    handle_error("Failed to set ExpressVPN preferences: " + str(e))

  time.sleep(2)  # Pause for 2 seconds

  # Connect to selected server
  try:
    subprocess.run(["expressvpn", "connect", MY_SERVER], check=True)
  except subprocess.CalledProcessError as e:
    handle_error("Failed to connect to " + MY_SERVER + " server: " + str(e))

  sys.exit(0)  # Exit with status 0 on success

if __name__ == "__main__":
  if run_script():
    logging.info("Script executed successfully")
    print("Script executed successfully")
