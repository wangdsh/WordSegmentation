#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 选取训练数据中的词生成词典

import codecs


def make_dict(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-16')
    output_data = codecs.open(output_file, 'w', 'utf-16')
    word_set = set()
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            word_set.add(word)

    for w in word_set:
        output_data.write(w+'\n')

    input_data.close()
    output_data.close()

if __name__ == '__main__':
    input_file = 'Train_utf16_seven.seg'
    output_file = 'Train_word_dict.txt'
    make_dict(input_file, output_file)

# python train_dict.py
