import argparse
import re
from pathlib import Path

def join_amr_lines(input_path: Path, output_path: Path, keep_blank=True):
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines = []
    i = 0
    merged_count = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        stripped = raw.strip()

        # keep blank lines
        if stripped == "":
            if keep_blank:
                out_lines.append("")
            i += 1
            continue

        # keep comment/meta lines (#::...) as-is
        if stripped.startswith("#"):
            out_lines.append(raw)
            i += 1
            continue

        # otherwise try to collect a possibly multi-line AMR block
        buffer = stripped
        open_count = buffer.count("(")
        close_count = buffer.count(")")
        balance = open_count - close_count

        j = i + 1
        # Append following lines until parentheses balanced or we hit a comment line
        while balance > 0 and j < len(lines):
            nxt_raw = lines[j].rstrip("\n")
            nxt = nxt_raw.strip()
            # don't merge comment lines into AMR (likely next block)
            if nxt.startswith("#") or nxt == "":
                break
            buffer += " " + nxt
            balance += nxt.count("(") - nxt.count(")")
            j += 1

        # normalize whitespace to single spaces
        buffer = re.sub(r'\s+', ' ', buffer).strip()

        # write merged line
        out_lines.append(buffer)

        if j - i > 1:
            merged_count += (j - i)

        # advance index
        i = j

    # write out
    with output_path.open("w", encoding="utf-8") as f:
        for L in out_lines:
            f.write(L + "\n")

    return merged_count, len(out_lines)

def main():
    parser = argparse.ArgumentParser(description="Join multi-line AMR graphs back into single lines.")
    parser.add_argument("-f", "--input",help="Input file (possibly with broken AMR lines)")
    parser.add_argument("-o", "--output",nargs="?", help="Output file (default: <input>.joined)", default=None)
    args = parser.parse_args()

    inp = Path(args.input)
    outp = Path(args.output) if args.output else inp.with_suffix(inp.suffix + ".joined")

    merged_count, out_lines = join_amr_lines(inp, outp)
    print(f"Saved {outp} — total output lines: {out_lines}; merged {merged_count} extra lines into previous lines.")

if __name__ == "__main__":
    main()
