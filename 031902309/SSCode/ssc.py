# coding=utf-8
# sound_shape_code
import pypinyin
# 获取四角编码
from FourCornerCode import four_corner
from pypinyin import pinyin



# 设置相似度以计算是否可以实现变形字匹配
SIMILARITY_ANALYSIS = 0.8

yun_mu = {
    'a': '1', 'o': '2', 'e': '3', 'i': '4',
    'u': '5', 'v': '6', 'ai': '7', 'ei': '7',
    'ui': '8', 'ao': '9', 'ou': 'A', 'iou': 'B',  # 有：you->yiou->iou->iu
    'ie': 'C', 've': 'D', 'er': 'E', 'an': 'F',
    'en': 'G', 'in': 'H', 'un': 'I', 'vn': 'J',  # 晕：yun->yvn->vn->ven
    'ang': 'F', 'eng': 'G', 'ing': 'H', 'ong': 'K'
}
sheng_mu = {
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


def getSoundCode(zh_word):
    sound_code = []
    # style拼音风格，heteronym是否启动多音字，strict只获取声母或者韵母相关拼音
    sheng_mu_code = pinyin(zh_word, style=pypinyin.INITIALS, heteronym=False, strict=False)[0][0]
    # 如果目标汉字声母不在已有声母集合中
    if sheng_mu_code not in sheng_mu:
        sheng_mu_code = '0'
    
    yun_mu_code = pinyin(zh_word, style=pypinyin.FINALS, heteronym=False, strict=True)[0][0]
    print(yun_mu_code)


if __name__ == "__main__":
    getSoundCode("汉")




