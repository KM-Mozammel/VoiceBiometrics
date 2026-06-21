import numpy as np
import os
import soundfile as sf
import librosa
from pydub import AudioSegment
import uuid

VOICE_DIR = os.path.join(os.getcwd(), "voice_input")
os.makedirs(VOICE_DIR, exist_ok=True)


def convert_to_wav(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        raise ValueError(f"Conversion failed: {e}")


def extract_features(file_path):
    try:
        wav_path = os.path.join(VOICE_DIR, f"{uuid.uuid4()}.wav")
        wav_path = convert_to_wav(file_path, wav_path)

        y, sr = sf.read(wav_path, dtype="float32")

        if len(y.shape) > 1:
            y = np.mean(y, axis=1)

    except Exception as e:
        raise ValueError(f"Audio loading failed: {e}")

    try:
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc, axis=1)

    except Exception as e:
        raise ValueError(f"MFCC extraction failed: {e}")


def compare_voices(file1_path, file2_path):
    f1 = extract_features(file1_path)
    f2 = extract_features(file2_path)

    distance = np.linalg.norm(f1 - f2)

    return {
        "distance": float(distance),
        "same_person": bool(distance < 50)
    }
    
def get_embedding(file_path):
    return extract_features(file_path)