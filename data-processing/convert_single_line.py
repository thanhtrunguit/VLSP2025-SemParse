import sys
import re
import argparse
import os

from amr_utils import write_to_file

def create_args_parser():
    '''Creating arg parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input_file", required=True, type=str, help="AMR file or folder")
    parser.add_argument("-o", "--output_file", required=True, type=str,
                        help="Full path of output file (default: same name as input but with output_ext)")
    parser.add_argument('-fol', "--folder", action='store_true',
                        help='Process multiple files in a folder - if not, args.input_file is a file')
    parser.add_argument('-a', "--amr_ext", default='.txt', type=str,
                        help="Input files must have this extension (default .txt, only necessary when using -fol)")
    parser.add_argument('-oe', "--output_ext", default='.txt',
                        help="Extension of output AMR files if output_file not given (default .single.txt)")
    return parser.parse_args()

def single_line_convert(lines, sent_file):
    '''Convert AMRs to a single line, ignoring lines that start with "# ::"
      If a sentence file is specified we also try to get the sentences'''
    all_amrs, cur_amr, sents = [], [], []
    for line in lines:
        if not line.strip() and cur_amr:
            cur_amr_line = " ".join(cur_amr)
            all_amrs.append(cur_amr_line.strip())
            cur_amr = []
        elif line.startswith('#::snt'):
            # Save sentences as well (don't always need them)
            sent = re.sub('(^#::snt)', '', line).strip() #remove # ::snt or # ::tok
            sents.append(sent)
        elif not line.startswith('#'):
            cur_amr.append(line.strip())
    # File did not end with newline, so add AMR here
    if cur_amr:
        all_amrs.append(" ".join(cur_amr).strip())

    # If we didn't find sentences, but we did have a sentence file, read the sentences from there (if possible)
    if not sents and sent_file:
        if os.path.isfile(sent_file):
            sents = [x.strip() for x in open(sent_file, 'r')]
            # Sanity check
            assert len(all_amrs) == len(sents), "{0} vs {1}".format(len(all_amrs), len(sents))
    return all_amrs, sents

def single_line_convert_with_snt(lines, sent_file):
    '''Convert AMRs to single-line graphs, keep #::snt on its own line before the AMR, add blank line after each pair'''
    all_amrs, cur_amr = [], []
    current_snt = None
    sents = []

    for line in lines:
        if not line.strip() and cur_amr:
            # End of AMR block → save sentence + AMR
            amr_str = " ".join(cur_amr).strip()
            if current_snt:
                all_amrs.append(current_snt.strip())  # sentence line
                current_snt = None
            all_amrs.append(amr_str)  # AMR line
            all_amrs.append("")       # blank line
            cur_amr = []
        elif line.startswith('#::snt'):
            current_snt = line.strip()
            sent = re.sub('(^#::snt)', '', line).strip()
            sents.append(sent)
        elif not line.startswith('#'):  # AMR graph content
            cur_amr.append(line.strip())

    # Handle last AMR if file doesn't end with newline
    if cur_amr:
        amr_str = " ".join(cur_amr).strip()
        if current_snt:
            all_amrs.append(current_snt.strip())
        all_amrs.append(amr_str)
        all_amrs.append("")

    # Optional: read sentences from file if not found
    if not sents and sent_file:
        if os.path.isfile(sent_file):
            sents = [x.strip() for x in open(sent_file, 'r')]
            assert len(all_amrs) == len(sents), f"{len(all_amrs)} vs {len(sents)}"

    return all_amrs, sents


if __name__ == "__main__":

    args = create_args_parser()

    amr_file_input_path = args.input_file
    out_ext = args.output_ext

    with open(amr_file_input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    single_line_amrs, _ = single_line_convert(lines, sent_file=None)

    if args.output_file:
        output_path = args.output_file

    write_to_file(single_line_amrs, output_path + args.output_ext)

    print("=== Single-line AMRs ===")
    for amr in single_line_amrs:
        print(amr)
        break



