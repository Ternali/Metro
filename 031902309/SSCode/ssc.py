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

yun_muDict = {
    'a': '1', 'o': '2', 'e': '3', 'i': '4',
    'u': '5', 'v': '6', 'ai': '7', 'ei': '7',
    'ui': '8', 'ao': '9', 'ou': 'A', 'iou': 'B',  # 有：you->yiou->iou->iu
    'ie': 'C', 've': 'D', 'er': 'E', 'an': 'F',
    'en': 'G', 'in': 'H', 'un': 'I', 'vn': 'J',  # 晕：yun->yvn->vn->ven
    'ang': 'F', 'eng': 'G', 'ing': 'H', 'ong': 'K'
}
sheng_muDict = {
    'b': '1', 'p': '2', 'm': '3', 'f': '4',
    'd': '5', 't': '6', 'n': '7', 'l': '7',
    'g': '8', 'k': '9', 'h': 'A', 'j': 'B',
    'q': 'C', 'x': 'D', 'zh': 'E', 'ch': 'F',
    'sh': 'G', 'r': 'H', 'z': 'E', 'c': 'F',
    's': 'G', 'y': 'I', 'w': 'J', '0': '0'
}
shapeDict = {'⿰': '1', '⿱': '2', '⿲': '3', '⿳': '4', '⿴': '5',  # 左右结构、上下、左中右、上中下、全包围
             '⿵': '6', '⿶': '7', '⿷': '8', '⿸': '9', '⿹': 'A',  # 上三包、下三包、左三包、左上包、右上包
             '⿺': 'B', '⿻': 'C', '0': '0'}  # 左下包、镶嵌、独体字：0
strokesDict = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A',
               11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K',
               21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U',
               31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 0: '0'}

zhStrokeDict = {}  # 汉字对应笔画数
zhStructureDict = {}  # 汉字对应形体结构


def getSoundCode(zh_word):
    sound_code = []
    # style拼音风格，heteronym是否启动多音字，strict只获取声母或者韵母相关拼音
    sheng_mu_code = pinyin(zh_word, style=pypinyin.INITIALS, heteronym=False, strict=False)[0][0]
    # 如果目标汉字声母不在已有声母集合中
    if sheng_mu_code not in sheng_muDict:
        sheng_mu_code = '0'

    yun_mu_code = pinyin(zh_word, style=pypinyin.FINALS_TONE3, heteronym=False, strict=True)[0][0]

    # 用于获取音调和去除韵母中音调
    yin_diao = '0'
    # 用于去除韵母中音调部分
    if yun_mu_code[-1] in ['1', '2', '3', '4']:
        yin_diao = yun_mu_code[-1]
        yun_mu_code = yun_mu_code[:-1]

    # 汇聚成音码
    if yun_mu_code in yun_muDict:
        # 按照顺序:声母，韵母辅音补码，韵母，音调
        sound_code.append(yun_muDict[yun_mu_code])
        sound_code.append(sheng_muDict[sheng_mu_code])
        sound_code.append('0')
    # 由于可能声母和韵母之间有补码位需要区分
    elif len(yun_muDict) > 1:
        # 获取不含补码位的韵母
        sound_code.append(yun_muDict[yun_mu_code[1:]])
        sound_code.append(sheng_muDict[sheng_mu_code])
        # 添加韵母补码位进去
        sound_code.append(yun_muDict[yun_mu_code[0]])
    # 仅有一位补码位没有韵母
    else:
        sound_code.append('0')
        sound_code.append(sheng_muDict[sheng_mu_code])
        # 添加韵母补码位
        sound_code.append('0')
    # 补充音调码
    sound_code.append(yin_diao)
    return sound_code


def getShapeCode(zh_word):
    shape_code = []
    structureShape = zhStructureDict.get(zh_word, '0')  # 获取对应形体结构
    shape_code.append(shapeDict[structureShape])
    # 获取对应汉字四角编码
    fc_code = fc_coder.query(zh_word)
    # 判断四角编码是否为空一般不为空
    if fc_code is None:
        shape_code.extend(['0', '0', '0', '0', '0'])
    else:
        shape_code.extend(fc_code[:])
    # 获取汉字对应笔画数
    # 并添加至形码
    strokes = zhStrokeDict.get(zh_word, '0')
    if int(strokes) > 35:
        shape_code.append('Z')
    else:
        shape_code.append(strokesDict[int(strokes)])
    return shape_code


# 获取汉字笔画数
def getZHStrokesDict():
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
    readFilePath = pkg_resources.resource_filename(__name__, "../zh_data/unihan_structure.txt")
    writeFilePath = pkg_resources.resource_filename(__name__, "../zh_data/hanzi_ssc_res.txt")
    writeFile = open(writeFilePath, "w", encoding='UTF-8')
    with open(readFilePath, 'r', encoding='UTF-8') as f:  # 文件特征：U+4EFF\t仿\t⿰亻方\n
        for line in f:
            line = line.split()
            soundCode = getSoundCode(line[1])
            shapeCode = getShapeCode(line[1])
            ssc = "".join(soundCode + shapeCode)
            if ssc != '00000000000':
                writeFile.write(line[0] + "\t" + line[1] + "\t" + ssc + "\n")
    writeFile.close()


zhSSCDict = {}  # 汉字音形码


# 汉字对应的音形码插入字典
def getZHSSCDict():
    filepath = pkg_resources.resource_filename(__name__, "../zh_data/hanzi_ssc_res.txt")
    f = open(filepath, 'r', encoding="UTF-8")
    for line in f:
        line = line.split()
        zhSSCDict[line[1]] = line[2]
    f.close()


# 获取汉字对应的音形码
def getSSCCode(zh_word):
    soundCode = getSoundCode(zh_word)
    shapeCode = getShapeCode(zh_word)
    ssc = "".join(soundCode + shapeCode)
    return ssc


if __name__ == "__main__":
    print(getSoundCode("水"))
    print(getShapeCode("水"))
    print(getSSCCode("水"))
