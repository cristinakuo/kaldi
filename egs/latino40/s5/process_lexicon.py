import argparse
import pandas as pd
import re
import os
import errno
import unidecode

chars_to_ignore_regex = '[\|\`\~\=\_\{\}\“\'\,\¿\¡\?\.\$\!\-\;\:\"\(\)\[\&\]\>\^\x7f]'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and xos.path.isdir(path):
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

def replace_tilde(text):
    text = text.replace("ña", "nia")
    text = text.replace("ñe", "nie")
    text = text.replace("ño", "nio")
    text = text.replace("ñu", "niu")
    text = text.replace("ñi", "ni")

    return text

def main(input_csv, output_csv):
    #df = pd.read_csv(input_csv, encoding="latin-1", header=None)
    #print("Before")
    #print(df.head())
    f = open(input_csv, "r", encoding='latin-1')
    lines = f.readlines()
    f.close()
    
    new_lines = []
    for line in lines:
        new_line = replace_tilde(line)
        new_line = unidecode.unidecode(new_line)
        new_lines.append(new_line)
        
    with open(output_csv, 'w') as the_file:
        for line in new_lines:
            the_file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dict_path",
        type=str,
        help="Path to dictionary",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Output path",
    )

    args = parser.parse_args()

    main(args.dict_path, args.output_path)