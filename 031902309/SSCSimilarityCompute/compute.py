from math import exp
from SSCode import ssc_new
# 汉字检验确实较为困难，代码可针对异体字做出判断分析
# 采用论文所述采用精度0.7降低错误检测概率，调整为0.8时错误检测概率降低15.8%，调整为0.7可降低38.1%，调整为0.6仅降低6%
import re
# 计算相似度
# 拼音部分权重
soundWeight = 0.5
# 字形部分权重
shapeWeight = 0.5


# 定义为0.5较为均衡
# 采用新的计算相似度方式，这部分内容参考基于改进音形码的论文
def Compute(ssc_one: str, ssc_two):
    """
    :param ssc_one:
    :param ssc_two:
    """
    sound_code_one = str(ssc_one[:17])
    sound_code_two = str(ssc_two[:17])
    shape_code_one = ssc_one[17:58]  # 如果取四角编码为20位则为58否则为54
    shape_code_two = ssc_two[17:58]
    sound_code_one = '0b' + sound_code_one
    sound_code_two = '0b' + sound_code_two
    # 计算拼音部分汉明距离
    sound_code_hamming_distance = bin(eval(sound_code_one) ^ eval(sound_code_two)).count("1")
    shape_code_one = '0b' + shape_code_one
    shape_code_two = '0b' + shape_code_two
    shape_code_hamming_distance = bin(eval(shape_code_one) ^ eval(shape_code_two)).count("1")
    b1 = exp(float(shape_code_hamming_distance) / 40) / (exp(float(sound_code_hamming_distance)/17) +
                                                         exp(float(shape_code_hamming_distance) / 40))
    b2 = exp(float(sound_code_hamming_distance)/17) / (exp(float(sound_code_hamming_distance)/17) +
                                                       exp(float(shape_code_hamming_distance)/40))
    s = b1 * (17 - sound_code_hamming_distance) / 17 + b2 * (40 - shape_code_hamming_distance)/40
    return s


if __name__ == "__main__":
    print(Compute(ssc_new.getSSCCode("太"), ssc_new.getSSCCode("大")))
    print(Compute(ssc_new.getSSCCode("品"), ssc_new.getSSCCode("蕾")))