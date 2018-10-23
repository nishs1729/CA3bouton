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
        
    #   Get list of directories in the path starting with 's_'
    def getDirs(self, path, sstr='s_'):
        dirs = [d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d]
        dirs.sort()
        return(dirs)

    def caSercaPeak(self, showFig=False):
    
        dirs = self.getDirs(self.dataPath)
        self.seeds = len(dirs)
        print self.seeds
        
        data = []
        for d in dirs[1001:2000]:
            caData = genfromtxt(self.dataPath + "/" + d + "/dat/ca.dat", usecols=(2), unpack=True)
            caData = caData/602.3
            #print caData
            
            sd = genfromtxt(self.dataPath + "/" + d + "/dat/serca_mol.dat", usecols=(0,2,3,4,5), unpack=True)
            sercaData = (sd[1] + sd[4] + 2*(sd[2] + sd[3]))/8678
            #print sercaData
            
            # get peaks
            caMaxId = detect_peaks(caData, mph=1, mpd=500, threshold=0, show=showFig)
            caMax = caData[caMaxId]
            
            sercaMaxId = detect_peaks(sercaData, mph=0.1, mpd=1500, threshold=0, show=showFig)
            sercaMaxId = [i for i in sercaMaxId if i<1000 or (i>4000 and i<5000)]
            sercaMax = sercaData[sercaMaxId]
            
            data.append(array(zip(caMax, sercaMax)).flatten())
            print caMax, sercaMax
        
        print data
        r = open(self.resultPath + '/caSercaPeak.dat', 'a')
        savetxt(r, data, fmt='%0.4f', delimiter="\t")


if __name__ == '__main__':
    if len(sys.argv)<2:
        dataDirName = "RSI20V80"
    else:
        dataDirName = sys.argv[1]

    vdcc = int(dataDirName.split("V")[1])
    dataType = "ppf/"
    path = "/media/nishant/4tb/output/" + dataType + dataDirName

    dataPath = path
    resultPath = "/home/nishant/Lab/results/" + dataType + dataDirName

    n = analysis(dataPath, resultPath)
    n.caSercaPeak(showFig=False)
