from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .main import addQuestion, addTitleToVideo, getOptTitle, getSuggestion, getTopic, generateVideo, applySuggestion

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return redirect(url_for('main.input'))

@bp.route('/input')
def input():
    return render_template('input.html')

@bp.route('/api', methods=['POST'])
def api():
    topic = request.form['q']
    generateVideo(topic, 2)
    return redirect(url_for('main.video'))

@bp.route('/video')
def video():
    video_url = url_for('static',filename='videos/video.mp4')
    optTitle = getOptTitle()
    topic = getTopic()
    sug = getSuggestion()
    return render_template('videoPlayer.html', video_url=video_url, topic=topic,optTitle = optTitle, suggestion= sug )

@bp.route('/addQuestiones', methods=['POST'])
def addQuestiones():
    video_url = "new URL"
    addQuestion()
    return jsonify(new_url=video_url)

@bp.route('/addTitle', methods=['POST'])
def addTitle():
    addTitleToVideo()
    return jsonify()

@bp.route('/addSug', methods=['POST'])
def addSug():
    applySuggestion()
    sug = getSuggestion()
    return jsonify(new_sug=sug)