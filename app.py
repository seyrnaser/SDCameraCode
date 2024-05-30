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

@app.route('/camera2')
def camera2():
    return render_template('camera2.html')

@app.route('/camera3')
def camera3():
    return render_template('camera3.html')

@app.route('/camera4')
def camera4():  # Corrected function name here
    return render_template('camera4.html')

@app.route('/view-all')
def view_all_cameras():
    return render_template('view_all.html')

@app.route('/start-streams', methods=['POST'])
def start_streams():
    script_path = "/home/seyr/Desktop/start_camera1.py"
    python_env_path = "/home/seyr/myprojectenv/bin/python3"
    try:
        # Start the RTSP stream script for Camera 1
        subprocess.Popen([python_env_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Prepare and run the ffmpeg command for Camera 1 in a new terminal
        ffmpeg_command1 = "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.250:8554/stream1 -codec copy -bsf:v h264_mp4toannexb -hls_time 2 -hls_list_size 30 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera1/index.m3u8"
        subprocess.Popen(['xterm', '-e', ffmpeg_command1])
       
        # FFMPEG commands for each camera
        commands = [
            "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.252:8554/unicast -codec copy -bsf:v h264_mp4toannexb -hls_time 2 -hls_list_size 30 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera2/index.m3u8",
            "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.253:8554/unicast -codec copy -bsf:v h264_mp4toannexb -hls_time 2 -hls_list_size 30 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera3/index.m3u8",
            "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.254:8554/unicast -codec copy -bsf:v h264_mp4toannexb -hls_time 2 -hls_list_size 30 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera4/index.m3u8"
        ]

        # Run FFMPEG command for each camera in a new terminal window
        for cmd in commands:
            subprocess.Popen(['xterm', '-e', cmd])
        return jsonify({'success': True, 'message': 'Streams started successfully in new terminals.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to start the streams.', 'error': str(e)})

@app.route('/reset-hls', methods=['POST'])
def reset_hls():
    try:
        # Kill all running ffmpeg processes
        kill_command = 'sudo pkill -9 ffmpeg'
        subprocess.run(kill_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Remove all HLS residues
        subprocess.run('sudo rm /var/www/html/hls/*/*.m3u8 /var/www/html/hls/*/*.ts', shell=True, check=True)
        return jsonify({'success': True, 'message': 'All streams reset successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'message': 'Failed to reset streams.', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
