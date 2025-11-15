import os
import random

def split_amr_file(input_path, train_path, dev_path, split_ratio=0.8, seed=42):
    # Read the whole file
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Group into sentence+AMR blocks
    blocks = []
    current_block = []
    for line in lines:
        if line.strip() == "":  # empty line = block separator
            if current_block:
                blocks.append("".join(current_block))
                current_block = []
        else:
            current_block.append(line)
    if current_block:  # last block if no trailing newline
        blocks.append("".join(current_block))

    # Shuffle with fixed seed
    random.seed(seed)
    random.shuffle(blocks)

    # Split into train/dev
    split_idx = int(len(blocks) * split_ratio)
    train_blocks = blocks[:split_idx]
    dev_blocks = blocks[split_idx:]

    # Write train file
    with open(train_path, "w", encoding="utf-8") as f:
        for block in train_blocks:
            f.write(block.strip() + "\n\n")

    # Write dev file
    with open(dev_path, "w", encoding="utf-8") as f:
        for block in dev_blocks:
            f.write(block.strip() + "\n\n")

    print(f"Total blocks: {len(blocks)}")
    print(f"Train: {len(train_blocks)}, Dev: {len(dev_blocks)}")

# Example usage
input_file = "original-data/train_amr_merged.txt"
train_file = "processed-data/train_split.txt"
dev_file = "processed-data/dev_split.txt"

split_amr_file(input_file, train_file, dev_file)
