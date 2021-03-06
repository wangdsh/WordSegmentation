# -*- coding=utf-8 -*-

import sys
import codecs


def utf16_to_utf8(input_file, output_file):
    fp_input = codecs.open(input_file, 'r', 'utf-16')
    fp_output = codecs.open(output_file, 'w', 'utf-8')

    fp_output.write(fp_input.read())

    fp_input.close()
    fp_output.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "pls use: python utf16_to_utf8.py input output"
        sys.exit()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    utf16_to_utf8(input_file, output_file)

# python utf16_to_utf8.py crf_train_data.seg crf_train_data_utf8.seg
