from flask import Flask, render_template, jsonify
import subprocess
import shlex

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/camera1')
def camera1():
    return render_template('camera1.html')

@app.route('/start-hls', methods=['POST'])
def start_hls():
    script_path = "/home/seyr/Desktop/start_camera1.py"
    python_env_path = "/home/seyr/myprojectenv/bin/python3"
    try:
        # Start the RTSP stream script without waiting for it to finish
        rtsp_process = subprocess.Popen([python_env_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Clear previous HLS files
        subprocess.run(['sudo', 'rm', '-rf', '/var/www/html/hls/camera1/*'], check=True)

        # Start the HLS conversion
        ffmpeg_command = "sudo /usr/bin/ffmpeg -i rtsp://10.0.32.250:8554/stream1 -codec copy -bsf:v h264_mp4toannexb -hls_time 10 -hls_list_size 0 -hls_flags delete_segments+append_list -f hls /var/www/html/hls/camera1/index.m3u8"
        ffmpeg_process = subprocess.Popen(shlex.split(ffmpeg_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return jsonify({'success': True, 'message': 'HLS stream started successfully.'})
    except Exception as e:  # Catching a general exception to handle unexpected errors
        return jsonify({'success': False, 'message': 'Failed to execute streaming commands.', 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
