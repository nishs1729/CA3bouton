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
        self.allDirs = self.getDirs(self.dataPath)
        self.ndirs = len(self.allDirs)

    #   Get list of directories in the path starting with 's_'
    def getDirs(self, path, sstr='s_'):
        dirs = [d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d]
        dirs.sort()
        return(dirs)

    #   Get data from dataFile in array
    def getData(self, inFile="/dat/ca.dat"):
        self.data = []
        for i,d in enumerate(self.allDirs):#[:100]):
            self.data.append(genfromtxt(self.dataPath+'/'+d+inFile, unpack=True))

    #   Average Over all Seeds
    def avg_dat(self, dirs, inFile="/dat/ca.dat"):
        self.seeds = len(dirs)
        data = [self.data[i] for i in dirs]
        avg = mean(data, axis=0)
        return avg

    def caStat(self, vdcc, resample=1000, outFile='/caStat.dat', showFig=True):
        #self.ndirs=100
        info = []
        for r in range(resample):
            if (r+1)%100==0: print 'resampling:', r+1
            dirs = [randint(0,self.ndirs-1) for p in range(self.ndirs)]

            # get avg of trials
            avg = self.avg_dat(dirs)
            #avg = genfromtxt(self.resultPath + '/ca.dat', usecols=(0,1,2), unpack=True)

            # get instantaneous ca conc.
            caConc = self.conc_calc(avg[:2])
            #caConc = genfromtxt(self.resultPath + '/CaConc', usecols=(0,1), unpack=True)

            temp = []

            # get global Ca peaks
            pk = detect_peaks(avg[2]/602.3, mph=1, mpd=300, threshold=0, show=showFig)
            pkValue = [avg[2][i]/602.3 for i in pk]
            temp += pkValue

            # get local Ca peaks

            pk = detect_peaks(caConc[1], mph=3, mpd=300, threshold=0, show=showFig)
            pkValue = [caConc[1][i] for i in pk]
            temp += pkValue


            # get local cumulative ca conc

            cumVal = []
            dt = caConc[0][1]-caConc[0][0]
            for p in [p-30 for p in pk]:
                dataChunk = caConc[1][p:p+400]
                cumVal.append(simps(dataChunk, dx=dt))
                #plot(caConc[0][p:p+400], dataChunk)
            #show()
            temp += cumVal


            info.append(temp)

        #print info

        m = mean(info, axis=0)
        s = std(info, axis=0)
        stat = array(zip(m,s)).flatten()
        stat = append(stat, vdcc)
        print stat

        r = open(self.resultPath + '/caPeakStat', 'w')
        savetxt(r, [stat], fmt=['%0.6f']*12+['%d'], delimiter="\t")

if __name__ == '__main__':
    if len(sys.argv)<2:
        dataDirName = "RS20p50hz"
    else:
        dataDirName = sys.argv[1]

    vdcc = int(dataDirName.split('V')[1])
    dataType = "ppf/"
    path = "/media/nishant/4tb/output/" + dataType + dataDirName

    dataPath = path
    resultPath = "/home/nishant/Lab/results/" + dataType + dataDirName

    n = analysis(dataPath, resultPath)
    n.getData()
    n.caStat(vdcc, resample=1000, showFig=False)
