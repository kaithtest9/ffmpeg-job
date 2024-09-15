from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/download-audio')
def download_audio(url):
    output = subprocess.run('yt-dlp -x --audio-format wav -o "/tmp/%(title)s.%(ext)s" ' + url, shell=True, capture_output=True)
    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')

    filesize = get_size('/tmp')

    return jsonify({
        'stdout': stdout,
        'stderr': stderr,
        'filesize': filesize,
    })

def get_size(start_path = '.'):
    file_size = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                file_size[fp] = os.path.getsize(fp)

    return file_size

@app.route('/download-video')
def download_video(url):
    output = subprocess.run('yt-dlp -o "/tmp/%(title)s.%(ext)s" ' + url, shell=True, capture_output=True)
    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')

    filesize = get_size('/tmp')

    return jsonify({
        'stdout': stdout,
        'stderr': stderr,
        'filesize': filesize
    })

@app.route('/transcript')
def transcript():
    url = request.args.get('url')
    output = subprocess.run('yt-dlp -x --audio-format wav -o "/tmp/%(title)s.%(ext)s" ' + url, shell=True, capture_output=True)
    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')
    return jsonify({
        'stdout': stdout,
        'stderr': stderr
    })

if __name__ == '__main__':
    app.run(debug=True)
                             