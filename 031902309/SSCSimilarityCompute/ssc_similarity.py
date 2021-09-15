# 计算相似度
# 将汉字对应笔画数调整回数字部分
from SSCode import ssc_new

strokesDictReverse = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10,
                      'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20,
                      'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30,
                      'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, '0': 0}
# 拼音部分权重
soundWeight = 0.5
# 字形部分权重
shapeWeight = 0.5


# 各占0.5较为均衡
# 定义d = 0.5p + 0.5s为单字相似度
def computeSoundCodeSimilarity(soundCode_one, soundCode_two):  # soundCode=['2', '8', '5', '2']
    """
    :param soundCode_one:
    :param soundCode_two:
    :return:
    """
    featureSize = len(soundCode_one)
    # 四部分各占比权重 韵母 声母 韵母补码 声调
    wights = [0.4, 0.4, 0.1, 0.1]
    multiplier = []
    for i in range(featureSize):
        if soundCode_one[i] == soundCode_two[i]:
            multiplier.append(1)
        else:
            multiplier.append(0)
    soundSimilarity = 0
    # 计算最终音码部分权重
    for i in range(featureSize):
        soundSimilarity += wights[i] * multiplier[i]
    return soundSimilarity


# 用于计算形体相似度
def computeShapeCodeSimilarity(shapeCode_one, shapeCode_two):  # shapeCode=['5', '6', '0', '1', '0', '3', '8']
    """
    :param shapeCode_one:
    :param shapeCode_two:
    :return:
    """
    featureSize = len(shapeCode_one)
    wights = [0.25, 0.1, 0.1, 0.1, 0.1, 0.1, 0.25]
    multiplier = []
    for i in range(featureSize - 1):
        if shapeCode_one[i] == shapeCode_two[i]:
            multiplier.append(1)
        else:
            multiplier.append(0)
    multiplier.append(
        1 - abs(strokesDictReverse[shapeCode_one[-1]] - strokesDictReverse[shapeCode_two[-1]]) * 1.0 / max(
            strokesDictReverse[shapeCode_one[-1]], strokesDictReverse[shapeCode_two[-1]]))
    shapeSimilarity = 0
    # 计算最终形码部分权重
    for i in range(featureSize):
        shapeSimilarity += wights[i] * multiplier[i]
    return shapeSimilarity


# 对汉字音形码进行计算
def computeSSCSimilarity(ssc1, ssc2):
    """
    :param ssc1:
    :param ssc2:
    :return:
    """
    # return
    # 0.5*computeSoundCodeSimilarity(ssc1[:4], ssc2[:4])+0.5*computeShapeCodeSimilarity(ssc1[4:], ssc2[4:])
    # 计算音码部分相似度和形码部分相似度然后根据权重计算音形码相似度
    soundSimi = computeSoundCodeSimilarity(ssc1[:4], ssc2[:4])
    shapeSimi = computeShapeCodeSimilarity(ssc1[4:], ssc2[4:])
    return soundWeight * soundSimi + shapeWeight * shapeSimi


if __name__ == "__main__":
    print(computeSSCSimilarity(ssc_new.getSSCCode("品"), ssc_new.getSSCCode("拼")))