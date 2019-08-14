#!/usr/bin/python3
import argparse  # argument parsing
import os.path  # file exist check
import logging  # logs
import re  # regex
import sys
from doxydown.classes import Main, Language, Class, Regex
from doxydown.print import print_doxydown
from doxydown.comments import handle_comment


ExtensionsRegex = [r'\w\.[h|c]\b']


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path to source file with doxygen comments")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument('-o', '--output', type=argparse.FileType('w', encoding='UTF-8'),
                       help='output file name')
    return parser.parse_args()


def logging_init(verbose):
    log_format = "%(message)s"
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.ERROR, format=log_format)


def check_if_file_exist(file):
    if not os.path.isfile(args.file):
        logging.error(f"[Error] {args.file} File doesn't not exist")
        exit(1)


def regex_language_select(file):
    check_if_file_exist(file)
    for lang in Language:
        if re.search(ExtensionsRegex[lang.value], file):
            logging.debug(f'{lang.name} selected')
            return Regex(lang)


def read_file():
    file = open(args.file, "r")
    file_lines = file.readlines()
    file.close()

    doxy_structures = Main()
    comment_start = 0
    comment_end = 0
    in_comment = False
    i = 1
    while i < len(file_lines):
        if re.search(regex.start, file_lines[i]):
            comment_start = i
            in_comment = True
        elif in_comment:
            if re.search(regex.end, file_lines[i]):
                comment_end = i
                in_comment = False
                return_type, value = handle_comment(file_lines[comment_start:], comment_end-comment_start)
                if return_type == Class.Function:
                    doxy_structures.function.append(value)
                elif return_type == Class.Define:
                    doxy_structures.define.append(value)
                elif return_type == Class.Enum:
                    doxy_structures.enum.append(value)
                elif return_type == Class.Struct:
                    doxy_structures.struct.append(value)
                elif return_type == Class.Module:
                    doxy_structures.module = value
                elif return_type == Class.Non:
                    pass
        i += 1
    return doxy_structures


if __name__ == "__main__":
    args = parse_arguments()
    logging_init(args.verbose)
    regex = regex_language_select(args.file)
    data = read_file()

    out_file = open(args.output.name, "w") if args.output else sys.stdout
    print_doxydown(data, out_file)
    if out_file is not sys.stdout:
        out_file.close()
