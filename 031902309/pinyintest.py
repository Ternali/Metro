from xpinyin import Pinyin
from pypinyin import pinyin
import re

# 测试拼音包的功能
test = 'alpha'
tmp = pinyin(test)
# 得益于pinyin的处理方式需要这么提取
print(str(tmp[0][0]))

# 测试拼音包的处理用于比较做最终决定
p = Pinyin()
result = p.get_pinyin('真的假的')
print(result)
# 替换无用的-用来提取拼音
tmp_result = re.sub('-', '', result)
print(tmp_result)
# 用来切割每个汉字对应的读音
result = result.split('-')
print(result)

# 用以测试提取拼音首字母
result = p.get_initials("真的假的")
print(result)
# 替换无用的-用于提取拼音首字母
tmp_result = re.sub('-', '', result)
print(tmp_result)
# 用于切割每个汉字拼音首字母
result = result.split('-')
print(result)

# 对单个字进行测试
result = p.get_initial("真")
print(result)
result = p.get_pinyin("真")
print(result)

