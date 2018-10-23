#!/usr/bin/python

#PBS -p 1
#PBS -j oe
#PBS -J 0-1

import os, sys
from time import time
sys.path.insert(0, '/storage/nishant/results/script/')
from modFuncNew import *

i = int(os.getenv('PBS_ARRAY_INDEX')) - 1

d = os.environ['d']
dataDirName = d # d comes from commant line input

dataType = "freq/"
path = "/storage/nishant/" + dataType + dataDirName
#dataDirList = os.listdir(path)
#print dataDirList

dataPath = path
resultPath = "/storage/nishant/results/" + dataType + dataDirName

if not os.path.exists(resultPath):
    os.makedirs(resultPath)

print "\n\ndataPath : ", dataPath
print "resultPath : ", resultPath

ns = analysis(dataPath, resultPath)

def azAvg():
    ns.avg_dat(inFile="/dat/az.dat", outFile="/az.dat")

def caAvg():
    #ns.avg_dat(inFile="/dat/ca.dat", outFile="/ca.dat")
    #ns.conc_calc(inFile="/ca.dat", outFile="/CaConc")
    ns.caStat(showFig=False)

def rrpAvg():
    ns.avg_dat(inFile="/dat/rrp.dat", outFile="/rrp.dat")

def vdccFlux():
    ns.avg_dat(inFile="/dat/vdcc_pq_ca_flux.dat", outFile="/vdccCaFlux.dat")
    ns.fluxCurrent(inFile="/vdccCaFlux.dat", outFile="/vdccCaFluxRate.dat")

def pmcaAvg():
    ns.avg_dat(inFile="/dat/pmca&leak_ca_flux.dat", outFile="/pmca_leak.dat")

def calbAvg():
    ns.avg_dat(inFile="/dat/calbindin_mol.dat", outFile="/calB.dat")

def sercaFluxAvg():
    ns.avg_dat(inFile="/dat/serca_ca_flux.dat", outFile="/sercaCaFlux.dat")

def sercaMolAvg():
    ns.avg_dat(inFile="/dat/serca_mol.dat", outFile="/sercaMol.dat")

def ryrFluxAvg():
    ns.avg_dat(inFile="/dat/ryr_ca_flux.dat", outFile="/ryrCaFlux.dat")
    ns.fluxCurrent(inFile="/ryrCaFlux.dat", outFile="/ryrCaFluxRate.dat", line=2)

def ryrMolAvg():
    ns.avg_dat(inFile="/dat/ryr_mol.dat", outFile="/ryrMol.dat")

def ip3Avg():
    ns.avg_dat(inFile="/dat/ip3.dat", outFile="/ip3.dat")

def ip3CreateAvg():
    ns.avg_dat(inFile="/dat/ip3_create.dat", outFile="/ip3Create.dat")

def ip3OpenAvg():
    ns.avg_dat(inFile="/dat/ip3r_open.dat", outFile="/ip3rOpen.dat")

def ip3FluxAvg():
    ns.avg_dat(inFile="/dat/ip3r_ca_flux.dat", outFile="/ip3rCaFlux.dat")
    ns.fluxCurrent(inFile="/ip3rCaFlux.dat", outFile="/ip3rCaFluxRate.dat")

def mglurAvg():
    ns.avg_dat(inFile="/dat/mglur.dat", outFile="/mglur.dat")

def plcAvg():
    ns.avg_dat(inFile="/dat/plc.dat", outFile="/plc.dat")

def gluAvg():
    ns.avg_dat(inFile="/dat/glu.dat", outFile="/glu.dat")

def ppf():
    isi = int(dataDirName.split("I")[1].split("V")[0])
    vdcc = int(dataDirName.split("V")[1].split('_')[0])
    print 'isi: ', isi, 'vdcc: ', vdcc
    ns.relppf(isi, vdcc)

def ptp():
    n = 20
    isi = 1000/int(dataDirName.split('p')[1].split('hz')[0])
    ns.relptp(n, isi)

def caC():
    ns.avg_dat(inFile="/dat/ca.c.dat", outFile="/ca.c.dat")
def cbp():
    ns.avg_dat(inFile="/dat/cbp.dat", outFile="/cbp.dat")
def caP():
    ns.avg_dat(inFile="/dat/ca.pb.dat", outFile="/ca.pb.dat")
    ns.avg_dat(inFile="/dat/ca.pf.dat", outFile="/ca.pf.dat")

# RS sims
fl = [ppf, azAvg, caAvg, rrpAvg, vdccFlux, pmcaAvg, calbAvg, sercaFluxAvg, sercaMolAvg, ryrFluxAvg, ryrMolAvg]

# IP3S sims
#fl = [ppf, azAvg, caAvg, rrpAvg, vdccFlux, pmcaAvg, calbAvg, sercaFluxAvg, sercaMolAvg, ip3Avg, ip3CreateAvg, ip3OpenAvg, ip3FluxAvg, gluAvg]

# IRS sims
#fl = [ppf, azAvg, caAvg, rrpAvg, vdccFlux, pmcaAvg, calbAvg, sercaFluxAvg, sercaMolAvg, ryrFluxAvg, ryrMolAvg, ip3Avg, ip3CreateAvg, ip3OpenAvg, ip3FluxAvg, gluAvg]

# custom
fl = [caAvg]#, calbAvg, sercaFluxAvg, sercaMolAvg, azAvg]

fl[i]()
