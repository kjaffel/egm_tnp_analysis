import math
class Cut_and_count_efficiency:
    #    altEff = [-1]*7
    iAltBkgModel = 0
    iAltSigModel = 1
    iAltMCSignal = 2
    iAltTagSelec = 3
    iPUup        = 4
    iPUdown      = 5
    iAltFitRange = 6

    def __init__(self,abin):
        self.ptBin   = abin
        self.effData = -1
        self.effMC   = -1
        self.altEff  = [-1]*7
        self.syst    = [-1]*7
    
    def __init__(self,ptBin,etaBin,effData,errEffData,errlowEffData, errhighEffData, effMC,errEffMC,errlowEffMC, errhighEffMC, effAltBkgModel,effAltSigModel,effAltMCSignal,effAltTagSel):
        self.ptBin      = ptBin
        self.etaBin     = etaBin
        self.effData    = effData
        self.effMC      = effMC
        self.errEffData = errEffData        
        self.errlowEffData = errlowEffData        
        self.errhighEffData = errhighEffData        
        self.errEffMC   = errEffMC
        self.errlowEffMC   = errlowEffMC
        self.errhighEffMC   = errhighEffMC
        self.altEff = [-1]*7
        self.syst   = [-1]*9
        self.altEff[self.iAltBkgModel] = effAltBkgModel
        self.altEff[self.iAltSigModel] = effAltSigModel
        self.altEff[self.iAltMCSignal] = effAltMCSignal
        self.altEff[self.iAltTagSelec] = effAltTagSel

    def __str__(self):
        return '%2.3f\t%2.3f\t%2.1f\t%2.1f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f' % (self.etaBin[0],self.etaBin[1],
                                                                                                       self.ptBin[0] ,self.ptBin[1] ,
                                                                                                       self.effData, self.errEffData, self.errlowEffData, self.errhighEffData,self.effMC, self.errEffMC, self.errlowEffMC, self.errhighEffMC,
                                                                                                       self.altEff[0],self.altEff[1], self.altEff[2], self.altEff[3] )

    @staticmethod
    def getSystematicNames():
        return [ 'statData', 'statMC', 'altBkgModel', 'altSignalModel', 'altMCEff', 'altTagSelection' ]



    def combineSyst(self,averageEffData,averageEffMC):
        systAltBkg      = self.altEff[self.iAltBkgModel] - averageEffData
        systAltSig      = self.altEff[self.iAltSigModel] - averageEffData
        systAltMC       = self.altEff[self.iAltMCSignal] - averageEffMC
#        systAltTagSelec = self.altEff[self.iAltTagSelec] - averageEffData
        systAltTagSelec = self.altEff[self.iAltTagSelec] - averageEffMC

        if self.altEff[self.iAltBkgModel] < 0:
            systAltBkg = 0

        if self.altEff[self.iAltSigModel] < 0:
            systAltSig = 0

        if self.altEff[self.iAltMCSignal] < 0:
            systAltMC = 0
        
        if self.altEff[self.iAltTagSelec] < 0:
            systAltTagSelec = 0

        self.syst[ 0                 ] = self.errEffData
        self.syst[ 1                 ] = self.errEffMC
        self.syst[self.iAltBkgModel+2] = systAltBkg
        self.syst[self.iAltSigModel+2] = systAltSig
        self.syst[self.iAltMCSignal+2] = systAltMC
        self.syst[self.iAltTagSelec+2] = systAltTagSelec
        
        self.systCombined = 0
        self.systlowCombined = 0
        self.systhighCombined = 0
        
        for isyst in range(6):
            self.systCombined += self.syst[isyst]*self.syst[isyst];
            if isyst ==0 :
               self.systlowCombined += self.errlowEffData * self.errlowEffData
               if averageEffData < 1. : self.systhighCombined += self.errhighEffData * self.errhighEffData

            elif isyst ==1 :
               self.systlowCombined += self.errlowEffMC * self.errlowEffMC
               if averageEffData < 1. : self.systhighCombined += self.errhighEffMC * self.errhighEffMC
               
            else :
               self.systlowCombined += (self.syst[isyst]/2)*(self.syst[isyst]/2)
               if averageEffData < 1. : self.systhighCombined += (self.syst[isyst]/2)*(self.syst[isyst]/2)
              

        self.systCombined = math.sqrt(self.systCombined)
        self.systlowCombined = math.sqrt(self.systlowCombined)
        self.systhighCombined = math.sqrt(self.systhighCombined)
        

    def __add__(self,eff):
        if self.effData < 0 :
            return eff.deepcopy()
        if eff.effData < 0 :
            return self.deepcopy()
        
        ptbin  = self.ptBin
        etabin = self.etaBin
        errData2 = 1.0 / (1.0/(self.errEffData*self.errEffData)+1.0/(eff.errEffData*eff.errEffData))
        wData1   = 1.0 / (self.errEffData * self.errEffData) * errData2
        wData2   = 1.0 / (eff .errEffData * eff .errEffData) * errData2
        newEffData      = wData1 * self.effData + wData2 * eff.effData;
        newErrEffData   = math.sqrt(errData2)

        errlowData2 = 1.0 / (1.0/(self.errlowEffData*self.errlowEffData)+1.0/(eff.errlowEffData*eff.errlowEffData))
        errhighData2 = 1.0 / (1.0/(self.errhighEffData*self.errhighEffData)+1.0/(eff.errhighEffData*eff.errhighEffData))
        newlowErrEffData = math.sqrt(errlowData2)
        newhighErrEffData = math.sqrt(errhighData2)
        
        #        errMC2 = 1.0 / (1.0/(self.errEffMC*self.errEffMC)+1.0/(eff.errEffMC*eff.errEffMC))
        #wMC1   = 1.0 / (self.errEffMC * self.errEffMC) * errMC2
        #wMC2   = 1.0 / (eff .errEffMC * eff .errEffMC) * errMC2
        newEffMC      = wData1 * self.effMC + wData2 * eff.effMC;
        newErrEffMC   = 0.00001#math.sqrt(errMC2)
        newlowErrEffMC   = 0.00001#math.sqrt(errMC2)
        newhighErrEffMC   = 0.00001#math.sqrt(errMC2)

        newEffAltBkgModel = wData1 * self.altEff[self.iAltBkgModel] + wData2 * eff.altEff[self.iAltBkgModel]
        newEffAltSigModel = wData1 * self.altEff[self.iAltSigModel] + wData2 * eff.altEff[self.iAltSigModel]
        newEffAltMCSignal = wData1 * self.altEff[self.iAltMCSignal] + wData2 * eff.altEff[self.iAltMCSignal]
        newEffAltTagSelec = wData1 * self.altEff[self.iAltTagSelec] + wData2 * eff.altEff[self.iAltTagSelec]

        effout = Cut_and_count_efficiency(ptbin,etabin,newEffData,newErrEffData,newlowErrEffData, newhighErrEffData,newEffMC,newErrEffMC,newlowErrEffMC, newhighErrEffMC,newEffAltBkgModel,newEffAltSigModel,newEffAltMCSignal,newEffAltTagSelec)
        return effout
    


import ROOT as rt
import numpy as np

def makeTGraphFromList( listOfEfficiencies , keyMin, keyMax ):
    grOut = rt.TGraphErrors(len(listOfEfficiencies))
    
    ip = 0
    for point in listOfEfficiencies:
        grOut.SetPoint(     ip, (point[keyMin]+point[keyMax])/2. , point['val'] )
        grOut.SetPointError(ip, (point[keyMax]-point[keyMin])/2. , point['err'] )
        ip = ip + 1

    #    print "###########################"
    #    print listOfEff
    #    grOut.Print()
    return grOut

def makeTGraphAsymErrorFromList( listOfEfficiencies , keyMin, keyMax ):
    grOut = rt.TGraphAsymmErrors(len(listOfEfficiencies))

    ip = 0
    for point in listOfEfficiencies:
        grOut.SetPoint(     ip, (point[keyMin]+point[keyMax])/2. , point['val'] )
        exh = point[keyMax] - (point[keyMin]+point[keyMax])/2
        exl = (point[keyMin]+point[keyMax])/2 - point[keyMin]
        eyh = point['errhigh']
        eyl = point['errlow']
        grOut.SetPointError(ip, exl, exh, eyl, eyh )
        ip = ip + 1

    #    print "###########################"
    #    print listOfEff
    #    grOut.Print()
    return grOut


class Cut_and_count_efficiencyList: 
    effList = {}

    def __init__(self):
        self.effList = {}

    
    def __str__(self):
        outStr = ''
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                outStr += str(self.effList[ptBin][etaBin])
                outStr += '\n'
        return outStr

    
    def addEfficiency( self, eff ):
        if not self.effList.has_key(eff.ptBin):
            self.effList[eff.ptBin] = {}
        self.effList[eff.ptBin][eff.etaBin] = eff

    def combineSyst(self):
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                if etaBin[0] >= 0 and etaBin[1] >= 0:
                    etaBinPlus  = etaBin
                    etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                    effPlus  = self.effList[ptBin][etaBinPlus]
                    effMinus = None
                    if self.effList[ptBin].has_key(etaBinMinus):
                        effMinus =  self.effList[ptBin][etaBinMinus] 

                    if effMinus is None:
                        #print " ---- Cut_and_count_efficiencyList: I did not find -eta bin, maybe absolute bin definition is used?"
                        averageData = (effPlus.effData)
                        averageMC   = (effPlus.effMC)
                        self.effList[ptBin][etaBinPlus ].combineSyst(averageData,averageMC)
                        
                    else:                        
                        averageData = (effPlus.effData + effMinus.effData)/2.
                        averageMC   = (effPlus.effMC   + effMinus.effMC  )/2.
                        self.effList[ptBin][etaBinMinus].combineSyst(averageData,averageMC)
                        self.effList[ptBin][etaBinPlus ].combineSyst(averageData,averageMC)

                # for one eta bin case ex) -2.5 < eta < 2.5
                if etaBin[0] < 0 and etaBin[1] > 0:

                    etaBinPlus  = etaBin

                    effPlus  = self.effList[ptBin][etaBinPlus]
                    effMinus = None

                    averageData = (effPlus.effData)
                    averageMC   = (effPlus.effMC )
                    self.effList[ptBin][etaBinPlus ].combineSyst(averageData,averageMC)
#                        self.effList[ptBin][etaBinMinus].combineSyst(effMinus.effData,effMinus.effMC)
#                        self.effList[ptBin][etaBinPlus ].combineSyst(effPlus.effData,effPlus.effMC)
                        #print 'syst 1 [-] (etaBin: %1.3f,%1.3f) ; (ptBin: %3.0f,%3.0f): %f '% (etaBin[0],etaBin[1],ptBin[0],ptBin[1],self.effList[ptBin][etaBinMinus].syst[1])
                        #print 'syst 1 [+] (etaBin: %1.3f,%1.3f) ; (ptBin: %3.0f,%3.0f): %f '% (etaBin[0],etaBin[1],ptBin[0],ptBin[1],self.effList[ptBin][etaBinPlus] .syst[1])
                        

                        
    def symmetrizeSystVsEta(self):
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                if etaBin[0] >= 0 and etaBin[1] > 0:
                    etaBinPlus  = etaBin
                    etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                    effPlus  = self.effList[ptBin][etaBinPlus]
                    effMinus = None
                    if self.effList[ptBin].has_key(etaBinMinus):
                        effMinus =  self.effList[ptBin][etaBinMinus] 

                    if effMinus is None:
                        self.effList[ptBin][etaBinMinus] = effPlus
                        #print " ---- Cut_and_count_efficiencyList: I did not find -eta bin!!!"
                    else:
                        #### fix statistical errors if needed
                        if    effPlus.errEffData <= 0.00001 and effMinus.errEffData > 0.00001: 
                            self.effList[ptBin][etaBinPlus ].errEffData = effMinus.errEffData
                        elif effMinus.errEffData <= 0.00001 and effPlus .errEffData > 0.00001: 
                            self.effList[ptBin][etaBinMinus].errEffData = effPlus.errEffData
                        else:
                            self.effList[ptBin][etaBinPlus ].errEffData = (effMinus.errEffData+effPlus.errEffData)/2.
                            self.effList[ptBin][etaBinMinus].errEffData = (effMinus.errEffData+effPlus.errEffData)/2.

                        if   effPlus.errEffMC <= 0.00001 and effMinus.errEffMC > 0.00001: 
                            self.effList[ptBin][etaBinPlus ].errEffMC = effMinus.errEffMC
                        elif effMinus.errEffMC <= 0.00001 and effPlus.errEffMC > 0.00001: 
                            self.effList[ptBin][etaBinMinus].errEffMC = effPlus.errEffMC
                        else:
                            self.effList[ptBin][etaBinPlus ].errEffMC = (effMinus.errEffMC+effPlus.errEffMC)/2.
                            self.effList[ptBin][etaBinMinus].errEffMC = (effMinus.errEffMC+effPlus.errEffMC)/2.
                            
                        for isyst in range(4):
                            if abs(effPlus.altEff[isyst] - effMinus.altEff[isyst]) < 0.10:
                                averageSyst = (effPlus.altEff[isyst] +  effMinus.altEff[isyst]) / 2
                                self.effList[ptBin][etaBinPlus ].altEff[isyst] = averageSyst
                                self.effList[ptBin][etaBinMinus].altEff[isyst] = averageSyst
                            else:
                                averageSyst = (effPlus.altEff[isyst] +  effMinus.altEff[isyst]) / 2
                                print "issue, I am averaging but the efficiencies are quite different in 2 etaBins"
                                print " --- syst: ", isyst
                                print str(self.effList[ptBin][etaBinPlus ])
                                print str(self.effList[ptBin][etaBinMinus])
                                print "   eff[+] = ",  self.effList[ptBin][etaBinPlus ].altEff[isyst]
                                print "   eff[-] = ",  self.effList[ptBin][etaBinMinus].altEff[isyst]                                
                                self.effList[ptBin][etaBinPlus ].altEff[isyst] = averageSyst
                                self.effList[ptBin][etaBinMinus].altEff[isyst] = averageSyst

    def ptEtaScaleFactor_2DHisto(self, onlyError, relError = False):
#        self.symmetrizeSystVsEta()
        self.combineSyst()

        ### first define bining
        xbins = []
        ybins = []
        for ptBin in self.effList.keys():
            if not ptBin[0] in ybins:
                ybins.append(ptBin[0])                
            if not ptBin[1] in ybins:
                ybins.append(ptBin[1])

            for etaBin in self.effList[ptBin].keys():
                if not etaBin[0] in xbins:
                    xbins.append(etaBin[0])                
                if not etaBin[1] in xbins:
                    xbins.append(etaBin[1])

        xbins.sort()
        ybins.sort()
        ## transform to numpy array for ROOT
        xbinsTab = np.array(xbins)
        ybinsTab = np.array(ybins)

        htitle = 'e/#gamma scale factors'
        hname  = 'h2_scaleFactorsEGamma'+str(onlyError) 
        if onlyError >= 0:
            htitle = 'e/#gamma uncertainties'
            hname  = 'h2_uncertaintiesEGamma'+str(onlyError)             

        h2 = rt.TH2F(hname,htitle,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)

        ## init histogram efficiencies and errors to 100%
        for ix in range(1,h2.GetXaxis().GetNbins()+1):
            for iy in range(1,h2.GetYaxis().GetNbins()+1):
                h2.SetBinContent(ix,iy, 1)
                h2.SetBinError  (ix,iy, 1)
        
        for ix in range(1,h2.GetXaxis().GetNbins()+1):
            for iy in range(1,h2.GetYaxis().GetNbins()+1):

                for ptBin in self.effList.keys():
                    if h2.GetYaxis().GetBinLowEdge(iy) < ptBin[0] or h2.GetYaxis().GetBinUpEdge(iy) > ptBin[1]:
                        continue
                    for etaBin in self.effList[ptBin].keys():
                        if h2.GetXaxis().GetBinLowEdge(ix) < etaBin[0] or h2.GetXaxis().GetBinUpEdge(ix) > etaBin[1]:
                            continue

                        ## average MC Cut_and_count_efficiency
                        etaBinPlus  = etaBin
                        etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                        effPlus  = self.effList[ptBin][etaBinPlus]
                        effMinus = None
                        if self.effList[ptBin].has_key(etaBinMinus):
                            effMinus =  self.effList[ptBin][etaBinMinus] 

                        averageMC = None
                        if effMinus is None:
                            averageMC = effPlus.effMC
                            #print " ---- Cut_and_count_efficiencyList: I did not find -eta bin!!!"
                        else:                        
                            averageMC   = (effPlus.effMC   + effMinus.effMC  )/2.
                        ### so this is h2D bin is inside the bining used by e/gamma POG
                        h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].effData      / self.effList[ptBin][etaBin].effMC)
                        h2.SetBinError  (ix,iy, self.effList[ptBin][etaBin].systCombined / averageMC )
                        if onlyError   == 0 :
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].systCombined      / averageMC  )
                        if   onlyError == -3 :
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].effData      )
                            h2.SetBinError  (ix,iy, self.effList[ptBin][etaBin].systCombined * self.effList[ptBin][etaBin].effMC / averageMC )
                        elif onlyError == -2 :
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].effMC)
                            h2.SetBinError  (ix,iy, 0 )
                        elif onlyError == -1 :
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].effData      / self.effList[ptBin][etaBin].effMC)
                            h2.SetBinError  (ix,iy, self.effList[ptBin][etaBin].systCombined / averageMC )

                        if onlyError   == 0 :
                                h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].systCombined      / averageMC  )
                        elif onlyError >= 1 and onlyError <= 6:
                            denominator = averageMC
                            if relError:
                                denominator = self.effList[ptBin][etaBin].systCombined
                            h2.SetBinContent(ix,iy, abs(self.effList[ptBin][etaBin].syst[onlyError-1]) / denominator )

        h2.GetXaxis().SetTitle("SuperCluster #eta")
        h2.GetYaxis().SetTitle("p_{T} [GeV]")
        return h2
        
                                
    def pt_1DGraph_list(self, doScaleFactor):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}
        
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                   if etaBin[0] >= 0 and etaBin[1] > 0:
                       etaBinPlus  = etaBin
                       etaBinMinus = (-etaBin[1],-etaBin[0])
                       
                       effPlus  = self.effList[ptBin][etaBinPlus]
                       effMinus = None
                       if self.effList[ptBin].has_key(etaBinMinus):
                           effMinus =  self.effList[ptBin][etaBinMinus] 

                       effAverage = effPlus
                       if not effMinus is None:
                           effAverage = effPlus + effMinus
                       else :
                           effAverage = effPlus
                           
                       if not listOfGraphs.has_key(etaBin):                        
                           ### init average Cut_and_count_efficiency 
                           listOfGraphs[etaBin] = []

                       effAverage.combineSyst(effAverage.effData,effAverage.effMC)
                       aValue  = effAverage.effData
                       anError = effAverage.systCombined 
                       if doScaleFactor :
                           aValue  = effAverage.effData      / effAverage.effMC
                           anError = effAverage.systCombined / effAverage.effMC  
                       listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                  'val': aValue  , 'err': anError } ) 
                   else:
                       etaBinPlus  = etaBin
                 
                       effPlus  = self.effList[ptBin][etaBinPlus]

                       effAverage = effPlus
                 
                       if not listOfGraphs.has_key(etaBin):
                           ### init average Cut_and_count_efficiency 
                           listOfGraphs[etaBin] = []

                       effAverage.combineSyst(effAverage.effData,effAverage.effMC)
                       aValue  = effAverage.effData
                       anError = effAverage.systCombined

                       #aValue  = effAverage.errlowEffData  # FIXME it seems wrong to assign errlowEffData to aValue, but now this function pt_1DGraph_list only used for SF i.e., with doScaleFactor == True 
                       #anError = effAverage.errhighEffData # so make no problem but need to fix to avoid confusion

                       if doScaleFactor :
                           aValue  = effAverage.effData      / effAverage.effMC
                           anError = effAverage.errEffData / effAverage.effMC
                       listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                  'val': aValue  , 'err': anError } )
                                                  
        return listOfGraphs

    def pt_1DGraphAsymError_list(self, doScaleFactor):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}


        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                   if etaBin[0] >= 0 and etaBin[1] > 0:
                       etaBinPlus  = etaBin
                       etaBinMinus = (-etaBin[1],-etaBin[0])

                       if abs(etaBin[0]) == 1.444 and abs(etaBin[1]) == 1.566: continue


                       effPlus  = self.effList[ptBin][etaBinPlus]
                       effMinus = None
                       if self.effList[ptBin].has_key(etaBinMinus):
                           effMinus =  self.effList[ptBin][etaBinMinus]

                       effAverage = effPlus
                       if not effMinus is None:
                           effAverage = effPlus + effMinus
                       else :
                           effAverage = effPlus

                       if not listOfGraphs.has_key(etaBin):
                           ### init average Cut_and_count_efficiency 
                           listOfGraphs[etaBin] = []

                       effAverage.combineSyst(effAverage.effData,effAverage.effMC)
                       aValue  = effAverage.effData
                       anErrorLow = effAverage.systlowCombined
                       anErrorHigh = effAverage.systhighCombined

                       listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                     'val': aValue  , 'errhigh': anErrorHigh, 'errlow': anErrorLow } )
                       if doScaleFactor :
                           aValue  = effAverage.effData      / effAverage.effMC
                           anError = effAverage.systCombined / effAverage.effMC

                           listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                      'val': aValue  , 'err': anError} )
                   else : 
                       etaBinPlus  = etaBin

                       effPlus  = self.effList[ptBin][etaBinPlus]

                       effAverage = effPlus

                       if not listOfGraphs.has_key(etaBin):
                           ### init average Cut_and_count_efficiency 
                           listOfGraphs[etaBin] = []

                       effAverage.combineSyst(effAverage.effData,effAverage.effMC)
                       aValue  = effAverage.effData
                       anErrorLow = effAverage.errlowEffData
                       anErrorHigh = effAverage.errhighEffData

                       listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                     'val': aValue  , 'errhigh': anErrorHigh, 'errlow': anErrorLow } )
                       if doScaleFactor :
                           aValue  = effAverage.effData      / effAverage.effMC
                           anError = effAverage.errEffData / effAverage.effMC

                           listOfGraphs[etaBin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                      'val': aValue  , 'err': anError} )


        return listOfGraphs

    def pt_1DGraph_list_customEtaBining(self, etaBining):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}

        for abin in etaBining:
            listOfGraphs[abin] = []
            for ptBin in self.effList.keys():
                for etaBin in self.effList[ptBin].keys():
                    if etaBin[0] >= 0 and etaBin[1] > 0:
                        etaBinPlus  = etaBin
                        etaBinMinus = (-etaBin[1],-etaBin[0])

                        if abin[0] < etaBin[0] or abin[1] > etaBin[1]:
                            continue
                        #                        if abin[0] >= etaBin[0] and abin[1] <= etaBin[1]:
                        #                            continue
                        effPlus  = self.effList[ptBin][etaBinPlus]
                        effMinus = None
                        if self.effList[ptBin].has_key(etaBinMinus):
                            effMinus =  self.effList[ptBin][etaBinMinus] 

                        effAverage = effPlus
                        if not effMinus is None:
                            effAverage = effPlus + effMinus

                        effAverage.combineSyst(effAverage.effData,effAverage.effMC)
                        aValue  = effAverage.effData
                        anError = effAverage.systCombined 
                        if doScaleFactor :
                            aValue  = effAverage.effData      / effAverage.effMC
                            anError = effAverage.systCombined / effAverage.effMC  
                        listOfGraphs[abin].append( {'min': ptBin[0], 'max': ptBin[1],
                                                    'val': aValue  , 'err': anError } ) 
                                                  
        return listOfGraphs


    
    def eta_1DGraph_list(self, typeGR = 0 ):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}
        
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                if not listOfGraphs.has_key(ptBin):                        
                    ### init average Cut_and_count_efficiency 
                    listOfGraphs[ptBin] = []
                effAverage = self.effList[ptBin][etaBin]
                aValue  = effAverage.effData
                anError = effAverage.systCombined 
                if typeGR == 1:
                    aValue  = effAverage.effData      / effAverage.effMC
                    anError = effAverage.systCombined / effAverage.effMC  
                if typeGR == -1:
                    aValue  = effAverage.effMC
                    anError = 0#effAverage.errEffMC
                    
                listOfGraphs[ptBin].append( {'min': etaBin[0], 'max': etaBin[1],
                                             'val': aValue  , 'err': anError } )

        return listOfGraphs

    def eta_1DGraphAsymError_list(self, typeGR = 0):
#        self.symmetrizeSystVsEta()
#        if doAverage:
        self.combineSyst()
        listOfGraphs = {}

        for ptBin in self.effList.keys():
            if ptBin[0] < 25: continue
            for etaBin in self.effList[ptBin].keys():
                if not listOfGraphs.has_key(ptBin):
                    ### init average Cut_and_count_efficiency 
                    listOfGraphs[ptBin] = []
                effAverage = self.effList[ptBin][etaBin]
                aValue  = effAverage.effData
                #anError = effAverage.systCombined
                anErrorLow = effAverage.systlowCombined
                anErrorHigh = effAverage.systhighCombined

                if typeGR == 0:
                   listOfGraphs[ptBin].append( {'min': etaBin[0], 'max': etaBin[1],
                                              'val': aValue  , 'errhigh': anErrorHigh, 'errlow': anErrorLow } )
                if typeGR == 1:
                    aValue  = effAverage.effData      / effAverage.effMC
                    anError = effAverage.systCombined / effAverage.effMC
                    listOfGraphs[ptBin].append( {'min': etaBin[0], 'max': etaBin[1],
                                                  'val': aValue  , 'err': anError} )
                if typeGR == -1:
                    aValue  = effAverage.effMC
                    anError = 0#effAverage.errEffMC
                    listOfGraphs[ptBin].append( {'min': etaBin[0], 'max': etaBin[1],
                                               'val': aValue  , 'err': anError} )

        return listOfGraphs 
