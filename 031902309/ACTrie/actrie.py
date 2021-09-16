import re

from xpinyin import Pinyin


class Node(object):
    """节点类"""

    def __init__(self):
        self.children = dict()
        # 存放当前敏感词组合序列的部分
        self.word = ""
        # 存放源敏感词未经任何修改
        self.source = ""
        self.fail = None
        self.tail = None
        self.length = 0


class Trie(object):
    """ac 自动机"""

    def __init__(self):
        self.root = Node()
        # 用于处理汉字拼音
        self.p_worker = Pinyin()
        # 用于存放汉字，汉字拼音和拼音首字母部分
        self.str_matrix = []
        # 存放相关的词组序列
        self.phrase_list = []
        # 用于存放匹配的组合内容
        self.combination = []

    # phrase_store为敏感词列表
    def prepareWork(self, phrase_store):
        # phrase为单个敏感词，未经组合的敏感词
        for index, phrase in enumerate(phrase_store):
            if index == len(phrase_store) - 1:
                self.str2matrix(phrase)
            else:
                self.str2matrix(phrase[:-1])
            # word为敏感词经过组合过的单个词语
            for word in self.phrase_list:
                if index == len(phrase_store) - 1:
                    self.build_tree(word, phrase)
                else:
                    self.build_tree(word, phrase[:-1])
        # 构建失败指针
        self.make_fail()

    # 将敏感词转换为对应的矩阵便于后续插入字典树中
    def str2matrix(self, phrase):
        # 获取汉字对应的拼音以及对应的首字母
        # alpha为单个汉字或者英文字母注意
        for letter in phrase:
            self.str_matrix.append(['['+self.p_worker.get_pinyin(letter).replace('-', '')+']',
                                    self.p_worker.get_pinyin(letter).replace('-', ''),
                                    str.lower(self.p_worker.get_initials(letter).replace('-', ''))])
        self.insertKey(len(phrase))

    def insertKey(self, layer: int):
        # 递归建树，获取每一行的
        self.recursionInsertKey(0, layer, "")
        self.str_matrix.clear()

    # 递归建树将汉字、拼音以及拼音首字母合在一起，例如"汉字", ”汉Z",...
    def recursionInsertKey(self, row_now: int, layer: int, phrase: str):
        if row_now == layer:
            self.phrase_list.append(phrase)
            return
        else:
            for column_now in range(0, 3):
                self.recursionInsertKey(row_now + 1, layer,
                                        phrase + self.str_matrix[row_now][column_now])

    # phrase为单个组合过的敏感词，initial为源敏感词即没有经过组合的敏感词
    def build_tree(self, phrase, initial: str):
        """构建字典树"""
        tmp_root = self.root
        # 用于组成拼音板块的makeup和count判别
        makeup = ''
        length = 0
        together = 0
        # letter表示敏感词组合过的词语的单个（汉字，字母
        for i in range(0, len(phrase)):
            # 因为需要完整的拼音串所以将拼音串添加到[]中然后提取即makeup为重组的拼音串
            if phrase[i] == '[':
                together = True
                continue
            if phrase[i] == ']':
                together = False
                length += 1
                if makeup not in tmp_root.children:
                    node = Node()
                    node.word = makeup
                    tmp_root.children.update({makeup: node})
                # 存在不存在均要转换成子节点
                tmp_root = tmp_root.children[makeup]
                makeup = ""
                continue

            if together:
                makeup += phrase[i]
                continue
            else:
                length += 1
                makeup = phrase[i]
                if makeup not in tmp_root.children:
                    node = Node()
                    node.word = makeup
                    tmp_root.children.update({makeup: node})
                # 存在不存在均要转换成子节点
                tmp_root = tmp_root.children[makeup]
                makeup = ""

        if tmp_root.source == "":
            # 为当前末尾节点添加源词
            tmp_root.source = initial
        # 为当前末尾节点添加当前敏感词组合序列的长度
        tmp_root.length = length

    # 构建fail指针
    def make_fail(self):
        tmp_que = [self.root]
        while len(tmp_que) != 0:
            # 开始遍历子节点
            sub_root = tmp_que.pop(0)
            # p = None
            for key, value in sub_root.children.items():
                # 将子节点的fail指针指向root节点
                if sub_root == self.root:
                    sub_root.children[key].fail = self.root
                else:
                    p = sub_root.fail
                    while p is not None:
                        if key in p.children:
                            sub_root.children[key].fail = p.fail
                            break
                        p = p.fail
                    if p is None:
                        sub_root.children[key].fail = self.root
                tmp_que.append(sub_root.children[key])

    def search(self, sentence, line):
        # index_store用于存储相应的匹配开始的下标，主要用于避免关键词重叠
        # 用于筛选关键字避免出现添加关键字的子集情况
        # start用于辅助纠正关键字重叠的情况
        index_store = []
        tmp = self.root
        for index, letter in enumerate(sentence):
            if self.illegalWord(letter):
                # 说明匹配已经开始，非法字符可以通过，中文中插入数字字符则不能通过
                continue
            letter = self.p_worker.get_pinyin(letter).replace('-', '')
            while tmp.children.get(str.lower(letter)) is None and tmp.fail is not None:
                tmp = tmp.fail
            # 匹配开始
            if tmp.children.get(str.lower(letter)) is not None:
                tmp = tmp.children.get(str.lower(letter))
            # 如果temp的fail为空，代表temp为root节点，
            # 没有在树中找到符合的敏感字，故跳出循环，检索下个字符
            else:
                continue
            # 如果检索到当前节点的长度信息存在，则代表搜索到了敏感词，打印输出即可
            if tmp.length:
                # af_start用于判别上一原文敏感词是否属于当前原文敏感词内容
                af_start = self.matched(node=tmp, sentence=sentence, cur_pos=index, line=line)
                if len(index_store):
                    if af_start == index_store[len(index_store) - 1]:
                        # 说明上个原文敏感词还真是当前敏感词的子集
                        self.combination.pop(len(self.combination) - 2)
                index_store.append(af_start)

    # 利用节点存储的字符长度信息，打印输出敏感词及其在搜索串内的坐标
    def matched(self, node, sentence, cur_pos, line: int) -> int:
        # cur_pos变化后用于计算开始匹配的内容下标用于去除重叠的子集
        # 用于存放匹配到的对应内容
        matched_part = ""
        word_length = node.length
        while word_length:
            # 非法字符不计入总个数
            if self.illegalWord(sentence[cur_pos]):
                matched_part = matched_part + sentence[cur_pos]
            # 正常字符需要减一即反向获取对应的内容
            else:
                matched_part = matched_part + sentence[cur_pos]
                word_length -= 1
            # 正常字符向后退
            cur_pos -= 1
        matched_part = matched_part[::-1]
        # 用于检验是否含有中文，如果含有中文那么如果夹杂数学字符则非敏感词，返回-1
        for letter in matched_part:
            if '\u4e00' <= letter <= '\u9fff':
                # 确实有中文那么检验是否有数字
                digit_contain = bool(re.search(r'\d', matched_part))
                if digit_contain:
                    return -1
        # 向容器中添加结果
        self.combination.append("Line" + str(line) + ": <" + node.source + "> " + matched_part)
        return cur_pos

    @staticmethod
    def illegalWord(letter) -> bool:
        if letter in "0123456789[\"`~!@#$%^&*()+=|{}':;',\\.<>/?~！@#￥%……&*（）——+| {}【】‘；：”“’。，、？_] \n":
            return True
        return False

    def writeFile(self, file_name):
        f = open(file_name, "a", encoding="utf-8")
        f.write("Total: " + str(len(self.combination)) + "\n")
        for element in self.combination:
            f.write(element + "\n")
        f.close()
        pass


if __name__ == "__main__":
    test_words = ["sub\n", "垃圾"]
    test_text = "拉圾网站，我这里有盗@#版软件。su*&b"
    model = Trie()
    model.prepareWork(test_words)
    model.search(test_text, 1)
    model.writeFile('ans.txt')
