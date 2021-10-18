import sys
import python_speech_features as psf
from scipy.io.wavfile import read
import numpy as np
import pickle


def get_mfcc(filepath):
    samplerate, signal = read(filepath)
    MFCCs = psf.mfcc(signal, samplerate, 0.025, 0.01, 26, appendEnergy = False)
    mean_mfcc = np.mean(MFCCs, axis=0)
    return mean_mfcc


def main(filepath):
    gender_map = {0: "male", 1: "female"}
    model_path = "GaussianNB.sav"
    model = pickle.load(open(model_path, 'rb'))
    mfcc = get_mfcc(filepath)
    result = model.predict(mfcc.reshape(1, -1))
    result = int(result.item())
    print(f"This is {gender_map[result]}'s voice")


if __name__ == '__main__':
    filepath = sys.argv[1]
    # filepath = "./data/wav_data/A30001X2.wav"
    main(filepath)