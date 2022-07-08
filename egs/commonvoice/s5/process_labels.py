import argparse
import pandas as pd
import re
import os
import errno

chars_to_ignore_regex = '[\|\`\~\=\_\{\}\“\'\,\¿\¡\?\.\$\!\-\;\:\"\(\)\[\&\]\>\^\x7f]'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def remove_special_characters(text):
    clean_text = re.sub(chars_to_ignore_regex, '', text)
    return clean_text

def process_text(text):
    text = text.lower()
    text = remove_special_characters(text)
    text = text.strip()
    # text = unidecode.unidecode(text) # For removing accents

    return text

def main(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    print("Before")
    print(df['sentence'].head())

    df['sentence'] = df['sentence'].apply(process_text)
    print("After")
    print(df['sentence'].head())
    
    mkdir_p(os.path.dirname(output_csv))
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dataset_path",
        type=str,
        help="Path to dataset CSV.",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Output path",
    )

    args = parser.parse_args()

    main(args.dataset_path, args.output_path)