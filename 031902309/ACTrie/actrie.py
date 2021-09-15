from xpinyin import Pinyin


class Node:

    def __init__(self):
        self.children = {}  # 相当于指针，指向树节点的下一层节点
        self.fail = None  # 失配指针，这个是AC自动机的关键
        self.word = ""  # 用来储存标签
        self.word_length = set()  # 用来存储字符长度


class Trie:

    def __init__(self):
        # 用于存放汉字，汉字拼音和拼音首字母部分
        self.str_matrix = []
        #
        self.dict_trie = {}
        self.p_worker = Pinyin()
        self.root = Node()
        # 存放相关的词组序列
        self.phrase_list = []
        # 用于存放匹配的原文内容
        self.source_result = []
        # 用于存放匹配到的敏感词
        self.word_result = []
        # 用于存放对应的函数
        self.line_result = []

    def prepareWork(self, phrase_store):
        for phrase in phrase_store:
            self.str2matrix(phrase)
            for element in self.phrase_list:
                self.insert(element, phrase)
        self.makeFail()

    # 将敏感词转换为对应的矩阵便于后续插入字典树中
    def str2matrix(self, phrase):
        # 获取汉字对应的拼音以及对应的首字母
        # alpha为单个汉字或者英文字母注意
        for alpha in phrase:
            self.str_matrix.append([alpha, self.p_worker.get_pinyin(alpha).replace('-', ''),
                                    str.lower(self.p_worker.get_initials(alpha).replace('-', ''))])
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

    # 将所有模式串插入树中
    def insert(self, word, source: str):
        temp_root = self.root
        for part in word:
            # 如果不包含这个字符就创建孩子节点
            if part not in temp_root.children:
                temp_root.children[part] = Node()
            # temp指向孩子节点
            temp_root = temp_root.children[part]
            if temp_root.word == "":
                temp_root.word = source
        # 一个字符串遍历完了后，将其长度保存到最后一个孩子节点信息中
        temp_root.word_length.add(len(word))

    # 构建失败路径
    def makeFail(self):
        temp_que = [self.root]
        while len(temp_que) != 0:
            # 获取节点
            temp = temp_que.pop(0)
            # 获取孩子节点的所有键值信息
            iterators = temp.children.keys()
            for child_key in iterators:
                y = temp.children[child_key]
                fa_fail = temp.fail
                while fa_fail is not None and child_key not in fa_fail.children:
                    fa_fail = fa_fail.fail
                if fa_fail is None:
                    y.fail = self.root
                else:
                    y.fail = fa_fail.children[child_key]
                if y.fail.word_length is not None:
                    y.word_length.update(y.fail.word_length)
                temp_que.append(y)

    def search(self, s: str, line: int):
        tmp = self.root
        for index, element in enumerate(s):
            while tmp.children.get(element) is None and tmp.fail is not None:
                tmp = tmp.fail
            if tmp.children.get(element) is not None:
                tmp = tmp.children.get(element)
            # 如果temp的fail为空，代表temp为root节点，
            # 没有在树中找到符合的敏感字，故跳出循环，检索下个字符
            else:
                continue
            # 如果检索到当前节点的长度信息存在，则代表搜索到了敏感词，打印输出即可
            if len(tmp.word_length):
                self.matched(tmp, s, index, line)

    # 利用节点存储的字符长度信息，打印输出敏感词及其在搜索串内的坐标
    def matched(self, node, s, cur_pos, line: int):
        for word_len in node.word_length:
            start_index = cur_pos - word_len + 1
            match_part = s[start_index: cur_pos + 1]
            self.source_result.append(match_part)
            self.word_result.append(node.word)
            self.line_result.append(line)


if __name__ == "__main__":
    test_words = ["不知", "不觉", "忘了爱"]
    test_text = """不知、不觉·间我~|~已经忘lai❤。"""
    model = Trie()
    model.prepareWork(test_words)
    model.search(test_text, 1)
    print(model.source_result)
    print(model.word_result)
    print(model.line_result)
