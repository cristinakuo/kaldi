import argparse
from sphfile import SPHFile
import random
from time import sleep
import torch
from torchaudio import functional as F

import torch
from scipy.io.wavfile import write
import numpy as np
from IPython.display import display, HTML, Audio
import IPython.display as ipd
import soundfile as sf


def add_noise(signal_array: np.array, noise_array: np.array, snr_db: int) -> np.array:
    signal_array = torch.from_numpy(signal_array).float()
    noise_array = torch.from_numpy(noise_array).float()
    snr_db = torch.tensor(snr_db)
    signal_len = len(signal_array)
    noise_len = len(noise_array)
    random_start = random.randint(0, noise_len-signal_len)
    noise_short = noise_array[random_start:random_start+signal_len]
    
    return F.add_noise(signal_array, noise_short, snr_db).numpy()


def main():
    parser = argparse.ArgumentParser(description="Add noise to audio data with a specified SNR (Signal-to-Noise Ratio).")
    parser.add_argument("--snr_db", type=float, required=True, help="SNR value in dB")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input audio file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save the output audio file")
    parser.add_argument("--noise_file", type=str, required=True, help="Path to the noise audio file")
    args = parser.parse_args()

    # TODO: path to a folder

    # Read noise
    print(f"Adding noise to all data... SNR_DB={args.snr_db}")
    snr_db = args.snr_db
    noise_array = SPHFile(args.noise_file).content
    input_array = SPHFile(args.input_file).content
    
    result = add_noise(input_array, noise_array, snr_db)
    result = result/np.max(result)
    
    sf.write(args.output_file, result, 16000, 'PCM_16')
    
    print("Done")

if __name__ == "__main__":
    main()
    
