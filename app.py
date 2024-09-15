from flask import Flask, jsonify, request
import subprocess
import os
import time
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/download-audio')
def download_audio():
    url = request.args.get('url')
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
def download_video():
    url = request.args.get('url')
    output = subprocess.run('yt-dlp -o "/tmp/%(title)s.%(ext)s" ' + url, shell=True, capture_output=True)
    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')

    filesize = get_size('/tmp')

    return jsonify({
        'stdout': stdout,
        'stderr': stderr,
        'filesize': filesize
    })

@app.route('/transcribe-video')
def transcribe():
    files = os.listdir('/app')
    for file in files:
        if file.endswith('.webm'):
            start = time.time()
            cmd = 'ffmpeg -i ' + file + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 /tmp/audio.wav'
            print(cmd)
            output = subprocess.run('ffmpeg -i ' + file + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 /tmp/audio.wav', shell=True, capture_output=True)
            print(f"Transcription time: {time.time() - start} seconds")
            stdout = output.stdout.decode('utf-8')
            stderr = output.stderr.decode('utf-8')

            # get file size
            filesize = get_size('/tmp')

            # get audio info
            audio_info = subprocess.run('ffprobe -i /tmp/audio.wav -show_streams -select_streams a:0', shell=True, capture_output=True)
            audio_info_stdout = audio_info.stdout.decode('utf-8')
            audio_info_stderr = audio_info.stderr.decode('utf-8')


            return jsonify({
                'stdout': stdout,
                'stderr': stderr,
                'transcription_time': time.time() - start,
                'filesize': filesize,
                'audio_info': audio_info_stdout,
                'audio_info_stderr': audio_info_stderr,
            })
        

@app.route('/transcribe-video-mp4')
def transcribe_mp4():
    files = os.listdir('/app')
    for file in files:
        if file.endswith('.webm'):
            start = time.time()
            cmd = 'ffmpeg -i ' + file + ' -c:v copy -an /tmp/video.mp4'
            print(cmd)
            output = subprocess.run('ffmpeg -i ' + file + ' -c:v copy -an /tmp/video.mp4', shell=True, capture_output=True)
            print(f"Transcription time: {time.time() - start} seconds")
            stdout = output.stdout.decode('utf-8')
            stderr = output.stderr.decode('utf-8')

            # get file size
            filesize = get_size('/tmp')

            # get audio info
            audio_info = subprocess.run('ffprobe -i /tmp/video.mp4 -show_streams -select_streams a:0', shell=True, capture_output=True)
            audio_info_stdout = audio_info.stdout.decode('utf-8')
            audio_info_stderr = audio_info.stderr.decode('utf-8')


            return jsonify({
                'stdout': stdout,
                'stderr': stderr,
                'transcription_time': time.time() - start,
                'filesize': filesize,
                'audio_info': audio_info_stdout,
                'audio_info_stderr': audio_info_stderr,
            })
        

def download_file(url):
    local_filename = url.split('/')[-1]
    local_filename = os.path.join('/tmp', local_filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    print("filename", local_filename)
    return local_filename

@app.route('/transcribe-video-avi')
def transcribe_avi():
    # download video

    start = time.time()
    download_file("https://cdn.leapcell.io/static-files/filename.avi")
    print(f"Download time: {time.time() - start} seconds")

    files = os.listdir('/tmp')
    for file in files:
        if file.endswith('.avi'):
            file = os.path.join('/tmp', file)
            start = time.time()
            cmd = 'ffmpeg -i ' + file + ' -c:v copy -an /tmp/video_avi.mp4'
            print(cmd)
            output = subprocess.run('ffmpeg -i ' + file + ' -c:v copy -an /tmp/video_avi.mp4', shell=True, capture_output=True)
            print(f"Transcription time: {time.time() - start} seconds")
            stdout = output.stdout.decode('utf-8')
            stderr = output.stderr.decode('utf-8')

            # get file size
            filesize = get_size('/tmp')

            # get audio info
            audio_info = subprocess.run('ffprobe -i /tmp/video_avi.mp4 -show_streams -select_streams a:0', shell=True, capture_output=True)
            audio_info_stdout = audio_info.stdout.decode('utf-8')
            audio_info_stderr = audio_info.stderr.decode('utf-8')


            return jsonify({
                'stdout': stdout,
                'stderr': stderr,
                'transcription_time': time.time() - start,
                'filesize': filesize,
                'audio_info': audio_info_stdout,
                'audio_info_stderr': audio_info_stderr,
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
                             