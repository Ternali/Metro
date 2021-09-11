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
#替换无用的-用来提取拼音
result = re.sub('-', '', result)
print(result)

