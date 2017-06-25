# -*- coding: utf-8 -*-

import codecs
import sys


def remove_blank(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')

    for line in input_data.readlines():
        line = line.lstrip()
        if line.strip() != '':
            output_data.write(line)

    input_data.close()
    output_data.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "pls use: python remove_blank_line_util.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    remove_blank(input_file, output_file)

# python remove_blank_line_util.py test_gold.txt test_gold_without_blank.txt
