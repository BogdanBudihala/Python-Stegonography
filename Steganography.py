from PIL import Image
from imageio import imread

class Steganographer():
    def __init__(self, fgPath, bgPath = None):
        self.__fgMatrix = imread(fgPath)
        self.__bgMatrix = imread(bgPath) if bgPath is not None else bgPath

    @staticmethod
    def __getStrippedPixel(pixel, isFgPixel=True):
        """
        :param pixel: Represents a list of 3 colors, RGB, each between [0, 255)
        :param isFgPixel: Represents a boolean that holds the information whether the pixel belongs to a foreground
        image or not
        :return: Returns the 'clean' version of the pixel, where the least significant 4 bits are 0 if the pixel
        belongs to foreground, else the most significant 4 bits are 0
        """
        return [colorValue//16*16 if isFgPixel else colorValue//16 for colorValue in pixel]

    @staticmethod
    def __getMergedPixels(fgPixel, bgPixel):
        return [fgPixel[i] + bgPixel[i] for i in range(len(fgPixel))]

    @staticmethod
    def __getSubtractedPixel(pixel, isFgPixel=True):
        """
        :param pixel: Represents a list of 3 colors, RGB, each between [0, 255)
        :param isFgPixel: Represents a boolean that holds the information whether the pixel belongs to a foreground
        image or not
        :return: Extracts the most significant (or least significant, promoted to most significant) 4 bits into a new
        color value and returns a new pixel
        """
        return [colorValue//16*16 if isFgPixel else (colorValue%16)*16 for colorValue in pixel]

    def extractImage(self, outputPath, extractFgImage=True):
        subtractionResultList = list()
        for i in range(len(self.__fgMatrix)):
            for j in range(len(self.__fgMatrix[i])):
                subtractionResultList.append(
                    tuple(Steganographer.__getSubtractedPixel(self.__fgMatrix[i][j], extractFgImage)))

        Steganographer.__saveOutput(subtractionResultList, outputPath, len(self.__fgMatrix[0]),
                                    len(self.__fgMatrix))

    def hideImage(self, outputPath):
        if self.__bgMatrix is None:
            raise Exception("Method requires an instance with both constructor parameters")

        outputPixelList = list()
        strippedFgMatrix = Steganographer.__getStrippedImage(self.__fgMatrix, True)
        strippedBgMatrix = Steganographer.__getStrippedImage(self.__bgMatrix, False)

        for i in range(len(strippedFgMatrix)):
            for j in range(len(strippedFgMatrix[i])):
                if i < len(strippedBgMatrix) and j < len(strippedBgMatrix[0]):
                    outputPixelList.append(tuple(Steganographer.__getMergedPixels(strippedFgMatrix[i][j],
                                                                                  strippedBgMatrix[i][j])))
                else:
                    outputPixelList.append(tuple(strippedFgMatrix[i][j]))

        Steganographer.__saveOutput(outputPixelList, outputPath, len(strippedFgMatrix[0]), len(strippedFgMatrix))

    @staticmethod
    def __saveOutput(listOfPixels, outputPath, width, height):
        imageToSave = Image.new('RGB', (width, height))
        imageToSave.putdata(listOfPixels)
        imageToSave.save(outputPath)

    @staticmethod
    def __getStrippedImage(imageMatrixToStrip, isFgImage=True):
        imageMatrixCopy = imageMatrixToStrip[:]
        for i in range(len(imageMatrixToStrip)):
            for j in range(len(imageMatrixToStrip[i])):
                imageMatrixCopy[i][j] = Steganographer.__getStrippedPixel(imageMatrixToStrip[i][j], isFgImage)
        return imageMatrixCopy

if __name__ == "__main__":
    mySteg = Steganographer('fg.png', 'bg.png')
    mySteg.hideImage("hiddenImage.png")

    myNewSteg = Steganographer("hiddenImage.png")
    myNewSteg.extractImage("extractedBg.png", False)
    myNewSteg.extractImage("extractedFg.png", True)


