import paramiko

# Create SSH client instance
ssh_client = paramiko.SSHClient()

# Set policy to automatically add new host keys
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Connect to Raspberry Pi
ssh_client.connect(hostname='10.0.32.250', username='sdconfig', password='password')
print("SSH connection established successfully.")

# Execute commands
command = (
    'cd ~/myenv; source bin/activate; '
    'cd ~/Desktop; sudo ~/myenv/bin/python3 test.py; '
    'rpicam-vid -t 0 --height 1080 --width 1080 --inline -o - | cvlc stream:///dev/stdin --sout \'#rtp{sdp=rtsp://:8554/stream1}\' :demux=h264'
)
stdin, stdout, stderr = ssh_client.exec_command(command)

# Print output
print(stdout.read().decode())





