from typing import List
from typing import Dict
from xpinyin import Pinyin


class Trie:
    """
    """

    def __init__(self):
        self.root = {}
        self.strMatrix = []
        self.strMatrix: List[List[str]]
        self.p_worker = Pinyin()

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
                    if inner_part not in tmp_root:
                        sub_tmp_root.update({inner_part: {}})
                        sub_tmp_root = sub_tmp_root[inner_part]
                    # 存在敏感词直接替换对应的子节点即可
                    else:
                        sub_tmp_root = sub_tmp_root[inner_part]
                # 递归建树，如果是最后部分则插入敏感词，搜索完毕后直接返回敏感词
                self.recursionInsertKey(row_now + 1, layer, sub_tmp_root, zh_words)


if __name__ == "__main__":
    tmp = Trie()
    tmp.str2matrix("汉字")
    print(tmp.root)
    keys = tmp.root.keys()
    print(keys)
