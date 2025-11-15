import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Extract lines starting with '#::snt' to a file (preserve your original logic).")
    parser.add_argument("-f","--input-file",
                        help="your AMR/PENMAN file")
    parser.add_argument("-o","--output-file",
                        help="where to save extracted sentences (default: processed-data/temp/problems_only.txt)")
    parser.add_argument("--encoding", default="utf-8", help="file encoding (default: utf-8)")
    args = parser.parse_args()

    input_file = args.input_file   # your AMR/PENMAN file
    output_file = args.output_file

    # ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(input_file, "r", encoding=args.encoding) as fin, \
         open(output_file, "w", encoding=args.encoding) as fout:
        for line in fin:
            if line.startswith("#::snt"):
                sentence = line[len("#::snt"):].strip()
                fout.write(sentence + "\n")

    print(f"Extracted sentences saved to {output_file}")

if __name__ == "__main__":
    main()