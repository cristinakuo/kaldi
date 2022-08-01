import argparse
import pandas as pd
import re
import os
import errno
import unidecode

chars_to_ignore_regex = '[\|\`\~\=\_\{\}\“\'\,\¿\¡\?\.\$\!\-\;\:\"\(\)\[\&\]\>\^\x7f]'
chars_to_ignore = ['"', '-', '`', '.', '*', ':', 'ː', '\'', "...", "-", "--", "<"]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def remove_special_characters(text):
    old_text = text
    for symbol in chars_to_ignore:
        text = text.replace(symbol, " ")
    text = text.replace("@", "a")

    text = re.sub(chars_to_ignore_regex, ' ', text)
    text = " ".join(text.split())
    return text

def replace_tilde(text):
    text = text.replace("ña", "nia")
    text = text.replace("ñe", "nie")
    text = text.replace("ño", "nio")
    text = text.replace("ñu", "niu")
    text = text.replace("ñi", "ni")

    return text

def process_text(text):
    text = text.lower()
    text = replace_tilde(text)
    text = unidecode.unidecode(text) # For removing accents
    text = remove_special_characters(text)
    text = text.strip() # Remove beginning and end spaces

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