import argparse

def main():
    parser = argparse.ArgumentParser(description="Merge #::snt lines with corresponding AMR lines.")
    parser.add_argument("--original-file",
                        help="file dữ liệu gốc (có #::snt)")
    parser.add_argument("--processed-file",
                        help="processed AMR file (one AMR per line expected)")
    parser.add_argument("--output-path",
                        help="output merged file path")
    parser.add_argument("--encoding", default="utf-8", help="file encoding (default utf-8)")
    args = parser.parse_args()

    # === your original variables (kept names & logic) ===
    problem_files = args.original_file #file dữ liệu gốc (có #::snt)
    processed_path = args.processed_file
    output_path = args.output_path

    # Read lines from both files
    with open(problem_files, "r", encoding=args.encoding) as f:
        results_lines = [line.rstrip("\n") for line in f]

    with open(processed_path, "r", encoding=args.encoding) as f:
        processed_lines = [line.rstrip("\n") for line in f]

    # Extract only #::snt lines from results.txt
    snt_lines = [line for line in results_lines if line.startswith("#::snt")]

    # Check length consistency
    if len(snt_lines) != len(processed_lines):
        raise ValueError(f"Line count mismatch: {len(snt_lines)} #::snt lines vs {len(processed_lines)} AMR lines")

    # Merge with empty line after each pair
    merged_lines = []
    for snt, amr in zip(snt_lines, processed_lines):
        merged_lines.append(snt)
        merged_lines.append(amr)
        merged_lines.append("")  # blank line

    # Save the merged file
    with open(output_path, "w", encoding=args.encoding) as f:
        for line in merged_lines:
            f.write(line + "\n")

    print(f"✅ Merged file saved to {output_path}")

if __name__ == "__main__":
    main()
