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
        self.ndirs = len(self.allDirs[:])

    #   Get list of directories in the path starting with 's_'
    def getDirs(self, path, sstr='s_'):
        dirs = [d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d]
        dirs.sort()
        return(dirs)

    #   Get data from dataFile in array
    def getData(self, inFile="/dat/ca.dat"):
        self.data = []
        for i,d in enumerate(self.allDirs[:]):
            self.data.append(genfromtxt(self.dataPath+'/'+d+inFile, unpack=True).tolist())

    #   Average Over all Seeds
    def avg_dat(self, dirs, inFile="/dat/ca.dat"):
        self.seeds = len(dirs)
        data = [self.data[i] for i in dirs]
        avg = mean(data, axis=0)
        return avg


    #   Ca Concentration Calculation
    def conc_calc(self, data, step=5):
        c_tc = multiply(data[0],data[1])
        dt=step*(data[0][1]-data[0][0])
        c_out = []
        for i in range(0,len(data[0])-step-1,step):
            c_out.append([data[0][i], (c_tc[i+step]-c_tc[i])/dt])

        return array(c_out).T

    def caStat(self, vdcc, resample=1000, outFile='/caStat.dat', showFig=True):
        #self.ndirs=100
        self.getData()
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

    def caVDCC(self, vdcc, skip=100, resample=1000, inFile='/dat/vdcc_pq_ca_flux.dat', outFile='/caStatVDCC.dat', showFig=True):
        data = []
        for i, dir in enumerate(self.allDirs):
            #print i, dir
            #skip=600
            vdccData = genfromtxt(self.dataPath+'/'+dir+inFile, dtype="int", usecols=(1), unpack=True)

            pkValue = [vdccData[300], vdccData[2300]]
            #print pkValue
            data.append(pkValue)

            '''
            pk = detect_peaks(vdccData, mph=3000, mpd=1900, show=showFig)
            pkValue = [vdccData[i] for i in pk]
            if len(pkValue)>2: print i, pkValue
            '''
            '''
            print vdccData[::skip]
            tp = vdccData[0]
            rep = 'a'
            l=0
            for j,v in enumerate(vdccData[skip::skip]):
                if v == tp and v != rep and unique(vdccData[(j+1)*skip:(j+2)*skip]).size == 1:
                    print v#, vdccData[(j+1)*skip], vdccData[(j+1)*skip:(j+1)*skip+10]

                    rep = v
                    l += 1
                else:
                    tp = v
            print l

            #temp = VDCCinflux(dir)
            #data[i] = temp
            '''
        m = mean(data, axis=0)
        s = std(data, axis=0)
        #print m, s, vdcc

        stat = array(zip(m,s)).flatten()
        stat = append(stat, vdcc)

        print stat
        r = open(self.resultPath + outFile, 'w')
        savetxt(r, [stat], fmt=['%0.6f']*4+['%d'], delimiter="\t")

    def caAtRelease(self, vdcc, outFile='/caAtRelease.dat'):
        print self.ndirs
        data = []
        a=0
        for n,dir in enumerate(self.allDirs):
            if n%100==0: print 'seed:', n
            ca = genfromtxt(self.dataPath+'/'+dir+'/dat/ca.dat', usecols=(0,2), unpack=True).tolist()
            ca[0] = [rint(i*100000) for i in ca[0]]

            rel = genfromtxt(self.dataPath+'/'+dir+'/dat/rel.dat', usecols=(0), unpack=True).tolist()
            if not isinstance(rel, (list)):
                rel = [rel]
            #print rel

            if len(rel)>0:
                rel = [int(rint(i*100000)) for i in rel]
                for t in rel:
                    try:
                        ind = map(int, ca[0]).index(t)
                        data.append(ca[1][ind])
                    except:
                        a += 1
        print 'Errors:', a#, t, dir
        #print data
        r = open(self.resultPath + outFile, 'w')
        savetxt(r, [[vdcc] + data], fmt='%0.2f', delimiter="\n")


    def caConcStd(self, resample=1000, outFile='/caConcStd.dat'):
        self.getData()
        t1 = time()
        caConcAll = []
        for r in range(resample):
            if (r+1)%100==0: print 'resampling:', r+1
            dirs = [randint(0,self.ndirs-1) for p in range(self.ndirs)]

            # get avg of trials
            avg = self.avg_dat(dirs)

            # get instantaneous ca conc.
            caConc = self.conc_calc(avg[:2])
            #plot(caConc[0], caConc[1]); show()
            caConcAll.append(caConc[1])

        t2 = time()
        #print t2-t1
        #print caConcAll

        caConcStd = std(caConcAll, axis=0)
        caConcMean = mean(caConcAll, axis=0)
        #plot(caConc[0], caConcStd); show()
        #print [caConc[0], caConcStd]

        r = open(self.resultPath + outFile, 'w')
        savetxt(r, array([caConc[0], caConcMean, caConcStd]).T, fmt='%0.6f', delimiter="\t")

    def azStat(self, outFile='/azStat.dat'):
        self.getData(inFile="/dat/az.dat")

        #print array(self.data)[0]
        data = [d[2]+d[7] + (d[3]+d[8]+d[13])*2 + (d[4]+d[9]+d[14])*3 + (d[5]+d[10]+d[15])*4 + (d[6]+d[11]+d[16])*5 + (d[12]+d[17])*6 + d[18]*7 for d in array(self.data)]

        #data = self.data[2] + self.data[7] +
        #      (self.data[3] + self.data[8] + self.data[13])*2 +
        #      (self.data[4] + self.data[9] + self.data[14])*3 +
        #      (self.data[5] + self.data[10] + self.data[15])*4 +
        #      (self.data[6] + self.data[11] + self.data[16])*5 +
        #      (self.data[12] + self.data[17])*6 +
        #      (self.data[18])*7

        avg = mean(data, axis=0)
        err = std(data, axis=0)

        #print avg, err

        r = open(self.resultPath + outFile, 'w')
        savetxt(r, array([self.data[0][0], avg, err]).T, fmt='%0.6f', delimiter="\t")


if __name__ == '__main__':
    if len(sys.argv)<2:
        dataDirName = "RSI20V100"
    else:
        dataDirName = sys.argv[1]

    vdcc = int(dataDirName.split('V')[1])
    dataType = "ppf/"
    path = "/media/nishant/4tb/output/" + dataType + dataDirName

    dataPath = path
    resultPath = "/home/nishant/Lab/results/" + dataType + dataDirName

    n = analysis(dataPath, resultPath)
    #n.caStat(vdcc, resample=1000, showFig=False)
    #n.caVDCC(vdcc, resample=2, showFig=False)
    #n.caAtRelease(vdcc)
    #n.caConcStd(resample=1000)
    n.azStat()
