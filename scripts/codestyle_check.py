#!/usr/bin/python2.7

INDENT_WIDTH = 4
COLUMN_LIMIT = 1200

import argparse

def split_line_into_words(line):
    words = []
    index = 0
    while index < len(line):
        word = ""
        while index < len(line) and line[index].isalpha():
            word = word + line[index]
            index += 1
        while index < len(line) and not line[index].isalpha():
            index += 1
        if len(word) > 0:
            words.append(word)
    return words

class LineChecks:
    @staticmethod
    def indent(line, level=None):
        line_indent = len(line) - len(line.lstrip())
        if line_indent % INDENT_WIDTH != 0:
            return 'Wrong indent: ' + str(line_indent)
        elif level and line_indent != level * INDENT_WIDTH:
            return 'Wrong indent: ' + str(line_indent) + ' for level: ' + str(level)
        else:
            return None

    @staticmethod
    def trailing_spaces(line):
        if len(line) != len(line.rstrip()):
            return 'Trailing spaces'
        else:
            return None

    @staticmethod
    def column_limit(line):
        if len(line) > COLUMN_LIMIT:
            return 'Line length: ' + str(len(line)) + ' greater than limit: ' + str(COLUMN_LIMIT)

    @staticmethod
    def execute(code):
        errors = []
        checks = [
            LineChecks.indent,
            LineChecks.trailing_spaces,
            LineChecks.column_limit,
        ]
        for index, line in enumerate(code):
            for check in checks:
                error_message = check(line)
                if error_message:
                    errors.append((index, error_message, line))

        return errors

ONE_LINE_OPERATORS = ['if', 'while', 'else', 'try', 'namespace', 'for', 'switch']
ACCEPTABLE_ONE_LINE_SUBSTRINGS = ['=', '({']

def remove_comment(line):
    if '//' in line:
        return line[:line.find('//')]
    else:
        return line

YT_DEFINES = ['PROFILE_AGGREGATED_TIMING']

class BraceChecks:
    @staticmethod
    def one_line_condition(line):
        for operator in ONE_LINE_OPERATORS:
            if operator in split_line_into_words(line) and line.count('(') == line.count(')') and ';' not in line:
                line = line.rstrip()
                if line[-1] != '{':
                    return 'One-line condition should have { at the same line'

    @staticmethod
    def multiline_condition(line):
        for acceptable_substring in ACCEPTABLE_ONE_LINE_SUBSTRINGS:
            if acceptable_substring in line:
                return None
        has_condition_operator = False
        for operator in ONE_LINE_OPERATORS:
            if operator in line:
                has_condition_operator = True
        if not has_condition_operator and '}' not in line and '{' in line:
                line = line.strip()
                if line != '{':
                    return 'Opening brace { should be at the next line'

    @staticmethod
    def before_after_else(line):
        if 'else' in line and not 'else if' in line:
            line = line.strip()
            if line != '} else {':
                return 'Else should be written like } else {'

    @staticmethod
    def empty_braces(line):
        if '{}' in line:
            return 'Empty brace should have one whitespace inside: { }'

    @staticmethod
    def execute(code):
        errors = []
        checks = [
            BraceChecks.one_line_condition,
            BraceChecks.multiline_condition,
            BraceChecks.before_after_else,
            #BraceChecks.empty_braces,
        ]
        for index, line in enumerate(code):
            line = remove_comment(line)
            has_yt_define = False
            for yt_define in YT_DEFINES:
                if yt_define in line:
                    has_yt_define = True
            if '#' not in line and not has_yt_define:
                for check in checks:
                    error_message = check(line)
                    if error_message:
                        errors.append((index, error_message, line))

        return errors



def check_source_file(path):
    errors = []

    code = []
    with open(path) as file:
        code = [line.strip('\n') for line in file.readlines()]

    errors.extend(LineChecks.execute(code))
    errors.extend(BraceChecks.execute(code))

    return errors

class TextColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_errors(errors):
    for line_index, message, line in errors:
        line_numer = line_index + 1
        print '  ' + message

        trailing_spaces = u'\u25CF' * (len(line) - len(line.rstrip()))
        line = line.rstrip()
        print '    ' + TextColors.BOLD + str(line_numer) + TextColors.ENDC + ':', line + TextColors.OKBLUE + trailing_spaces + TextColors.ENDC

def main():
    parser = argparse.ArgumentParser(description='C++ source YT codestyle checker')
    parser.add_argument('sources', type=str, nargs='+', help='Sources path')

    args = parser.parse_args()

    print TextColors.BOLD + 'Check codestyle for', len(args.sources), 'files:', TextColors.ENDC,

    failed_count = 0
    for source in args.sources:
        if ".cpp" in source or ".h" in source:
            errors = check_source_file(source)
            if len(errors) > 0:
                print ''
                print 'Errors in ' + TextColors.BOLD + source + TextColors.ENDC + ':'
                print_errors(errors)
                failed_count += 1

    if failed_count > 0:
        print
        print
        print TextColors.BOLD + 'Failed count: ' + str(failed_count) + TextColors.ENDC
        exit(1)
    else:
        print TextColors.BOLD + 'OK' + TextColors.ENDC

if __name__ == '__main__':
    main()
