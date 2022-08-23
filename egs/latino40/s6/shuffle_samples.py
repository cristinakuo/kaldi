"""
Script to shuffle samples: 90% train and 10% test, no validation
    
"""
import argparse
import pandas as pd
import os
import errno
import random
import math

TRAIN_PROPORTION = 0.8
TEST_PROPORTION = 0.1
VAL_PROPORTION = 0.1

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def main(database_dir, output_dir, first_seed, second_seed):
    original_partitions = ['train', 'test', 'val']

    partitions_dfs = []
    for partition in original_partitions:
        file_path = os.path.join(database_dir, f'data_{partition}.csv')
        df = pd.read_csv(file_path)
        print(f"Read {partition} with {len(df)} samples.")
        partitions_dfs.append(df)
    all_samples_df = pd.concat(partitions_dfs)

    all_samples = len(all_samples_df)
    all_indices = list(range(all_samples))
    print("Finally", all_samples)
    
    train_num_samples = math.ceil(all_samples*TRAIN_PROPORTION)
    test_num_samples = math.ceil(all_samples*TEST_PROPORTION)
    random.seed(first_seed)
    train_indices = random.sample(all_indices, train_num_samples)
    
    left_indices = [index for index in all_indices if index not in train_indices]
    test_indices = random.sample(left_indices, test_num_samples)
    val_indices = [index for index in left_indices if index not in test_indices]

    train_df = all_samples_df.loc[all_samples_df.index.isin(train_indices)]
    test_df = all_samples_df.loc[all_samples_df.index.isin(test_indices)]
    val_df = all_samples_df.loc[all_samples_df.index.isin(val_indices)]

    print("Train", len(train_df))
    print("Test", len(test_df))
    print("Val", len(val_df))

    out_dir = os.path.join(output_dir, f"{first_seed}_{second_seed}")
    mkdir_p(out_dir)
    train_df.to_csv(os.path.join(out_dir, "data_train.csv"), index=False)
    test_df.to_csv(os.path.join(out_dir, "data_test.csv"), index=False)
    val_df.to_csv(os.path.join(out_dir, "data_val.csv"), index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "database_dir",
        type=str,
        help="Path to database, where datasets CSV are.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="Output dir.",
    )
    parser.add_argument(
        "first_seed",
        type=int,
        help="First seed",
    )
    parser.add_argument(
        "second_seed",
        type=int,
        help="Second seed",
    )

    args = parser.parse_args()

    main(args.database_dir, args.output_dir, args.first_seed, args.second_seed)