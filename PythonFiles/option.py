import pickle
import os.path

class Option:
    def __init__(self):
        # 날씨
        self.beSunny    = False
        self.beRainy    = False
        self.beFoggy    = False
        self.beLighting = False
        # self.beCloudy   = False
        # self.beClear    = False
        # self.beDry      = False
        # self.beHumid    = False # 습함
        # self.beWindy    = False

        # 미세먼지
        self.beGreat = False
        self.beNormal = False
        self.beBad = False
        self.beTooBad = False

        # 온도
        self.beHot = False
        self.beCold = False

        self.load()

    def save(self):
        objects = self.__dict__
        print(objects)
        with open('option.sav', 'wb') as f:
            pickle.dump(objects, f)

    def load(self):
        if os.path.isfile('option.sav'):
            with open('option.sav', 'rb') as f:
                diction = pickle.load(f)
                self.__dict__.update(diction)
        else:
            print('No File')

    def changeOptions(self, str):
        optionDict = self.__dict__
        optionDict[str] = bool(1 - optionDict[str])
        self.__dict__.update(optionDict)
        return optionDict[str]


if __name__ == '__main__':
    o = Option()