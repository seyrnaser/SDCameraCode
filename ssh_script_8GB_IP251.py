import paramiko

# Create SSH client instance
ssh_client = paramiko.SSHClient()

# Set policy to automatically add new host keys
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to Raspberry Pi
    ssh_client.connect(hostname='10.0.32.251', username='sdconfig', password='password')
    print("SSH connection established successfully.")
    
    # Execute commands for Camera 2, adjusting to use 'rpicam-vid'
    command = (
        'cd ~/myenv; source bin/activate; '
        'cd ~/Desktop; sudo ~/myenv/bin/python3 test.py;'
        # Adjusted to use 'rpicam-vid' and specifying '/stream2' for Camera 2 on port 8554
        'rpicam-vid -t 0 --height 1080 --width 1080 --inline -o - | cvlc stream:///dev/stdin --sout \'#rtp{sdp=rtsp://:8554/stream1}\' :demux=h264'
    )
    stdin, stdout, stderr = ssh_client.exec_command(command)
    
    # Print output
    output = stdout.read().decode()
    print(output)
    if output == "":
        # If there's no output, print any errors
        print(stderr.read().decode())
    
except Exception as e:
    print("Error:", e)


