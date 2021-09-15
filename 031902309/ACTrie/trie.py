from typing import List
from xpinyin import Pinyin


class Trie:
    """
    """

    def __init__(self):
        self.root = {}
        self.strMatrix = []
        self.strMatrix: List[List[str]]
        self.p_worker = Pinyin()
        # 此处result_dict仅仅存放敏感词
        self.result_store = []
        # 此处仅存放敏感词对应的文章中的内容
        self.passage_store = []
        # 存放敏感词对应的行数
        self.line_store = []

    # 将敏感词转换为对应的矩阵便于后续插入字典树中
    def str2matrix(self, zh_words):
        # 获取汉字对应的拼音以及对应的首字母
        for zh_word in zh_words:
            self.strMatrix.append([zh_word, self.p_worker.get_pinyin(zh_word).replace('-', ''),
                                   self.p_worker.get_initials(zh_word).replace('-', '')])
        self.insertKey(len(zh_words), zh_words)

    def insertKey(self, layer: int, zh_words: str):
        # 递归建树，获取每一行的
        for i in range(0, layer):
            self.recursionInsertKey(i, layer, self.root, zh_words)
        self.strMatrix.clear()

    # 递归建树将汉字、拼音以及拼音首字母合在一起，例如{"汉: {"z": {"i": {"汉字": True}}},...
    def recursionInsertKey(self, row_now: int, layer: int, tmp_root, zh_words: str):
        if row_now == layer:
            tmp_root.update({zh_words: True})
            return
        else:
            for column_now in range(0, 3):
                # 用sub_tmp_root替代tmp_root以避免发生变根性错误
                sub_tmp_root = tmp_root
                # 获取每一行每一列的字用于建树
                for index, inner_part in enumerate(self.strMatrix[row_now][column_now]):
                    # 如果不存在该敏感词
                    if inner_part not in sub_tmp_root:  # 原先为tmp_root
                        sub_tmp_root.update({inner_part: {}})
                        sub_tmp_root = sub_tmp_root[inner_part]
                    # 存在敏感词直接替换对应的子节点即可
                    else:
                        sub_tmp_root = sub_tmp_root[inner_part]
                # 递归建树，如果是最后部分则插入敏感词，搜索完毕后直接返回敏感词
                self.recursionInsertKey(row_now + 1, layer, sub_tmp_root, zh_words)

    # 搜索关键字
    def searchKey(self, sentence: str, line_number: int):
        # 获取敏感词词典树根
        trie_root = self.root
        # 是否初次匹配的决定因素
        matched = False
        # 是否中文的决定因素
        zh_word = False
        # 用于组成原文内容
        tmp_phrase = ""
        for element in sentence:
            # 说明非法字符是夹杂在词语中间的
            # 判断是否非法字符且夹在匹配内容中
            if element in "[\"`~!@#$%^&*()+=|{}':;',\\.<>/?~！@#￥%……&*（）——+| {}【】‘；：”“’。，、？_]":
                if matched:
                    tmp_phrase += element
                continue
            # 判断当前内容是否在敏感词词典树中
            # 首先进行判断是否汉字，是汉字转换成对应的拼音特别，英文直接处理即可
            if '\u4e00' <= element <= '\u9fff':
                zh_word = True

    # 写入目标文件
    def output(self, file_name: str):
        f = open(file_name, "w", encoding="utf-8")
        length = len(self.line_store)
        f.write("Total: %d" % length)
        for index in range(0, length):
            f.write("Line%d: <%s> %s" % (self.line_store[index], self.result_store[index], self.passage_store[index]))


if __name__ == "__main__":
    tmp = Trie()
    tmp.str2matrix("发拆")
    print(tmp.root)
    keys = tmp.root.keys()
    print(keys)
