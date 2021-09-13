from SSCode import ssc
from SSCSimilarityCompute import ssc_similarity

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


if __name__ == "__main__":
    strs = ''
    for i in range(1, 58):
        strs += '0'
    print(strs)
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
