说明：

1） 任务为汉语分词
2） 文件的编码格式为 utf-16 little endian
3） 训练数据存放在 Train_utf16.seg 中
5)  测试数据放在 Test_utf16.seg 中

要求：

1） 将训练数据Train_utf16.seg分成 7：3，用70 % 部分训练，用 30% 测试，按通常的 P/R/F 三个指标评测，在实验报告中给出结果值；

2） 用全部训练数据 Train_utf16.seg 训练，用测试数据 Test_utf16.seg 测试，将测试结果按同训练数据相同的格式提交上来(编码格式为 utf-16 little endian)。结果文件按“姓名-学号.seg” 表示。

3）  实验报告必须包括你使用的方法，实验的设置和步骤，30%作为测试的结果值，问题分析与讨论。

6月26日23点之前交，逾期算缺交。
抄袭者0分
提交结果与实验报告
评测结果好坏直接影像得分
同小组同学选择不同的任务
发到邮箱：lxww301@pku.edu.cn

CRF执行流程

### run order(原始版)

*** divide train data to 7:3, 7 for train, 3 for test
python main.py divide

*** change train data format for crf++
python make_crf_train_data.py Train_utf16_seven.seg crf_train_data.seg

*** change utf16 to utf8
python utf16_to_utf8.py crf_train_data.seg crf_train_data_utf8.seg

*** using crf train model
crf_learn -f 3 -c 4.0 template crf_train_data_utf8.seg crf_model

*** change test data format for crf++
python make_crf_test_data.py Train_utf16_three.seg crf_test_data.seg

*** change utf16 to utf8
python utf16_to_utf8.py crf_test_data.seg crf_test_data_utf8.seg

*** word segmentation
crf_test -m crf_model crf_test_data_utf8.seg > msr_test4crf.tag.utf8

*** change data to word
python crf_data_2_word.py msr_test4crf.tag.utf8 msr_test4crf.tag2word.utf8

*** get train word dict for evaluation
python train_dict.py

*** change utf16 to utf8
python utf16_to_utf8.py Train_word_dict.txt Train_word_dict_utf8.txt

*** evaluation
./score Train_word_dict_utf8.txt test_gold_without_blank.txt msr_test4crf.tag2word.utf8 > score_result.txt

过程简化（简化版: 提供一个CRF分词脚本, 输入待分词文本，输出分词后的文本。模型训练过程不变）

*** divide train data to 7:3, 7 for train, 3 for test
python main.py divide

*** change train data format for crf++
python make_crf_train_data.py Train_utf16_seven.seg crf_train_data.seg

*** change utf16 to utf8
python utf16_to_utf8.py crf_train_data.seg crf_train_data_utf8.seg

*** using crf train model
crf_learn -f 3 -c 4.0 template crf_train_data_utf8.seg crf_model

*** test data format transfer
python utf16_to_utf8.py Train_utf16_three.seg Train_utf8_three.seg

*** crf segmentation, remove blank
python crf_segmenter.py crf_model Train_utf8_three.seg msr_test4crf.tag.utf8
python remove_blank_line_util.py msr_test4crf.tag.utf8 msr_test4crf.tag2word.utf8

*** evaluation
./score Train_word_dict_utf8.txt test_gold_without_blank.txt msr_test4crf.tag2word.utf8 > score_result.txt


遇到问题及解决方法：
如果python要使用CRFPP包，必须安装python的依赖包，在下载源码解压后的 CRF++-0.58/python路径下运行以下命令(缺少Python.h错误：apt-get install python-dev)
# python setup.py build
# python setup.py install


crf_learn参数说明
-f num
这个参数设置特征的cut-off threshold。CRF++使用训练数据中至少NUM次出现的特征。默认值为1。当使用CRF++到大规模数据时，只出现一次的特征可能会有几百万，这个选项就会在这样的情况下起到作用。
-c float
这个参数设置CRF的hyper-parameter。c的数值越大，CRF拟合训练数据的程度越高。这个参数可以调整过度拟合和不拟合之间的平衡度。这个参数可以通过交叉验证等方法寻找较优的参数。
-p NUM
如果电脑有多个CPU，那么那么可以通过多线程提升训练速度。NUM是线程数量。
-a CRF-L2 or CRF-L1
规范化算法选择。默认是CRF-L2。一般来说L2算法效果要比L1算法稍微好一点，虽然L1算法中非零特征的数值要比L2中大幅度的小。


Maximum Entropy执行流程

*** 对训练语料进行标注
python ./MaximumEntropy/character_tagging.py ./Train_utf16_seven.seg ./MaximumEntropy/msr_training.tagging.utf16

*** utf16 to utf8
python utf16_to_utf8.py ./MaximumEntropy/msr_training.tagging.utf16 ./MaximumEntropy/msr_training.tagging.utf8

*** 用PosTagger来训练一个字标注器
/root/maxent/example/postagger/postrainer.py -f /home/derc/wangdsh/WordSegmentation/MaximumEntropy/msr_training.tagging.utf8 --iters 100 /home/derc/wangdsh/WordSegmentation/MaximumEntropy/msr_tagger.model

*** test data format transfer
python utf16_to_utf8.py Train_utf16_three.seg Train_utf8_three.seg

*** 对测试语料将其单字离散化并添加空格，便于标注
python ./MaximumEntropy/character_split.py Train_utf8_three.seg ./MaximumEntropy/msr_test.split.utf8

*** 执行最大熵标注脚本得到字标注结果
/root/maxent/example/postagger/maxent_tagger.py -m /home/derc/wangdsh/WordSegmentation/MaximumEntropy/msr_tagger.model /home/derc/wangdsh/WordSegmentation/MaximumEntropy/msr_test.split.utf8 > /home/derc/wangdsh/WordSegmentation/MaximumEntropy/msr_test.split.tag.utf8

*** 按标注的词位信息把结果再转化为分词结果
python ./MaximumEntropy/character_2_word.py ./MaximumEntropy/msr_test.split.tag.utf8 ./MaximumEntropy/msr_test.split.tag2word.utf8

*** remove_blank_line and strip
python remove_blank_line_util.py ./MaximumEntropy/msr_test.split.tag2word.utf8 ./MaximumEntropy/msr_test.split.tag2word.no.blank.utf8

*** 评测
./score Train_word_dict_utf8.txt test_gold_without_blank.txt ./MaximumEntropy/msr_test.split.tag2word.no.blank.utf8 > ./MaximumEntropy/score_result.txt

测试结果格式整理
vi
行末添加一个空格（最后加1个空格）
:%s/$/
行首删除一个空格
:%s/^ //
