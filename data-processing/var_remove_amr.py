import re
import argparse
import os
from amr_utils import write_to_file, remove_char_outside_quotes

from convert_single_line import single_line_convert
from wiki_remove_amr import delete_wiki

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
    parser.add_argument('-oe', "--output_ext", default='',
                        help="Extension of output AMR files if output_file not given (default .single.txt)")
    return parser.parse_args()
def process_var_line(line, var_dict):
    '''Function that processes line with a variable in it. Returns the string without
       variables and the dictionary with var-name + var - value
       Only works if AMR is shown as multiple lines and input correctly!'''
    curr_var_name = False
    curr_var_value = False
    var_value = ''
    var_name = ''
    current_quotes = False
    for ch in line:
        # We start adding the variable value
        if ch == '/' and not current_quotes:
            curr_var_value = True
            curr_var_name = False
            var_value = ''
            continue
        # We start adding the variable name
        elif ch == '(' and not current_quotes:
            curr_var_name = True
            curr_var_value = False
            # We already found a name-value pair, add it now
            if var_value and var_name:
                # Remove closing brackets that were not in between quotes
                add_value = remove_char_outside_quotes(var_value.strip(), ')')
                # Now we have to check: if this previous item starts with ':', we remove it,
                # because that means it started a new part ( :name (n / name ..)
                if add_value.split()[-1].startswith(':'):
                    add_value = " ".join(add_value.split()[:-1])
                var_dict[var_name.strip()] = add_value
            var_name = ''
            continue
        # Check if we are currently within quotes
        elif ch == '"':
            current_quotes = not current_quotes

        # Add to variable name/value
        if curr_var_name:
            var_name += ch
        if curr_var_value:
            var_value += ch

    # Remove brackets that were not within quotes for final var value
    final_var = remove_char_outside_quotes(var_value, ')')
    # Save information to dictionary
    var_dict[var_name.strip()] = final_var
    # Remove variable information from the AMR line
    # deleted_var_string = re.sub(r'\([a-zA-Z-_0-9]+[\d]? /', '(', line).replace('( ', '(')
    deleted_var_string = re.sub(r'\(\s*([^\s/()]+)\s*/', '(', line).replace('( ', '(')
    return deleted_var_string, var_dict


def delete_amr_variables(amrs):
    '''Function that deletes variables from AMRs'''
    full_var_dict = {}
    del_amr = []

    # First get the var dict
    for line in amrs:
        _, full_var_dict = process_var_line(line, full_var_dict)

    # Loop over AMRs to rewrite
    for line in amrs:
        # if re.search(r'\b\d+(\.\d+)?\b', line):
        #     del_amr.append(line)
        #     continue
        if line.strip() and line[0] != '#':
            if '/' in line:
                # Found variable here
                # Get the deleted variable string and save
                deleted_var_string, _ = process_var_line(line, full_var_dict)
                del_amr.append(deleted_var_string)
            else:
                # Probable reference to variable here!
                split_line = line.split()
                # print(line)
                ref_var = split_line[1].replace(')', '')

                # Check if the variable occurs in our dictionary
                if ref_var in full_var_dict and False:
                    # Get value to replace the variable name with
                    ref_value = full_var_dict[ref_var]
                    # Do the replacing and add brackets for alignment
                    split_line[1] = split_line[1].replace(ref_var, '(' + ref_value.strip() + ')')
                    n_line = (len(line) - len(line.lstrip())) * ' ' + " ".join(split_line)
                    del_amr.append(n_line)
                else:
                    # No reference found, add line without editing (usually there are numbers in this line)
                    del_amr.append(line)
        else:
            # Line with other info, just add
            del_amr.append(line)
    return del_amr

if __name__ == "__main__":

    args = create_args_parser()

    train_amr_merged = args.input_file
    if args.output_file:
        output_path = args.output_file

    out_ext = args.output_ext

    amr_train_no_wiki = delete_wiki(train_amr_merged)

    amr_remove_wiki_vars = delete_amr_variables(amr_train_no_wiki)
    # amr_final_single_line, _ = single_line_convert(amr_remove_wiki_vars, "")


    write_to_file(amr_remove_wiki_vars, output_path + args.output_ext)

    for amr in amr_remove_wiki_vars:
        print(amr)
        break