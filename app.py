from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Specify the directory to store uploaded videos and subtitles
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Endpoint to upload a video
@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(video_path)
    
    return jsonify({'message': 'Video uploaded successfully'}), 200

# Endpoint to add subtitles
@app.route('/add-subtitles', methods=['POST'])
def add_subtitles():
    video_filename = request.form.get('video_filename')
    subtitles = request.form.get('subtitles')

    subtitles_filename = f'subtitles_{video_filename}.txt'
    subtitles_path = os.path.join(app.config['UPLOAD_FOLDER'], subtitles_filename)

    with open(subtitles_path, 'w') as f:
        f.write(subtitles)
    
    return jsonify({'message': 'Subtitles added successfully'}), 200

# Endpoint to retrieve subtitles
@app.route('/get-subtitles/<video_filename>')
def get_subtitles(video_filename):
    subtitles_filename = f'subtitles_{video_filename}.txt'
    subtitles_path = os.path.join(app.config['UPLOAD_FOLDER'], subtitles_filename)

    if not os.path.exists(subtitles_path):
        return jsonify({'message': 'Subtitles not found'}), 404

    with open(subtitles_path, 'r') as f:
        subtitles = f.read()

    return jsonify({'subtitles': subtitles})

if __name__ == '__main__':
    app.run(debug=True)
