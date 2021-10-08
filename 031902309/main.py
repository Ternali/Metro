import sys

from ACTrie.actrie import Trie

args = sys.argv
# 参数错误
if len(args) != 4:
    print("参数数目冗余或者缺失")
    exit(-1)
AcTrie = Trie()
work_store = []
try:
    f = open(args[1], encoding="utf-8")
    # 读取敏感词文件一次性读取所有行数
    word_store = f.readlines()
    f.close()
    # 开始插入敏感词到树中
    AcTrie.prepareWork(word_store)
    # 读入待检测文件
    f = open(args[2], encoding="utf-8")
    contents = f.readlines()
    f.close()
    # 开始匹配对应的字段
    for line, content in enumerate(contents):
        AcTrie.search(content, line + 1)
    # 写入到文件中
    AcTrie.writeFile(args[3])
except FileNotFoundError:
    print("文件不存在")

