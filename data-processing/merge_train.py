import argparse

def create_args_parser():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Merge multiple AMR files into one.")
    parser.add_argument("-f","--input_files", nargs="+", help="List of AMR files to merge")
    parser.add_argument("-o", "--output_file", required=True, help="Output file path")

    return parser.parse_args()

def merge_files(input_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_f:
        for file_path in input_files:
            with open(file_path, 'r', encoding='utf-8') as in_f:
                out_f.write(in_f.read().strip() + "\n\n")  # extra newline between files
    print(f"[✔] Merged {len(input_files)} files into {output_file}")

if __name__ == "__main__":
    args = create_args_parser()

    merge_files(args.input_files, args.output_file)
