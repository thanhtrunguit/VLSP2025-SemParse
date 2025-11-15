
import sys
import re
from pathlib import Path

def parse_blocks(text):
    # split on one or more blank lines (lines containing only whitespace)
    raw_blocks = re.split(r"\n\s*\n", text.strip(), flags=re.MULTILINE)
    blocks = [b for b in raw_blocks if b.strip() != '']
    return blocks

def extract_from_block(block):
    """
    Return (sentence or None, amr_lines list)
    If no #::snt found -> (None, [])
    If #::snt found but no AMR lines -> (sentence, [])
    """
    m = re.search(r'^\s*#::snt\s*(.*)$', block, flags=re.MULTILINE)
    if not m:
        return None, []
    sentence = m.group(1).strip()
    # remove the first #::snt line to get AMR part
    block_after = re.sub(r'^\s*#::snt\s*.*$', '', block, count=1, flags=re.MULTILINE)
    # strip leading/trailing whitespace/newlines
    amr_text = re.sub(r'^\s+|\s+$', '', block_after, flags=re.DOTALL)
    if amr_text == '':
        return sentence, []
    amr_lines = amr_text.splitlines()
    return sentence, amr_lines

def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    blocks = parse_blocks(text)

    snts = []
    amr_blocks = []
    skipped_blocks = 0

    for block in blocks:
        sentence, amr_lines = extract_from_block(block)
        if sentence is None:
            skipped_blocks += 1
            continue
        snts.append(sentence)
        amr_blocks.append(amr_lines)

    return snts, amr_blocks, skipped_blocks

def write_outputs(input_path, snts, amr_blocks):
    out_snt = input_path.parent / 'problems_only.txt'
    out_amr = input_path.parent / 'graphs_only.txt'

    with open(out_snt, 'w', encoding='utf-8') as f:
        for s in snts:
            f.write(s.replace('\n', ' ').strip() + '\n')

    with open(out_amr, 'w', encoding='utf-8') as f:
        for block in amr_blocks:
            for line in block:
                f.write(line.rstrip() + '\n')

    return out_snt, out_amr

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_amr.py input.txt")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    snts, amr_blocks, skipped = process_file(input_path)

    out_snt, out_amr = write_outputs(input_path, snts, amr_blocks)

    print(f"Done. Extracted {len(snts)} sentence(s) and {len(amr_blocks)} AMR block(s).")
    if skipped:
        print(f"Skipped {skipped} block(s) that didn't contain '#::snt'.")
    print(f"Sentences -> {out_snt}")
    print(f"AMR blocks -> {out_amr} (multi-line AMR blocks separated by one blank line)")

if __name__ == '__main__':
    main()
