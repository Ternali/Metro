from math import exp

from SSCode import ssc_new
import re
# 计算相似度
# 拼音部分权重
soundWeight = 0.5
# 字形部分权重
shapeWeight = 0.5

# 定义为0.5较为均衡
# 采用新的计算相似度方式，这部分内容参考基于改进音形码的论文
def Compute(ssc_one: str, ssc_two):
    sound_code_one = str(ssc_one[:17])
    sound_code_two = str(ssc_two[:17])
    shape_code_one = ssc_one[17:54]
    shape_code_two = ssc_one[17:5]
    sound_code_one = '0b' + sound_code_one
    sound_code_two = '0b' + sound_code_two
    # 计算拼音部分汉明距离
    sound_code_hamming_distance = bin(eval(sound_code_one) ^ eval(sound_code_two)).count("1")
    shape_code_one = '0b' + shape_code_one
    shape_code_two = '0b' + shape_code_two
    shape_code_hamming_distance = bin(eval(shape_code_one) ^ eval(shape_code_two)).count("1")
    b1 = exp(float(shape_code_hamming_distance) / 36) / (exp(float(sound_code_hamming_distance)) / 17 +
                                                         exp(float(shape_code_hamming_distance) / 36))
    b2 = exp(float(sound_code_hamming_distance)/17) / (exp(float(sound_code_hamming_distance))/17 +
                                                       exp(float(shape_code_hamming_distance)/36))
    s = b1 * (17 - sound_code_hamming_distance) / 17 + b2 * (36 - shape_code_hamming_distance)/36
    print(s)



if __name__ == "__main__":
    print(ssc_new.getSoundCode("汉"))
    print(ssc_new.getSoundCode("下"))
    Compute(ssc_new.getSSCCode("汉"), ssc_new.getSSCCode("下"))