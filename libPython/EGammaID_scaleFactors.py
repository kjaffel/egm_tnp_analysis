#!/usr/bin/env python
import sys,os
import CMS_lumi, tdrstyle
from math import sqrt
import ROOT as rt

import efficiencyUtils as effUtil
from efficiencyUtils import efficiency
from efficiencyUtils import efficiencyList

from Cut_and_Count_efficiencyUtils import Cut_and_count_efficiency
from Cut_and_Count_efficiencyUtils import Cut_and_count_efficiencyList
import  Cut_and_Count_efficiencyUtils as Cut_and_Count_effUtil


tdrstyle.setTDRStyle()

effiMin = 0.68
effiMax = 1.07

sfMin = 0.78
sfMax = 1.12


def isFloat( myFloat ):
    try:
        float(myFloat)
        return True
    except:
        return False


graphColors = [rt.kBlack, rt.kGray+1, rt.kRed +1, rt.kRed-2, rt.kAzure+2, rt.kAzure-1, 
               rt.kSpring-1, rt.kYellow -2 , rt.kYellow+1,
               rt.kBlack, rt.kBlack, rt.kBlack, 
               rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack ]

def findMinMax_v2( effis ):
    mini = +999
    maxi = -999

    for key in effis.keys():
        for eff in effis[key]:
            if eff['val'] - eff['errlow'] < mini:
                mini = eff['val'] - eff['errlow']
            if eff['val'] + eff['errhigh'] > maxi:
                maxi = eff['val'] + eff['errhigh']

    if mini > 0.18 and mini < 0.28:
        mini = 0.18
    if mini > 0.28 and mini < 0.38:
        mini = 0.28
    if mini > 0.38 and mini < 0.48:
        mini = 0.38
    if mini > 0.48 and mini < 0.58:
        mini = 0.48
    if mini > 0.58 and mini < 0.68:
        mini = 0.58
    if mini > 0.68 and mini < 0.78:
        mini = 0.68
    if mini > 0.78 and mini < 0.88:
        mini = 0.78
    if mini > 0.88:
        mini = 0.88
    if mini > 0.92:
        mini = 0.92

        
    if  maxi > 0.95:
        maxi = 1.17        
    elif maxi < 0.87:
        maxi = 0.87
    else:
        maxi = 1.07

    if maxi-mini > 0.5:
        maxi = maxi + 0.2
        
    return (mini,maxi)
    


def findMinMax( effis ):
    mini = +999
    maxi = -999

    for key in effis.keys():
        for eff in effis[key]:
            if eff['val'] - eff['err'] < mini:
                mini = eff['val'] - eff['err']
            if eff['val'] + eff['err'] > maxi:
                maxi = eff['val'] + eff['err']

    if mini > 0.18 and mini < 0.28:
        mini = 0.18
    if mini > 0.28 and mini < 0.38:
        mini = 0.28
    if mini > 0.38 and mini < 0.48:
        mini = 0.38
    if mini > 0.48 and mini < 0.58:
        mini = 0.48
    if mini > 0.58 and mini < 0.68:
        mini = 0.58
    if mini > 0.68 and mini < 0.78:
        mini = 0.68
    if mini > 0.78 and mini < 0.88:
        mini = 0.78
    if mini > 0.88:
        mini = 0.88
    if mini > 0.92:
        mini = 0.92

        
    if  maxi > 0.95:
        maxi = 1.17        
    elif maxi < 0.87:
        maxi = 0.87
    else:
        maxi = 1.07

    if maxi-mini > 0.5:
        maxi = maxi + 0.2
        
    return (mini,maxi)

    

def EffiGraph1D(effDataList, effMCList, sfList ,nameout, xAxis = 'pT', yAxis = 'eta'):
            
    W = 800
    H = 800
    yUp = 0.45
    canName = 'toto' + xAxis

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.10)
    c.SetLeftMargin(0.12)
    
    
    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.0075)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p2.SetTopMargin(   0.0075)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    firstGraph = True
    leg = rt.TLegend(0.5,0.80,0.95 ,0.92)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfMC      = []

    xMin = 10
    xMax = 200
    if 'pT' in xAxis or 'pt' in xAxis:
        p1.SetLogx()
        p2.SetLogx()    
        xMin = 10
        xMax = 500
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  3
        xMax = 42
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.60
        xMax = +2.60
    
    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    effminmax =  findMinMax( effDataList )
    effiMin = effminmax[0]
    effiMax = effminmax[1]
    effiMin = 0.18
    effiMax = 1.35

    sfminmax =  findMinMax( sfList )
    sfMin = sfminmax[0]
    sfMin = 0.78
    sfMax = 1.12

    for key in sorted(effDataList.keys()):
        grBinsEffData = effUtil.makeTGraphFromList(effDataList[key], 'min', 'max')
        grBinsSF      = effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')
        grBinsEffMC = None
        if not effMCList is None:
            grBinsEffMC = effUtil.makeTGraphFromList(effMCList[key], 'min', 'max')
            grBinsEffMC.SetLineStyle( rt.kDashed )
            grBinsEffMC.SetLineColor( graphColors[igr] )
            grBinsEffMC.SetMarkerSize( 0 )
            grBinsEffMC.SetLineWidth( 2 )

        grBinsSF     .SetMarkerColor( graphColors[igr] )
        grBinsSF     .SetLineColor(   graphColors[igr] )
        grBinsSF     .SetLineWidth(2)
        grBinsEffData.SetMarkerColor( graphColors[igr] )
        grBinsEffData.SetLineColor(   graphColors[igr] )
        grBinsEffData.SetLineWidth(2) 
                
        grBinsEffData.GetHistogram().SetMinimum(effiMin)
        grBinsEffData.GetHistogram().SetMaximum(effiMax)

        grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram().SetMinimum(sfMin)
        grBinsSF.GetHistogram().SetMaximum(sfMax)
        
        grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
        if 'eta' in xAxis or 'Eta' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SuperCluster #eta")
        elif 'pt' in xAxis or 'pT' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("p_{T}  [GeV]")  
        elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")  
            
        grBinsSF.GetHistogram().GetYaxis().SetTitle("Data / MC " )
        grBinsSF.GetHistogram().GetYaxis().SetTitleOffset(1)

        grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
        grBinsEffData.GetHistogram().GetYaxis().SetTitle("Data efficiency" )
        grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )

            
        ### to avoid loosing the TGraph keep it in memory by adding it to a list
        listOfTGraph1.append( grBinsEffData )
        listOfTGraph2.append( grBinsSF ) 
        listOfMC.append( grBinsEffMC   )
        if 'eta' in yAxis or 'Eta' in yAxis:
            leg.AddEntry( grBinsEffData, '%1.3f #leq | #eta | #leq  %1.3f' % (float(key[0]),float(key[1])), "PL")        
        elif 'pt' in yAxis or 'pT' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq p_{T} #leq  %3.0f GeV' % (float(key[0]),float(key[1])), "PL")        
        elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")        

        
    for igr in range(len(listOfTGraph1)+1):

        option = "P"
        if igr == 1:
            option = "AP"

        use_igr = igr
        if use_igr == len(listOfTGraph1):
            use_igr = 0
            
        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(effiMax)
        p1.cd()
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].Draw("ez")

        p2.cd()            
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)
        if 'pT' in xAxis or 'pt' in xAxis :
            listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        listOfTGraph2[use_igr].Draw(option)
        

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    leg.Draw()    
    CMS_lumi.CMS_lumi(c, 4, 10)

    c.Print(nameout)
    listName = nameout.split('/')
    for iext in ["pdf","C","png"]:
        c.SaveAs(nameout.replace('egammaEffi.txt_egammaPlots',listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3]).replace('pdf',iext))

    return listOfTGraph2



def doPlot(filein, lumi, axis = ['pT','eta'] ):
    print " Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi )
    CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi

    nameOutBase = filein
    if not os.path.exists( filein ) :
        print 'file %s does not exist' % filein
        sys.exit(1)


    fileWithEff = open(filein, 'r')
    effGraph = Cut_and_count_efficiencyList()

    for line in fileWithEff :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]) )
            ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )

            myeff = Cut_and_count_efficiency(ptKey,etaKey,
                               float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),float(numbers[8]),float(numbers[9]),float(numbers[10] ),float(numbers[11] ),
                               float(numbers[12]),float(numbers[13]),float(numbers[14]),float(numbers[15]) )
#                           float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )

            effGraph.addEfficiency(myeff)

    fileWithEff.close()

    print " ------------------------------- "

    pdfout = nameOutBase + '_egammaPlots.pdf'
    cDummy = rt.TCanvas()
    cDummy.Print( pdfout + "[" )

    if axis[0] == 'vtx' or axis[0] == 'pT':

       EffiGraphAsymError1D( effGraph.pt_1DGraphAsymError_list( False , False) , #eff Data
                    None,
                    effGraph.pt_1DGraph_list( True , False) , #SF
                    pdfout,
                    xAxis = axis[0], yAxis = axis[1] )


    if axis[0] == 'eta':
       EffiGraphAsymError1D( effGraph.eta_1DGraphAsymError_list( typeGR =  0 , doAverage = False) , # eff Data
                              effGraph.eta_1DGraphAsymError_list( typeGR = -1 , doAverage = False) , # eff MC
                              effGraph.eta_1DGraphAsymError_list( typeGR = +1 , doAverage = False) , # SF
                              pdfout,
                              xAxis = axis[0], yAxis = axis[1] )



    cDummy.Print( pdfout + "]" )



def EffiGraph1D_multiData(effDataLists, effMCList, sfLists ,nameout, fileNameList, denomNameList, xAxis = 'pT', yAxis = 'eta', EB_or_EE = 'EB'):

    W = 800
    H = 800
    yUp = 0.3
    canName = 'toto' + xAxis + EB_or_EE

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.10)
    c.SetLeftMargin(0.12)


    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp + 0.001, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.02)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p1.SetGridy()
    p2.SetTopMargin(   0.0075)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    firstGraph = True
    #leg = rt.TLegend(0.35, 0.8, 0.65 ,0.93) # for eta, nvtx
    leg = rt.TLegend(0.35, 0.8, 0.65 ,0.93) # for et plot
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfTGraph2_ = []
    listOfMC      = []

    xMin = 10
    xMax = 200
    if 'pT' in xAxis or 'pt' in xAxis:
        p1.SetLogx()
        p2.SetLogx()
        xMin = 10
        xMax = 500
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  0
        xMax = 70
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.50
        xMax = +2.50
    elif 'phi' in xAxis or 'Phi' in xAxis:
        xMin = -3.15
        xMax = +3.15
    elif 'z' in xAxis or 'Z' in xAxis:
        xMin = 0
        xMax = 20

    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    # loop over effGraphList and save them into listOfTGraph
    idx_sfList = 0
    for list_ in effDataLists :
        if 'eta' not in xAxis :
           if 'EB' == EB_or_EE :
              effDataList = list_.pt_1DGraphAsymError_list( False)
              effMCList= None
              sfList = list_.pt_1DGraph_list( True)
              name = fileNameList[idx_sfList]
           elif 'EE' == EB_or_EE :
              effDataList = list_.pt_1DGraphAsymError_list( False)
              effMCList= None
              sfList = list_.pt_1DGraph_list( True )
              name = fileNameList[idx_sfList]
        elif 'eta' in xAxis :
              effDataList = list_.eta_1DGraphAsymError_list( typeGR =  0 )
              #effMCList = list_.eta_1DGraphAsymError_list( typeGR = -1 , doAverage = False)
              effMCList = None
              sfList = sfLists[idx_sfList].eta_1DGraphAsymError_list( typeGR = +1 )
              name = fileNameList[idx_sfList]

        effminmax =  findMinMax_v2( effDataList )
        effiMin = effminmax[0]
        effiMax = effminmax[1]

        sfminmax =  findMinMax( sfList )
        sfMin = sfminmax[0]

        for key in sorted(effDataList.keys()):
            grBinsEffData = Cut_and_Count_effUtil.makeTGraphAsymErrorFromList(effDataList[key], 'min', 'max')
            grBinsSF      = Cut_and_Count_effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')
            
            grBinsEffMC = None
            if not effMCList is None:
                grBinsEffMC = Cut_and_Count_effUtil.makeTGraphFromList(effMCList[key], 'min', 'max') # use symmetric error for scale factor plot
                grBinsEffMC.SetLineColor( rt.kBlack )
                grBinsEffMC.SetMarkerStyle( 24 )
                grBinsEffMC.SetLineWidth( 1 )

            grBinsSF     .SetMarkerColor( graphColors[igr] )
            grBinsSF     .SetLineColor(   graphColors[igr] )
            grBinsSF     .SetLineWidth(2)
            grBinsEffData.SetMarkerColor( graphColors[igr] )
            grBinsEffData.SetLineColor(   graphColors[igr] )
            grBinsEffData.SetLineWidth(2)

            grBinsEffData.GetHistogram().SetMinimum(effiMin)
            grBinsEffData.GetHistogram().SetMaximum(effiMax)

            grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
            grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
            grBinsSF.GetHistogram().SetMinimum(sfMin)
            grBinsSF.GetHistogram().SetMaximum(sfMax)

            grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
            if 'eta' in xAxis or 'Eta' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #eta")
            elif 'pt' in xAxis or 'pT' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC E_{T}  [GeV]")
            elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")
            elif 'phi' in xAxis or 'Phi' in xAxis:
                grBinsSF.GetHistogram().GetXaxis().SetTitle("SC #phi")
            elif 'z' in xAxis or 'Z' in xAxis :
                grBinsSF.GetHistogram().GetXaxis().SetTitle("z [cm]")

            grBinsSF.GetHistogram().GetYaxis().SetTitle("Data/ " + denomNameList[idx_sfList] )
            grBinsSF.GetHistogram().GetYaxis().SetTitleOffset(1)

            grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
            grBinsEffData.GetHistogram().GetYaxis().SetTitle("Efficiency" )
            grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )

            ### to avoid loosing the TGraph keep it in memory by adding it to a list
            listOfTGraph1.append( grBinsEffData )
            listOfTGraph2.append( grBinsSF )
            listOfMC.append( grBinsEffMC   )

            # check if the ratio is ratio of itself, and if true don't draw the ratio graph
            if fileNameList[idx_sfList] == denomNameList[idx_sfList] : 
               listOfTGraph2_.append( False )
            else : listOfTGraph2_.append( True )

            if 'eta' in yAxis or 'Eta' in yAxis:
                leg.AddEntry( grBinsEffData,  name, "PL")
            elif 'pt' in yAxis or 'pT' in yAxis:
                leg.AddEntry( grBinsEffData, name, "PL")
            elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
                leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")  

        idx_sfList = idx_sfList + 1

    if not effMCList is None:
       leg.AddEntry( grBinsEffMC, 'MC', "PL")

    #for igr in range(len(listOfTGraph1)+1):
    for igr in range(len(listOfTGraph1)):

        option = "APE"
        #if igr == 1:
        #    option = "APE" # Don't know why axis is drawn in the second graph. I changed to draw axis in the first graph, and looks ok now.

        if not igr == 0:
            option = "PE"

        use_igr = igr
        if use_igr == len(listOfTGraph1):
            use_igr = 0

        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        #if not listOfMC[use_igr] is None:
        #    listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.2)
        if 'pT' not in xAxis : listOfTGraph1[use_igr].GetHistogram().SetMinimum(0.92)
        if 'pT' not in xAxis : listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.05)

        #listOfTGraph1[use_igr].GetHistogram().SetMaximum(1.05) # et plot

        listOfTGraph1[use_igr].GetHistogram().SetLabelSize(0)

        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetLabelFont(63)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetLabelSize(30)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleFont(63)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleSize(30)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleOffset(1.5)

        p1.cd()
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            #listOfMC[use_igr].Draw("ez")
            listOfMC[use_igr].Draw("pesame")

        p2.cd()
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)

        listOfTGraph2[use_igr].GetHistogram().SetMinimum(0.87)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(1.12)

        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelFont(63)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelSize(30)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleFont(63)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleSize(30)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleOffset(1.5)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelFont(63)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelSize(25)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleFont(63)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleSize(30)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleOffset(3.5)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetNdivisions(505)

        if 'pT' in xAxis or 'pt' in xAxis :
            listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        if listOfTGraph2_[use_igr] : 
           listOfTGraph2[use_igr].Draw(option)

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)

    p2.cd()
    lineAtOne.Draw()
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    leg.Draw()

    eb_ee = rt.TLatex()
    if 'eta' not in xAxis :
        eb_ee.SetTextSize(0.03)
        if 'EB' == EB_or_EE : eb_ee.DrawLatex(0.65,0.9, "|#eta_{SC}| < 1.479") # for et plot
        if 'EE' == EB_or_EE : eb_ee.DrawLatex(0.65,0.9, "|#eta_{SC}| > 1.479")

        #if 'EB' == EB_or_EE : eb_ee.DrawLatex(0.52,0.9, "|#eta_{SC}| < 1.479")
        #if 'EE' == EB_or_EE : eb_ee.DrawLatex(0.52,0.9, "|#eta_{SC}| > 1.479")

    CMS_lumi.CMS_lumi(c, 4, 10)

    c.Print(nameout)


def EffiGraphAsymError1D(effDataList, effMCList, sfList ,nameout, xAxis = 'pT', yAxis = 'eta'):
            
    W = 800
    H = 800
    yUp = 0.45
    canName = 'toto' + xAxis

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.10)
    c.SetLeftMargin(0.12)
    
    
    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.0075)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p2.SetTopMargin(   0.0075)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    firstGraph = True
    leg = rt.TLegend(0.5,0.8,0.95 ,0.93)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfMC      = []

    xMin = 10
    xMax = 500
    if 'pT' in xAxis or 'pt' in xAxis:
        #p1.SetLogx()
        #p2.SetLogx()    
        xMin = 0
        xMax = 60
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  0
        xMax = 70
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.60
        xMax = +2.60
    
    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    effminmax =  findMinMax_v2( effDataList )
    effiMin = effminmax[0]
    effiMax = effminmax[1]

    #effiMin = 0.
    #effiMax = effminmax[1]

    sfminmax =  findMinMax( sfList )
    sfMin = sfminmax[0]
    sfMin = 0.8
    #sfMax = 1.2

    for key in sorted(effDataList.keys()):
        grBinsEffData = Cut_and_Count_effUtil.makeTGraphAsymErrorFromList(effDataList[key], 'min', 'max')
        grBinsSF      = Cut_and_Count_effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')
        grBinsEffMC = None
        if not effMCList is None:
            grBinsEffMC = Cut_and_Count_effUtil.makeTGraphFromList(effMCList[key], 'min', 'max') # use symmetric error for scale factor plot
            grBinsEffMC.SetLineStyle( rt.kDashed )
            grBinsEffMC.SetLineColor( graphColors[igr] )
            grBinsEffMC.SetMarkerSize( 0 )
            grBinsEffMC.SetLineWidth( 2 )

        grBinsSF     .SetMarkerColor( graphColors[igr] )
        grBinsSF     .SetLineColor(   graphColors[igr] )
        grBinsSF     .SetLineWidth(2)
        grBinsEffData.SetMarkerColor( graphColors[igr] )
        grBinsEffData.SetLineColor(   graphColors[igr] )
        grBinsEffData.SetLineWidth(2) 
                
        grBinsEffData.GetHistogram().SetMinimum(effiMin)
        grBinsEffData.GetHistogram().SetMaximum(effiMax)

        grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram().SetMinimum(sfMin)
        grBinsSF.GetHistogram().SetMaximum(sfMax)
        
        grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
        if 'eta' in xAxis or 'Eta' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SuperCluster #eta")
        elif 'pt' in xAxis or 'pT' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("p_{T}  [GeV]")  
        elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")  
            
        grBinsSF.GetHistogram().GetYaxis().SetTitle("Data / MC " )
        grBinsSF.GetHistogram().GetYaxis().SetTitleOffset(1)
            
        grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
        grBinsEffData.GetHistogram().GetYaxis().SetTitle("Data efficiency" )
        grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )

            
        ### to avoid loosing the TGraph keep it in memory by adding it to a list
        listOfTGraph1.append( grBinsEffData )
        listOfTGraph2.append( grBinsSF ) 
        listOfMC.append( grBinsEffMC   )
        if 'eta' in yAxis or 'Eta' in yAxis:
            leg.AddEntry( grBinsEffData, '%1.3f #leq | #eta | #leq  %1.3f' % (float(key[0]),float(key[1])), "PL")        
        elif 'pt' in yAxis or 'pT' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq p_{T} #leq  %3.0f GeV' % (float(key[0]),float(key[1])), "PL")        
        elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")        

        
    for igr in range(len(listOfTGraph1)+1):

        option = "P"
        if igr == 1:
            option = "AP"

        use_igr = igr
        if use_igr == len(listOfTGraph1):
            use_igr = 0
            
        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(effiMax)
        p1.cd()
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].Draw("ez")

        p2.cd()            
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)
        #if 'pT' in xAxis or 'pt' in xAxis :
            #listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        listOfTGraph2[use_igr].Draw(option)
        

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    leg.Draw()    
    CMS_lumi.CMS_lumi(c, 4, 10)

    c.Print(nameout)

    return listOfTGraph2


def diagnosticErrorPlot( effgr, ierror, nameout ):
    errorNames = efficiency.getSystematicNames()
    c2D_Err = rt.TCanvas('canScaleFactor_%s' % errorNames[ierror] ,'canScaleFactor: %s' % errorNames[ierror],1000,600)    
    c2D_Err.Divide(2,1)
    c2D_Err.GetPad(1).SetLogy()
    c2D_Err.GetPad(2).SetLogy()
    c2D_Err.GetPad(1).SetRightMargin(0.15)
    c2D_Err.GetPad(1).SetLeftMargin( 0.15)
    c2D_Err.GetPad(1).SetTopMargin(  0.10)
    c2D_Err.GetPad(2).SetRightMargin(0.15)
    c2D_Err.GetPad(2).SetLeftMargin( 0.15)
    c2D_Err.GetPad(2).SetTopMargin(  0.10)

    h2_sfErrorAbs = effgr.ptEtaScaleFactor_2DHisto(ierror+1, False )
    h2_sfErrorRel = effgr.ptEtaScaleFactor_2DHisto(ierror+1, True  )
    h2_sfErrorAbs.SetMinimum(0)
    h2_sfErrorAbs.SetMaximum(min(h2_sfErrorAbs.GetMaximum(),0.2))
    h2_sfErrorRel.SetMinimum(0)
    h2_sfErrorRel.SetMaximum(1)
    h2_sfErrorAbs.SetTitle('e/#gamma absolute SF syst: %s ' % errorNames[ierror])
    h2_sfErrorRel.SetTitle('e/#gamma relative SF syst: %s ' % errorNames[ierror])
    c2D_Err.cd(1)
    h2_sfErrorAbs.DrawCopy("colz TEXT45")
    c2D_Err.cd(2)
    h2_sfErrorRel.DrawCopy("colz TEXT45")
    
    c2D_Err.Print(nameout)


# for data comparisons
def doPlots(filesin, lumi, axis = ['pT','eta'] ):

    effGraphList = []
    dataNameList = []
    denomNameList = []

    for filein in filesin :
        fileWithEff = open(filein, 'r')
        print 'open ' + filein

        temp_effGraph = Cut_and_count_efficiencyList()
        temp_name =  filein.replace('/','_').split('_')[7]
        temp_denomname =  (filein.replace('/','_').split('_')[10]).split('.txt')[0]
        print "temp_name: " + temp_name + " temp_denomname: " + temp_denomname

        print " Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi )
        CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi

        if not os.path.exists( filein ) :
            print 'file %s does not exist' % filein
            sys.exit(1)

        fileWithEff = open(filein, 'r')
        effGraph = Cut_and_count_efficiencyList()

        for line in fileWithEff :
            modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
            numbers = modifiedLine.split('\t')

            if len(numbers) > 0 and isFloat(numbers[0]):
                etaKey = ( float(numbers[0]), float(numbers[1]) )
                ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )

                myeff = Cut_and_count_efficiency(ptKey,etaKey,
                                   float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),float(numbers[8]),float(numbers[9]),float(numbers[10] ),float(numbers[11] ),
                                   float(numbers[12]),float(numbers[13]),float(numbers[14]),float(numbers[15]) )
#                               float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )

                #effGraph.addEfficiency(myeff)
                temp_effGraph.addEfficiency(myeff)

        fileWithEff.close()

        dataNameList.append(temp_name)
        denomNameList.append(temp_denomname)
        effGraphList.append(temp_effGraph)

        print " ------------------------------- "

    #print "nameOutBase: " + filesin[0].split("/")[0] + "/" + filesin[0].split("/")[1] + "/" + filesin[0].split("/")[2] + "/" + filesin[0].split("/")[3] + "/" + filesin[0].split("/")[4]  
    nameOutBase = filesin[0].split("/")[0] + "/" + filesin[0].split("/")[1] + "/" + filesin[0].split("/")[2] + "/" + filesin[0].split("/")[3] + "/" + filesin[0].split("/")[4] + "/"
    pdfout = nameOutBase + 'egammaPlots.pdf' # name for the final plot with all data
    print "pdf out: " + pdfout
    #cDummy = rt.TCanvas()
    #cDummy.Print( pdfout + "[" )


    if axis[0] == 'vtx' or axis[0] == 'pT':

       EffiGraph1D_multiData( effGraphList , #eff Data
                    None,
                    effGraphList , #SF
                    pdfout,
                    dataNameList ,
                    denomNameList ,
                    xAxis = axis[0], yAxis = axis[1])

       EffiGraph1D_multiData( effGraphList , #eff Data
                    None,
                    effGraphList , #SF
                    pdfout + '_EE.pdf',
                    dataNameList ,
                    denomNameList ,
                    xAxis = axis[0], yAxis = axis[1],
                    EB_or_EE = 'EE')

    if axis[0] == 'eta':
       EffiGraph1D_multiData( effGraphList , #eff Data
                              None,
                              effGraphList , #SF 
                              pdfout,
                              dataNameList,
                              denomNameList ,
                              xAxis = axis[0], yAxis = axis[1] )



    #cDummy.Print( pdfout + "]" )

def doEGM_SFs(filein, lumi, axis = ['pT','eta'], doCut_and_Count = False):
    print " Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi )
    CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi 

    nameOutBase = filein 
    if not os.path.exists( filein ) :
        print 'file %s does not exist' % filein
        sys.exit(1)


    fileWithEff = open(filein, 'r')
    if doCut_and_count:
        effGraph = Cut_and_count_efficiencyList()
    else:
        effGraph = efficiencyList()
    
    for line in fileWithEff :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]) )
            ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )
        
            if doCut_and_count:
                myeff = Cut_and_count_efficiency(ptKey,etaKey,
                                float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),float(numbers[8]),float(numbers[9]),float(numbers[10] ),float(numbers[11] ),
                                float(numbers[12]),float(numbers[13]),float(numbers[14]),float(numbers[15]) )
    #                           float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )
            else:
                myeff = efficiency(ptKey, etaKey,
                                float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),
                                float(numbers[8]),float(numbers[9]),float(numbers[10]),float(numbers[11]) )
    #                           float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )
            effGraph.addEfficiency(myeff)

    fileWithEff.close()

### massage the numbers a bit
    if not doCut_and_count:
        effGraph.symmetrizeSystVsEta()
        effGraph.combineSyst()

    print " ------------------------------- "

    customEtaBining = []
    customEtaBining.append( (0.000,0.800))
    customEtaBining.append( (0.800,1.444))
    customEtaBining.append( (1.444,1.566))
    customEtaBining.append( (1.566,2.000))
    customEtaBining.append( (2.000,2.500))


    pdfout = nameOutBase + '_egammaPlots.pdf'
    cDummy = rt.TCanvas()
    cDummy.Print( pdfout + "[" )

    if doCut_and_count:    
        EffiGraphAsymError1D( effGraph.pt_1DGraphAsymError_list( False ) , #eff Data
                             None, 
                             effGraph.pt_1DGraph_list( True ) , #SF
                            pdfout,
                            xAxis = axis[0], yAxis = axis[1] )
        listOfSF1D = EffiGraphAsymError1D( effGraph.eta_1DGraphAsymError_list( typeGR =  0 ) , # eff Data
                                            effGraph.eta_1DGraphAsymError_list( typeGR = -1 ) , # eff MC
                                            effGraph.eta_1DGraphAsymError_list( typeGR = +1 ) , # SF
                                            pdfout, 
                                            xAxis = axis[1], yAxis = axis[0] )
    else:
        EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, False ) , #eff Data
                    None, 
                    effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, True ) , #SF
                    pdfout,
                    xAxis = axis[0], yAxis = axis[1] )

        #EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,False) , 
        #             effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,True)   , False, pdfout )
        #EffiGraph1D( effGraph.eta_1DGraph_list(False), effGraph.eta_1DGraph_list(True), True , pdfout )
        listOfSF1D = EffiGraph1D( effGraph.eta_1DGraph_list( typeGR =  0 ) , # eff Data
                            effGraph.eta_1DGraph_list( typeGR = -1 ) , # eff MC
                                effGraph.eta_1DGraph_list( typeGR = +1 ) , # SF
                              pdfout, 
                              xAxis = axis[1], yAxis = axis[0] )


    h2EffData = effGraph.ptEtaScaleFactor_2DHisto(-3)
    h2EffMC   = effGraph.ptEtaScaleFactor_2DHisto(-2)
    h2SF      = effGraph.ptEtaScaleFactor_2DHisto(-1)
    h2Error   = effGraph.ptEtaScaleFactor_2DHisto( 0)  ## only error bars

    rt.gStyle.SetPalette(1)
    rt.gStyle.SetPaintTextFormat('1.3f');
    rt.gStyle.SetOptTitle(1)

    c2D = rt.TCanvas('canScaleFactor','canScaleFactor',900,600)
    c2D.Divide(2,1)
    c2D.GetPad(1).SetRightMargin(0.15)
    c2D.GetPad(1).SetLeftMargin( 0.15)
    c2D.GetPad(1).SetTopMargin(  0.10)
    c2D.GetPad(2).SetRightMargin(0.15)
    c2D.GetPad(2).SetLeftMargin( 0.15)
    c2D.GetPad(2).SetTopMargin(  0.10)
    c2D.GetPad(1).SetLogy()
    c2D.GetPad(2).SetLogy()
    

    c2D.cd(1)
    dmin = 1.0 - h2SF.GetMinimum()
    dmax = h2SF.GetMaximum() - 1.0
    dall = max(dmin,dmax)
    h2SF.SetMinimum(1-dall)
    h2SF.SetMaximum(1+dall)
    h2SF.DrawCopy("colz TEXT45")
    
    c2D.cd(2)
    h2Error.SetMinimum(0)
    h2Error.SetMaximum(min(h2Error.GetMaximum(),0.2))    
    h2Error.DrawCopy("colz TEXT45")

    c2D.Print( pdfout )
    listName = pdfout.split('/')
    for iext in ["pdf","C","png"]:
        c2D.SaveAs(pdfout.replace('egammaEffi.txt_egammaPlots',listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3]).replace('pdf',iext))

    rootout = rt.TFile(nameOutBase + '_EGM2D.root','recreate')
    rootout.cd()
    h2SF.Write('EGamma_SF2D',rt.TObject.kOverwrite)
    h2EffData.Write('EGamma_EffData2D',rt.TObject.kOverwrite)
    h2EffMC  .Write('EGamma_EffMC2D'  ,rt.TObject.kOverwrite)
    for igr in range(len(listOfSF1D)):
        listOfSF1D[igr].Write( 'grSF1D_%d' % igr, rt.TObject.kOverwrite)


    errorNames = efficiency.getSystematicNames()
    for isyst in range(len(errorNames)):
        h2_isyst = diagnosticErrorPlot( effGraph, isyst, pdfout )
        h2_isyst.Write( errorNames[isyst],rt.TObject.kOverwrite)
    cDummy.Print( pdfout + "]" )
    rootout.Close()



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='tnp EGM scale factors')
    parser.add_argument('--lumi'  , type = float, default = -1, help = 'Lumi (just for plotting purpose)')
    parser.add_argument('txtFile' , default = None, help = 'EGM formatted txt file')
    parser.add_argument('--PV'    , action  = 'store_true', help = 'plot 1 vs nVtx instead of pT' )
    args = parser.parse_args()

    if args.txtFile is None:
        print ' - Needs EGM txt file as input'
        sys.exit(1)
    

    CMS_lumi.lumi_13TeV = "5.5 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.lumi_sqrtS = "13 TeV"
    
    axis = ['pT','eta']
    if args.PV:
        axis = ['nVtx','eta']

    doEGM_SFs(args.txtFile, args.lumi,axis, doCut_and_Count =False)
