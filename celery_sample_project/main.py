from flask import Flask, request, render_template
from tasks import *
from celery import group, chain, chord

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/transcode360p', methods=['POST'])
def transcodeTo360p():
    if request.method == 'POST':
        transcode_360p.apply_async(queue='tasks', priority=1)
        return 'Video is getting transcoded to 360p dimensions!'
    else:
        return 'ERROR: Wrong HTTP Method'


@app.route('/transcode480p', methods=['POST'])
def transcodeTo480p():
    if request.method == 'POST':
        transcode_480p.apply_async(queue='tasks', priority=2)
        return 'Video is getting transcoded to 480p dimensions!'
    else:
        return 'ERROR: Wrong HTTP Method'


@app.route('/transcode720p', methods=['POST'])
def transcodeTo720p():
    if request.method == 'POST':
        transcode_720p.apply_async(queue='tasks', priority=3)
        return 'Video is getting transcoded to 720p dimensions!'
    else:
        return 'ERROR: Wrong HTTP Method'


@app.route('/transcode1080p', methods=['POST'])
def transcodeTo1080p():
    if request.method == 'POST':
        transcode_1080p.apply_async(queue='tasks', priority=4)
        return 'Video is getting transcoded to 1080p dimensions!'
    else:
        return 'ERROR: Wrong HTTP Method'


@app.route('/transcodeALL', methods=['POST'])
def transcodeToALL():
    if request.method == 'POST':
        # We will do something like this to simulate actual processing of a video
        transcoding_tasks = group(
            transcode_1080p.signature(queue='tasks', priority=1, immutable=True),
            transcode_720p.signature(queue='tasks', priority=2, immutable=True),
            transcode_480p.signature(queue='tasks', priority=3, immutable=True),
            transcode_360p.signature(queue='tasks', priority=4, immutable=True)
        )
        chord(transcoding_tasks)(end_processing.signature(queue='tasks', immutable=True))
        return 'Video is getting transcoded to all dimensions!'
    else:
        return 'ERROR: Wrong HTTP Method'


@app.route('/transcodeMANY', methods=['POST'])
def transcodeToMany():
    for i in range(int(request.args['numOfVids'])):
        # Real time scenario
        
        transcoding_tasks = group(
            transcode_1080p.signature(queue='tasks', priority=1, immutable=True),
            transcode_720p.signature(queue='tasks', priority=2, immutable=True),
            transcode_480p.signature(queue='tasks', priority=3, immutable=True),
            transcode_360p.signature(queue='tasks', priority=4, immutable=True)
        )
        
        # Removing initial common_setup
        # chord works fine with priorities but not chain :(
        # hence -
        chord(transcoding_tasks)(end_processing.signature(queue='tasks', immutable=True))

    return(str(request.args['numOfVids']) + ' video(s) being transcoded to all dimensions!')


if __name__ == "__main__":
    app.run(debug=True)
