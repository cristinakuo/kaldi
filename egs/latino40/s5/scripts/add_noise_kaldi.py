import os
import argparse
from glob import glob
from add_noise import add_noise
from tqdm import tqdm
from sphfile import SPHFile
import numpy as np
from pathlib import Path
import soundfile as sf

def split_path(full_path, base_path):
    full_path = Path(full_path)
    base_path = Path(base_path)

    if base_path in full_path.parents:
        relative_path = full_path.relative_to(base_path)
        return str(base_path), str(relative_path)
    else:
        return None, str(full_path)

def main():
    parser = argparse.ArgumentParser(description="Add noise to audio data with a specified SNR (Signal-to-Noise Ratio).")
    parser.add_argument("--snr_db", type=int, required=True, help="SNR value in dB")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the input audio dir")
    parser.add_argument("--noise_file", type=str, required=True, help="Path to the noise audio file")
    args = parser.parse_args()
    
    input_dir = args.input_dir
    wav_files = glob(input_dir + "/**/*.wav", recursive=True)
    print(f"Found {len(wav_files)} files.")
    # Read noise
    print(f"Adding noise to all data... SNR_DB={args.snr_db}")
    snr_db = args.snr_db
    noise_array = SPHFile(args.noise_file).content
    for wav_file in tqdm(wav_files):
        input_array = SPHFile(wav_file).content
    
        result = add_noise(input_array, noise_array, snr_db)
        result = result/np.max(result)

        base_path, tail_path = split_path(wav_file, input_dir)
        new_base_path = base_path + f'_snr_{snr_db}dB'
        new_path = os.path.join(new_base_path, tail_path)
        # Create the output directory if it does not exist
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        sf.write(new_path, result, 16000, 'PCM_16')
    
    print("Done")

if __name__ == "__main__":
    main()
    
