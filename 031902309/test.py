from ACTrie.actrie import Trie

AcTrie = Trie()
# 测试无修改
word_store = ["中文"]
AcTrie.prepareWork(word_store)
AcTrie.search("中文", line=1)
assert AcTrie.combination[0] == "Line1: <中文> 中文"
# 中文中插入非法字符
AcTrie.search("中*文", line=1)
assert AcTrie.combination[1] == "Line1: <中文> 中*文"
# 中文插入字母，数字
AcTrie.search("中a文 中1文", line=1)
assert len(AcTrie.combination) == 2
# 中文采用谐音，拼音以及首字母
AcTrie.search("种文", line=1)
assert AcTrie.combination[2] == "Line1: <中文> 种文"
AcTrie.search("中wen", line=1)
assert AcTrie.combination[3] == "Line1: <中文> 中wen"
AcTrie.search("中w", line=1)
assert AcTrie.combination[4] == "Line1: <中文> 中w"
# 英文插入字符
word_store.clear()
word_store = ["ch"]
AcTrie.prepareWork(word_store)
AcTrie.search("c**h", line=1)
assert AcTrie.combination[5] == "Line1: <ch> c**h"
# 英文插入数字
AcTrie.search("c23h", line=1)
assert AcTrie.combination[6] == "Line1: <ch> c23h"
# 英文大小写变化
AcTrie.search("CH", line=1)
assert AcTrie.combination[7] == "Line1: <ch> CH"
