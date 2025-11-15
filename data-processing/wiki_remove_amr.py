import re
import argparse
import os
from amr_utils import write_to_file
def create_args_parser():
    '''Creating arg parser'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input_file", required=True, type=str, help="AMR file or folder")
    parser.add_argument("-o", "--output_file", required=False, type=str,
                        help="Full path of output file (default: same name as input but with output_ext)")
    parser.add_argument('-fol', "--folder", action='store_true',
                        help='Process multiple files in a folder - if not, args.input_file is a file')
    parser.add_argument('-a', "--amr_ext", default='.txt', type=str,
                        help="Input files must have this extension (default .txt, only necessary when using -fol)")
    parser.add_argument('-oe', "--output_ext", default='.txt',
                        help="Extension of output AMR files if output_file not given (default .single.txt)")
    parser.add_argument('-k', '--keep_wiki', action='store_true', help='Keep Wiki link when processing')
    return parser.parse_args()



# def delete_wiki(input_file):
#     '''Delete wiki links from AMRs'''
#     no_wiki = []
#     with open(input_file, 'r', encoding='utf-8') as f:
#         for line in f:
#             # Remove all :wiki(...) occurrences but leave surrounding graph parentheses intact
#             # (we include optional leading whitespace so we don't leave an extra space)
#             n_line = re.sub(r'\s*:wiki\([^()]*\)', '', line)
#             # Remove :wiki - forms too
#             n_line = re.sub(r'\s*:wiki\s*-\s*', '', n_line)
#
#             # Normalize whitespace but preserve leading indent
#             indent = len(n_line) - len(n_line.lstrip(' '))
#             cleaned = ' ' * indent + ' '.join(n_line.split())
#
#             # If a line contains only closing parens like ")" or ")))", merge it onto previous line
#             if re.fullmatch(r'^\s*\)+\s*$', cleaned):
#                 if no_wiki:
#                     # append the closing parens directly to the previous logical line
#                     no_wiki[-1] = no_wiki[-1] + cleaned.strip()
#                 else:
#                     # if file starts oddly with parens, keep it
#                     no_wiki.append(cleaned)
#             else:
#                 no_wiki.append(cleaned)
#     return no_wiki

# def delete_wiki(input_file):
#     '''No-op version: keep original AMRs unchanged'''
#     with open(input_file, 'r', encoding='utf-8') as f:
#         return [line.rstrip("\n") for line in f]


def delete_wiki(input_file):
    '''No-op version: keep AMRs unchanged but normalize whitespace and keep indentation'''
    cleaned_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Preserve indentation level
            indent = len(line) - len(line.lstrip(' '))
            # Normalize inner whitespace but keep indentation
            cleaned = ' ' * indent + ' '.join(line.split())

            # Merge lines that contain only closing parentheses
            if re.fullmatch(r'^\s*\)+\s*$', cleaned):
                if cleaned_lines:
                    cleaned_lines[-1] += cleaned.strip()
                else:
                    cleaned_lines.append(cleaned)
            else:
                cleaned_lines.append(cleaned)
    return cleaned_lines

if __name__ == "__main__":

    args = create_args_parser()

    amr_train_input_path = args.input_file
    out_ext = args.output_ext
    keep_wiki = args.keep_wiki

    amr_no_wiki = delete_wiki(amr_train_input_path)

    if args.output_file:
        output_path = args.output_file

    write_to_file(amr_no_wiki, output_path + args.output_ext)

    for amr in amr_no_wiki:
        print(amr)
        break