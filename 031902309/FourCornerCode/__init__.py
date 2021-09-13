import pickle
import pkg_resources

# 5位16进制共有20位2进制
class FourCorner:
    """
    :type
    """
    # 读取已有汉字四角编码
    def __init__(self):
        data_file = pkg_resources.resource_filename(__name__, "../data/data.pkl")
        f = open(data_file, 'rb')
        self.data = pickle.load(f)
        f.close()

    # 获取对应汉字的四角编码
    def query(self, zh_word):
        """
        :param zh_word:
        :return:
        """
        return str(self.data.get(zh_word))[:-1]



