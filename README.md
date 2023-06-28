# expressvpn-linux-autorun
A simple script to automatically run and connect ExpressVPN linux every time the system boots.

Instructions for Use:
1. Create a directory for the scripts and navigate to it:
   ```
   $ mkdir ~/scripts && cd ~/scripts
   ```
2. Clone the repository:
   ```
   $ git clone https://github.com/mrizkihidayat66/expressvpn-linux-autorun.git
   ```
3. Move the script file and remove the unnecessary directory:
   ```
   $ mv expressvpn-linux-autorun/expressvpn.autorun.py expressvpn.autorun.py && rm -r -f expressvpn-linux-autorun
   ```
4. Make the script executable:
   ```
   $ chmod +x expressvpn.autorun.py
   ```
5. Edit the script file to make the necessary configuration changes:
   ```
   $ nano expressvpn.autorun.py
   ```
   - Change your superuser password, ExpressVPN license, and default location to connect.

6. Create a systemd service file:
   ```
   $ sudo nano /etc/systemd/system/expressvpn-autorun.service
   ```
   > [Unit]  
   > Description=ExpressVPN Auto Run  
   > After=network.target  
   >   
   > [Service]  
   > ExecStart=/usr/bin/python3 /home/\<user\>/scripts/expressvpn.autorun.py  
   > WorkingDirectory=/home/\<user\>/scripts  
   > User=\<user\>  
   > Group=\<user\>  
   > Restart=on-failure  
   > RestartSec=6  
   > SuccessExitStatus=0  
   >   
   > [Install]  
   > WantedBy=multi-user.target  

7. Enable the service to start on boot:
   ```
   $ sudo systemctl enable expressvpn-autorun.service
   ```
8. Start the service:
   ```
   $ sudo systemctl start expressvpn-autorun.service
   ```
That's it! ExpressVPN will now automatically run and connect every time your system boots.
