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


def add_noise(signal_array, noisy_array, snr):
    noise_torch = torch.from_numpy(noisy_array).float()
    signal_torch = torch.from_numpy(signal_array).float()
    noise_len = len(noise_torch)

    signal_len = len(signal_torch)
    random_start = random.randint(0, noise_len-signal_len)
    
    signal_power = signal_torch.norm(p=2)
    noise_short = noise_torch[random_start:random_start+signal_len]
    noise_power = noise_short.norm(p=2)
    scale = snr * noise_power / signal_power
    print("Scale", scale)
    noisy_signal_torch = scale * signal_torch + noise_short
    noisy_signal_array = noisy_signal_torch.numpy()
    
    return noisy_signal_array

def add_noise_torch(signal_array, noise_array, snr_db):
    signal_len = len(signal_array)
    noise_len = len(noise_array)
    random_start = random.randint(0, noise_len-signal_len)
    noise_short = noise_array[random_start:random_start+signal_len]
    
    return F.add_noise(signal_array, noise_short, snr_db)


def main():
    parser = argparse.ArgumentParser(description="Add noise to audio data with a specified SNR (Signal-to-Noise Ratio).")
    parser.add_argument("--snr_db", type=float, required=True, help="SNR value in dB")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input audio file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to save the output audio file")
    parser.add_argument("--noise_file", type=str, required=True, help="Path to the noise audio file")
    args = parser.parse_args()

    # TODO: path to a folder

    # Read noise
    snr = 10**(args.snr_db/20)
    print(f"Adding noise to all data... SNR_DB={args.snr_db}")
    noise_array = SPHFile(args.noise_file).content
    input_array = SPHFile(args.input_file).content
    
    # Using torch audio
    input_array = torch.from_numpy(input_array).float()
    noise_array = torch.from_numpy(noise_array).float()
    snr_db = torch.tensor(args.snr_db)
    torchaudio_result = add_noise_torch(input_array, noise_array, snr_db)
    #torchaudio_result = np.int16(torchaudio_result * 32767)

    #custom_result = add_noise(input_array, noise_array, snr)
    #custom_array = np.int16(custom_array * 32767)
    result = torchaudio_result.numpy()
    result = result/np.max(result)
    
    #write_to_wav(args.output_file, noisy_array, 16000)
    sf.write(args.output_file, result, 16000, 'PCM_16')
    #write(args.output_file, 16000, result)
    
    print("Done")

if __name__ == "__main__":
    main()
    
