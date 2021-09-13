from math import exp

from SSCode import ssc
from SSCSimilarityCompute import ssc_similarity
import difflib
import binascii

'''
def getBin(fc_code_param):
    """
    :return:
    """
    fc_code_result = ""
    for num in fc_code_param:
        tmp_num = int(num)
        tmp_num = (str(bin(tmp_num))).replace('0b', '')
        for i in range(1, 5 - len(tmp_num)):
            tmp_num = "0" + tmp_num
        fc_code_result += tmp_num
    return fc_code_result
'''


if __name__ == "__main__":
    print('str'[:-1])
    print(exp(1))
    print(eval('0b111000'))
    print(eval('0b111110'))
    print(bin(56 & 62))
    print(bin(eval("0b1111101") & eval('0b1110001')))
    print(bin(eval('0b1111101') & eval('0b1110001')).count("0") - 1)
    number = int("0111111101", 2)
    number_two = int("1101111011", 2)
    # print("111".)
    print(bin(number ^ number_two).count("1"))
    number = "0b1111"
    one = "0b1001"
    # one.decode()
    print("".join(difflib.Differ().compare(number, one)))

    '''
    strs = ''
    for i in range(1, 58):
        strs += '0'
    print(strs)
    '''
'''
o = ssc.getShapeCode("汉")
print(o)
i = ssc.getSoundCode("汉")
print(i)

one = ssc.getSSCCode("汉")
two = ssc.getSSCCode("权")
print(one)
print(two)
print(ssc_similarity.computeSSCSimilarity(ssc1=one, ssc2=two))
'''
