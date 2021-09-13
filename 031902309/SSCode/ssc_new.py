# coding=utf-8
# sound_shape_code
import pkg_resources
import pypinyin
# 获取四角编码
from FourCornerCode import FourCorner
from pypinyin import pinyin

fc_coder = FourCorner()
# 设置相似度以计算是否可以实现变形字匹配
SIMILARITY_ANALYSIS = 0.8

# 韵母部分占5位，包含补码
yun_muDict = {
    'a': '00000', 'ai': '00001', 'ao': '00011', 'an': '00010', 'ang': '00010',
    'i': '00111', 'ie': '00101', 'iu': '00100', 'in': '01100',
    'ing': '01100', 'o': '01111', 'ou': '01110', 'ong': '01010',
    'e': '01001', 'ei': '01000', 'er': '11000', 'en': '11001',
    'eng': '11001', 'u': '11010', 'ui': '11110', 'un': '11111',
    'v': '11100', 've': '10100', 'vn': '10101'
}  # ü替代为v
# 声母部分占5位
sheng_muDict = {
    'b': '00000', 'p': '00001', 'm': '00011', 'f': '00010',
    'd': '00111', 't': '00101', 'n': '00100', 'l': '01100',
    'g': '01111', 'k': '01110', 'h': '01010', 'j': '01001',
    'q': '01000', 'x': '11000', 'zh': '11011', 'ch': '11010',
    'sh': '11110', 'r': '11111', 'z': '11011', 'c': '11010',
    's': '11110'
}
# 字形部分占4位
shapeDict = {'⿰': '0001', '⿱': '0010', '⿲': '0011', '⿳': '0110', '⿴': '1110',  # 左右结构、上下、左中右、上中下、全包围
             '⿵': '1100', '⿶': '1101', '⿷': '1111', '⿸': '0111', '⿹': '0100',  # 上三包、下三包、左三包、左上包、右上包
             '⿺': '0101', '⿻': '1010', '0': '0000'}  # 左下包、镶嵌、独体字：0
strokesDict = {1: '0000000000000001',
               2: '0000000000000011',
               3: '0000000000000111',
               4: '0000000000001111',
               5: '0000000000011111',
               6: '0000000000111111',
               7: '0000000001111111',
               8: '0000000011111111',
               9: '0000000111111111',
               10: '0000001111111111',
               11: '0000011111111111',
               12: '0000111111111111',
               13: '0001111111111111',
               14: '0011111111111111',
               15: '0111111111111111',
               16: '1111111111111111',
               }

zhStrokeDict = {}  # 汉字对应笔画数
zhStructureDict = {}  # 汉字对应形体结构


def getSoundCode(zh_word):
    """
    :param zh_word:
    :return:
    """
    sound_code = []
    # style拼音风格，heteronym是否启动多音字，strict只获取声母或者韵母相关拼音
    sheng_mu_code = pinyin(zh_word, style=pypinyin.INITIALS, heteronym=False, strict=False)[0][0]
    # 如果目标汉字声母不在已有声母集合中
    # print(sheng_mu_code)用于测试声母
    if sheng_mu_code not in sheng_muDict:
        sheng_mu_code = '00000'

    yun_mu_code = pinyin(zh_word, style=pypinyin.FINALS_TONE3, heteronym=False, strict=True)[0][0]

    # 用于获取音调和去除韵母中音调，提前声明以防止尴尬情况发生
    yin_diao = '0'
    # 用于去除韵母中音调部分
    if yun_mu_code[-1] in ['1', '2', '3', '4']:
        yin_diao = yun_mu_code[-1]
        if yin_diao == '1':
            yin_diao = '00'
        elif yin_diao == '2':
            yin_diao = '01'
        elif yin_diao == '3':
            yin_diao = '10'
        else:
            yin_diao = '11'
        yun_mu_code = yun_mu_code[:-1]
    else:
        yin_diao = '00'
        yun_mu_code = yun_mu_code[:-1]

    # print(yin_diao)用于测试音调
    # print(yun_mu_code)用于测试韵母
    # 汇聚成音码
    if yun_mu_code in yun_muDict:
        sound_code.append(sheng_muDict[sheng_mu_code])
        # 按照顺序:声母，韵母辅音补码，韵母，音调
        sound_code.append(yun_muDict[yun_mu_code])
        sound_code.append('00000')
    # 由于可能声母和韵母之间有补码位需要区分
    elif len(yun_mu_code) > 1:
        sound_code.append(sheng_muDict[sheng_mu_code])
        # 获取不含补码位的韵母
        sound_code.append(yun_muDict[yun_mu_code[1:]])
        # 添加韵母补码位进去
        sound_code.append(yun_muDict[yun_mu_code[0]])
    # 仅有一位补码位没有韵母
    else:
        sound_code.append(sheng_muDict[sheng_mu_code])
        sound_code.append('00000')
        # 添加韵母补码位
        sound_code.append('00000')
    # 补充音调码

    sound_code.append(yin_diao)
    return sound_code


def getShapeCode(zh_word):
    """
    :param zh_word:
    :return:
    """
    shape_code = []
    # 将对应的形体插入字典中
    getZHStructureDict()
    structureShape = zhStructureDict.get(zh_word, '0')  # 获取对应形体结构
    # print(structureShape)用于测试结构位原先对应数字
    shape_code.append(shapeDict[structureShape])
    # 获取对应汉字四角编码
    fc_code = fc_coder.query(zh_word)
    # print(fc_code)用于测试四角编码原先对应数字
    # 判断四角编码是否为空一般不为空
    if fc_code is None:
        shape_code.extend(['0000', '0000', '0000', '0000'])
    else:
        fc_code = getBin(fc_code)
        shape_code.extend(fc_code[:])
    # 获取汉字对应笔画数
    # 并添加至形码
    # 将对应的笔画插入字典中
    getZHStrokesDict()
    strokes = zhStrokeDict.get(zh_word, '0')
    # print(strokes)用于测试笔画原先对应数字
    if int(strokes) > 16:
        shape_code.append('0000000011111111')
    else:
        shape_code.append(strokesDict[int(strokes)])
    return shape_code


# 用于获取四角编码对应的2进制
def getBin(fc_code_param):
    """
    :param:fc_code_param:四角编码
    :return:
    """
    fc_code_result = []
    for num in fc_code_param:
        tmp_num = int(num)
        tmp_num = (str(bin(tmp_num))).replace('0b', '')
        for i in range(1, 5 - len(tmp_num)):
            tmp_num = "0" + tmp_num
        fc_code_result.append(tmp_num)
    return fc_code_result


# 获取汉字笔画数
def getZHStrokesDict():
    """
    :param
    """
    filepath = pkg_resources.resource_filename(__name__, "../zh_data/utf8_strokes.txt")
    # 获取已有汉字笔画数文件
    f = open(filepath, 'r', encoding='UTF-8')
    for line in f:
        line = line.split()
        # 往里头添加汉字笔画数键值对
        zhStrokeDict[line[1]] = line[2]
    f.close()


# 获取汉字结构
def getZHStructureDict():
    """
    :param
    """
    # 从已有文件中获取对应的结构形成键值对并插入
    filepath = pkg_resources.resource_filename(__name__, "../zh_data/unihan_structure.txt")
    f = open(filepath, 'r', encoding="UTF-8")
    for line in f:
        line = line.split()
        if line[2][0] in shapeDict:
            zhStructureDict[line[1]] = line[2][0]
    f.close()


# 形成汉字音形码文件
def createZHSSCFile():
    """
    :param
    """
    readFilePath = pkg_resources.resource_filename(__name__, "../zh_data/unihan_structure.txt")
    writeFilePath = pkg_resources.resource_filename(__name__, "../zh_data/hanzi_ssc_res.txt")
    writeFile = open(writeFilePath, "w", encoding='UTF-8')
    with open(readFilePath, 'r', encoding='UTF-8') as f:  # 文件特征：U+4EFF\t仿\t⿰亻方\n
        for line in f:
            line = line.split()
            soundCode = getSoundCode(line[1])
            shapeCode = getShapeCode(line[1])
            ssc = "".join(soundCode + shapeCode)
            if ssc != '000000000000000000000000000000000000000000000000000000000':
                writeFile.write(line[0] + "\t" + line[1] + "\t" + ssc + "\n")
    writeFile.close()


zhSSCDict = {}  # 汉字音形码


# 不推荐因为采用新的计算方式
# 汉字对应的音形码插入字典
def getZHSSCDict():
    """
    :param
    """
    filepath = pkg_resources.resource_filename(__name__, "../zh_data/hanzi_ssc_res.txt")
    f = open(filepath, 'r', encoding="UTF-8")
    for line in f:
        line = line.split()
        zhSSCDict[line[1]] = line[2]
    f.close()


# 获取汉字对应的音形码
def getSSCCode(zh_word):
    """
    :param zh_word:
    :return:
    """
    soundCode = getSoundCode(zh_word)
    shapeCode = getShapeCode(zh_word)
    ssc = "".join(soundCode + shapeCode)
    return ssc


# 测试代码相对应功能使用
if __name__ == "__main__":
    leng = 0
    for element in getShapeCode("汉"):
        leng += len(element)
    print(leng)