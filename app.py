from flask import Flask, render_template, jsonify, request
import subprocess
import shlex

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/camera1')
def camera1():
    return render_template('camera1.html')

@app.route('/start-streams', methods=['POST'])
def start_streams():
    script_path = "/home/seyr/Desktop/start_camera1.py"
    python_env_path = "/home/seyr/myprojectenv/bin/python3"
    try:
        # Start the RTSP stream script without waiting for its output
        subprocess.Popen([python_env_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Prepare the ffmpeg command to run in a new terminal
        ffmpeg_command = "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.250:8554/stream1 -codec copy -bsf:v h264_mp4toannexb -hls_time 2 -hls_list_size 30 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera1/index.m3u8"
        # Open a new terminal to run the ffmpeg command
        subprocess.Popen(['xterm', '-e', ffmpeg_command])
        return jsonify({'success': True, 'message': 'Stream started successfully in a new terminal.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to start the stream.', 'error': str(e)})

@app.route('/reset-hls', methods=['POST'])
def reset_hls():
    try:
        # First, kill all running ffmpeg processes to ensure no files are being written to during the cleanup
        kill_command = 'sudo pkill -9 ffmpeg'
        subprocess.run(kill_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Remove all HLS residues
        subprocess.run('sudo rm /var/www/html/hls/*/*.m3u8 /var/www/html/hls/*/*.ts', shell=True, check=True)
        return jsonify({'success': True, 'message': 'All streams reset successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'message': 'Failed to reset streams.', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
