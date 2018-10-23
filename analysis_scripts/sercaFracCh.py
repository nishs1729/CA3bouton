#!/usr/bin/python

from numpy import *
from scipy.integrate import *
from random import randint
import os, sys
from time import time
from peaks import *
from pylab import *

class analysis:

    #   Set dataPath and resultPath
    def __init__(self, dp, rp):
        self.dataPath = dp
        self.resultPath = rp

    def sercaFracCh(self, vdcc, inFile='/sercaMol.dat', showFig=False):
        data = genfromtxt(self.resultPath + inFile, usecols=(0,2,3,4,5), unpack=True)
        caOcc = vstack((data[0], data[1] + data[4] + 2*(data[2] + data[3])))

        # get peaks
        maxId = detect_peaks(caOcc[1], mph=4, mpd=500, threshold=0, show=showFig)
        minId = detect_peaks(caOcc[1], mph=-80000, mpd=1000, threshold=0, valley=True, show=showFig)
        maxValue = [caOcc[1][i] for i in maxId]
        minValue = [caOcc[1][i] for i in minId]

        print maxValue[0] - minValue[0], maxValue[1] - minValue[1], vdcc

if __name__ == '__main__':
    if len(sys.argv)<2:
        dataDirName = "RSI20V80"
    else:
        dataDirName = sys.argv[1]

    for v in arange(50,170,10):
        dataDirName = "RSI20V" + str(v)
        vdcc = int(dataDirName.split("V")[1])
        dataType = "ppf/"
        path = "/media/nishant/4tb/output/" + dataType + dataDirName

        dataPath = path
        resultPath = "/home/nishant/Lab/results/" + dataType + dataDirName

        n = analysis(dataPath, resultPath)
        n.sercaFracCh(vdcc, showFig=True)
