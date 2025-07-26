import os
import json
import logging
import tempfile
from flask import Flask, request, jsonify

from db import init_db, save_embedding, get_embedding_by_id
from embedding_service import extract_audio_features, compare_embeddings

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

init_db()

@app.route('/extract-embedding', methods=['POST'])
def extract_embedding():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    if not audio.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        return jsonify({'error': 'Supported formats: WAV, MP3, M4A, FLAC'}), 400

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_filename = temp_file.name
        audio.save(temp_filename)

    try:
        app.logger.info(f"Processing file: {temp_filename}")
        features = extract_audio_features(temp_filename)
        embedding = features.tolist()
        file_id = save_embedding(json.dumps(embedding))

        return jsonify({
            'file_id': file_id,
            'embedding': embedding,
            'feature_count': len(embedding)
        })

    except Exception as e:
        app.logger.error(f"Error processing audio: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


@app.route('/get-embedding/<int:file_id>', methods=['GET'])
def get_embedding(file_id):
    try:
        result = get_embedding_by_id(file_id)
        if not result:
            return jsonify({'error': 'Embedding not found'}), 404
        embedding, created_at = result
        return jsonify({
            'file_id': file_id,
            'embedding': json.loads(embedding),
            'created_at': created_at
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compare-voices', methods=['POST'])
def compare_voices():
    data = request.get_json()
    if 'embedding1' not in data or 'embedding2' not in data:
        return jsonify({'error': 'Both embedding1 and embedding2 required'}), 400

    try:
        result = compare_embeddings(data['embedding1'], data['embedding2'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'voice-embedding-api'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
