from typing import Dict
from typing import List
from xpinyin import Pinyin
# 测试三和一大树的成长过程
# 这是一个异常艰难的过程要做到三个合二为一几乎不可能(
trie = {}
p = Pinyin()
# 这是要做到汉字，拼音和拼音首字母大写
# trie: Dict[List[str],bool] 可能是这个类型基于字典树的类型确实有点怪，
# 有点像C++ unordered_map<unordered_map<string,bool>, bool>但又不太像
word = "中文"
new_sub_trie: Dict[str, bool] = {"is_end": False}
tmp_list = [word[0], p.get_pinyin(word[0]), p.get_initial(word[0])]
print(tmp_list)

