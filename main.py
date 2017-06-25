# -*- coding=utf-8 -*-

import codecs
import random
import sys

origin_train_file = 'Train_utf16.seg'
train_file_seven = 'Train_utf16_seven.seg'
train_file_three = 'Train_utf16_three.seg'
test_gold_without_blank = 'test_gold_without_blank.txt'


# 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试
# 前70%用于训练，后30%用于测试
def divide():
    origin_file = codecs.open(origin_train_file, 'r', 'utf-16')
    origin_file_seven = codecs.open(train_file_seven, 'w', 'utf-16')
    origin_file_three = codecs.open(train_file_three, 'w', 'utf-16')
    test_gold = codecs.open(test_gold_without_blank, 'w', 'utf-8')

    lines = origin_file.readlines()
    total_line_num = len(lines)
    cut_line_num = int(total_line_num * 0.7)
    print 'cut_line_num:', cut_line_num

    for i in range(cut_line_num):
        origin_file_seven.write(lines[i])

    for i in range(cut_line_num, total_line_num):
        if lines[i].strip() != '':
            test_gold.write(lines[i])
        # 因为用作测试，所以把分隔符去掉
        origin_file_three.write(lines[i].replace('  ', ''))

    origin_file.close()
    origin_file_seven.close()
    origin_file_three.close()
    test_gold.close()


# 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试
# 后70%用于训练，前30%用于测试
def divide_two():
    origin_file = codecs.open(origin_train_file, 'r', 'utf-16')
    origin_file_seven = codecs.open(train_file_seven, 'w', 'utf-16')
    origin_file_three = codecs.open(train_file_three, 'w', 'utf-16')
    test_gold = codecs.open(test_gold_without_blank, 'w', 'utf-8')

    lines = origin_file.readlines()
    total_line_num = len(lines)
    cut_line_num = int(total_line_num * 0.3)
    print 'cut_line_num:', cut_line_num

    for i in range(cut_line_num):
        if lines[i].strip() != '':
            test_gold.write(lines[i])
        # 因为用作测试，所以把分隔符去掉
        origin_file_three.write(lines[i].replace('  ', ''))

    for i in range(cut_line_num, total_line_num):
        origin_file_seven.write(lines[i])

    origin_file.close()
    origin_file_seven.close()
    origin_file_three.close()
    test_gold.close()


# 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试
# 后70%用于训练，前30%用于测试
def divide_three():
    origin_file = codecs.open(origin_train_file, 'r', 'utf-16')
    origin_file_seven = codecs.open(train_file_seven, 'w', 'utf-16')
    origin_file_three = codecs.open(train_file_three, 'w', 'utf-16')
    test_gold = codecs.open(test_gold_without_blank, 'w', 'utf-8')

    lines = origin_file.readlines()
    total_line_num = len(lines)

    train = True
    count = 0
    for i in range(total_line_num):
        if train:  # 训练
            origin_file_seven.write(lines[i])
            count += 1
            if count == 7:
                train = False
                count = 0
        else:  # 测试
            if lines[i].strip() != '':
                test_gold.write(lines[i])
            origin_file_three.write(lines[i].replace('  ', ''))
            count += 1
            if count == 3:
                train = True
                count = 0

    origin_file.close()
    origin_file_seven.close()
    origin_file_three.close()
    test_gold.close()


# 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试
# 产生随机数，随机选择
def divide_four():
    origin_file = codecs.open(origin_train_file, 'r', 'utf-16')
    origin_file_seven = codecs.open(train_file_seven, 'w', 'utf-16')
    origin_file_three = codecs.open(train_file_three, 'w', 'utf-16')
    test_gold = codecs.open(test_gold_without_blank, 'w', 'utf-8')

    lines = origin_file.readlines()
    total_line_num = len(lines)

    nums = range(10)

    for i in range(total_line_num / 10):
        random.shuffle(nums)
        for j in range(10):
            if j < 7:
                origin_file_seven.write(lines[i * 10 + nums[j]])
            else:
                if lines[i * 10 + nums[j]].strip() != '':
                    test_gold.write(lines[i * 10 + nums[j]])
                origin_file_three.write(lines[i * 10 + nums[j]])
    for line in lines[-(total_line_num % 10 + 1):]:  # 最后几行算训练数据吧
        origin_file_seven.write(line)

    origin_file.close()
    origin_file_seven.close()
    origin_file_three.close()
    test_gold.close()


def shuffle_train():
    origin_file = codecs.open(origin_train_file, 'r', 'utf-16')
    shuffle_train_file = codecs.open('Train_utf16_shuffle.seg', 'w', 'utf-16')

    lines = origin_file.readlines()
    total_line_num = len(lines)
    print 'total_line_num:', total_line_num

    nums = range(10)

    for i in range(total_line_num / 10):
        random.shuffle(nums)
        for j in range(10):
            shuffle_train_file.write(lines[i * 10 + nums[j]])
    for line in lines[-(total_line_num % 10):]:  # 最后几行
        shuffle_train_file.write(line)

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] != 'divide' or \
            (sys.argv[2] != '1' and sys.argv[2] != '2' and sys.argv[2] != '3' and sys.argv[2] != '4' and sys.argv[2] != '5'):
        print "usage: python main.py divide 1 or 2 or 3 or 4"
        exit(0)
    if sys.argv[2] == '1':  # 前70%用于训练，后30%用于测试
        divide()  # 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试
    elif sys.argv[2] == '2':  # 后70%用于训练，前30%用于测试
        divide_two()
    elif sys.argv[2] == '3':  # 按10行切分，每块前7行为训练，后3行为测试
        divide_three()
    elif sys.argv[2] == '4':
        divide_four()
    elif sys.argv[2] == '5':  # 将全部训练数据集打乱顺序
        shuffle_train()

# python main.py divide 1
# python main.py divide 2
# python main.py divide 3
# python main.py divide 4
# python main.py divide 5
