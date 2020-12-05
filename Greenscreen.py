from PIL import Image
from imageio import imread

class Greenscreen():
    def __init__(self, fgPath, bgPath):
        self.__fgMatrix = imread(fgPath)
        self.__bgMatrix = imread(bgPath)
        self.__outPixelList = None
        self.__outImage = None

    @staticmethod
    def __isGreen(pixel):
        r, g, b = pixel
        #if g > int(r) + int(b):
        return True if g > 110 and r < 115 and b < 115 else False

    def overlapImages(self, outputPath):
        if self.__outImage is None:
            totalLines = min(len(self.__fgMatrix), len(self.__bgMatrix))
            totalColumns = min(len(self.__fgMatrix[0]), len(self.__bgMatrix[0]))
            self.__outPixelList = [None]*(totalLines*totalColumns)
            for i in range(totalLines):
                self.__parseLine(i, totalColumns)
            self.__outImage = Image.new('RGB', (totalColumns, totalLines))
            self.__outImage.putdata(self.__outPixelList)
        self.__saveOutput(outputPath)

    def __saveOutput(self, outputPath):
        self.__outImage.save(outputPath)

    def __parseLine(self, lineIndex, totalColumns):
        for j in range(totalColumns):
            pixelsToBeAppended = tuple(self.__bgMatrix[lineIndex][j]) if Greenscreen.__isGreen(self.__fgMatrix[lineIndex][j]) \
                else tuple(self.__fgMatrix[lineIndex][j])
            self.__outPixelList[lineIndex*totalColumns+j] = pixelsToBeAppended


if __name__ == "__main__":
    Greenscreen("fg.jpg", "bg.jpg").overlapImages("combined.png")
