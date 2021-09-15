from SSCSimilarityCompute.compute import Compute


class KMP(object):
    # thrshold为模糊度即使用模糊度匹配不使用完全匹配
    # 求模式串T的next函数（修正方法）值并存入next数组
    # nextVal = [-1]
    # startIdxRes = []#写在这里，多次使用kmp时startIdxRes不会被清空而是存放了上一次的数据，影响结果
    def __init__(self, threshold):
        self.threshold = threshold
        self.nextVal = [-1]
        self.startIdxRes = []

    def reset(self):
        self.nextVal = [-1]
        self.startIdxRes = []

    def indexKMP(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        """
        try:
            return haystack.index(needle)
        except:
            return -1
        """
        # 子串定位，即模式匹配，可采用BF算法  也可采用KMP算法，我采用KMP算法
        # 0<=pos<= len(strS) - len(strT)) + 1
        self.getNextVal(needle)
        i = 0
        while i < len(haystack):
            j = 0
            while i < len(haystack) and j < len(needle):
                if j == -1 or Compute(haystack[i], needle[j]) > self.threshold:
                    i += 1
                    j += 1
                else:
                    j = self.nextVal[j]
            if j == len(needle):
                self.startIdxRes.append(i - len(needle))

    # 求next数组用于匹配失败时使用
    def getNextVal(self, strT):
        i = 0
        j = -1
        while i < len(strT) - 1:
            if j == -1 or Compute(strT[i], strT[j]) > self.threshold:
                i += 1
                j += 1
                if i < len(strT) and Compute(strT[i], strT[j]) > self.threshold:
                    self.nextVal.append(self.nextVal[j])
                else:
                    self.nextVal.append(j)
            else:
                j = self.nextVal[j]


