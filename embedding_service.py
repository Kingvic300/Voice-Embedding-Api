# embedding_service.py
import librosa
import numpy as np

def extract_audio_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=16000)
        features = []

        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features.extend(np.mean(mfccs, axis=1).tolist())
        features.extend(np.std(mfccs, axis=1).tolist())

        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

        features.append(float(np.mean(spectral_centroids)))
        features.append(float(np.std(spectral_centroids)))
        features.append(float(np.mean(spectral_rolloff)))
        features.append(float(np.std(spectral_rolloff)))
        features.extend(np.mean(spectral_contrast, axis=1).tolist())

        zcr = librosa.feature.zero_crossing_rate(y)
        features.append(float(np.mean(zcr)))
        features.append(float(np.std(zcr)))

        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features.extend(np.mean(chroma, axis=1).tolist())

        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        features.extend(np.mean(tonnetz, axis=1).tolist())

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features.append(float(tempo))

        return np.array(features, dtype=np.float32)

    except Exception as e:
        raise Exception(f"Feature extraction failed: {str(e)}")


def compare_embeddings(embedding1, embedding2):
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)

    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)

    similarity = dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
    euclidean_distance = np.linalg.norm(emb1 - emb2)

    return {
        'cosine_similarity': float(similarity),
        'euclidean_distance': float(euclidean_distance),
        'match_probability': float(max(0, similarity))
    }
