import pickle
import pkg_resources


class FourConrner:
    # 读取已有汉字四角编码
    def __init__(self):
        data_file = pkg_resources.resource_filename(__name__, "data/data.pkl")
        f = open(data_file, 'rb')
        self.data = pickle.load(f)

    # 获取对应汉字的四角编码
    def query(self, hanzi):
        return self.data.get(hanzi)
