from pypinyin import pinyin
from typing import Dict


class Trie:
    def __init__(self):
        self.dict_trie = {}
        self.source_result = {}
        self.key_result = {}

    def match(self, sentence: str, line: int):
        # 用于存放敏感词
        match_list = []
        # 用于存放源词即存在伪装
        source_match_list = []
        state_list = []
        temp_match = ""

        for word_pos, char in enumerate(sentence):
            # 如果存在敏感词的话添加对应的字典树加以判断
            if char in self.dict_trie:
                state_list.append(self.dict_trie)
                temp_match = ""

            for index, state in enumerate(state_list):
                # 如果存在敏感词组成部分
                if char in state:
                    state_list[index] = state[char]
                    temp_match += char
                    # 是否存在结束
                    if state[char]["is_end"]:
                        match_list.append("Line"+str(line)+":<"+temp_match+"> ")
                        # 由于敏感词之间存在重叠需要鉴别，不加以鉴别会出现重叠部分
                        if len(state[char].keys()) == 1:
                            state_list.pop(index)
                            temp_match = ""
                else:
                    state_list.pop(index)
                    temp_match = ""

        self.key_result = match_list

    def insertKey(self, keyword):
        # 形成字典树的新根
        # 将可能的中文转为英文并存储
        keyword = pinyin(keyword)[0][0]
        trie = self.dict_trie
        length = len(keyword)
        for i in range(0, length):
            # 用于判断敏感词部分是否存在，用于节省空间搭建字典树
            part = keyword[i]
            # 存在则直接赋值
            if part in trie:
                sub_trie = trie[part]
                trie = sub_trie
            # 不存在需要构建新子字典树
            else:
                new_sub_trie: Dict[str, bool] = {"is_end": False}
                # 再合适位置插入新的字典树
                trie[part] = new_sub_trie
                # 以新子字典树为依据向下蔓延
                trie = new_sub_trie
            if i == length - 1:
                trie["is_end"] = True

    def output(self):
        length: int = len(self.key_result)
        print('Total:%d' % length)
        for index, element in enumerate(self.key_result):
            print(element)


if __name__ == "__main__":
    dfa = Trie()
    dfa.insertKey("匹配")
    dfa.insertKey("匹配算法")
    tmp = ["匹配关键词", "匹配算法", "信息抽取", "匹配", "息气"]
    dfa.match("息气 信息抽取之 DFA 算法匹配关键词，匹配算法, 匹配 息气", 1)
    dfa.output()
