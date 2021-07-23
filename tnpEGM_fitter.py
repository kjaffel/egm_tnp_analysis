#import ctypes
#libc = ctypes.CDLL("libc.so.6")
#libc.malloc_trim(0)

### python specific import
import argparse
import os
import sys
import pickle
import shutil


parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--addGaus'    , action='store_true'  , help = 'add gaussian to alternate signal model failing probe')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('settings'     , default = None       , help = 'setting file [mandatory]')
parser.add_argument('--doCutCount' , action='store_true'  , help = 'calculate cut and count efficiency')
parser.add_argument('--isPassOverTotal', action='store_true'  , default = False, help = 'efficiency definition: pass/ total not pass/ (pass+fail)')
parser.add_argument('--plotX'      , default = None       , help ='x axis of plot to draw') # plot type to draw
parser.add_argument('--onlyDoPlot' , action='store_true'  , help = 'do not create SF root files and systematic plots', default = False)
parser.add_argument('--flagForTotal', default = None      , help ='WP to test')
parser.add_argument('--doHLT'       , action='store_true' , default = True, help ='Produce HLT efficency maps if False will do Egamma ID/ISO and reco scale factors')
args = parser.parse_args()

print '===> settings %s <===' % args.settings
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
print importSetting
exec(importSetting)

### tnp library
import libPython.binUtils  as tnpBiner
import libPython.rootUtils as tnpRoot

if args.flag is None:
    print '[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py'
    sys.exit(0)
    
if not args.flag in tnpConf.flags.keys() :
    print '[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag
    print '  --> define in settings first'
    print '  In settings I found flags: '
    print tnpConf.flags.keys()
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print '===>  Output directory: '
print outputDirectory


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print tnpBins['bins'][ib]['name']
        print '  - cut: ',tnpBins['bins'][ib]['cut']
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( outputDirectory ):
        shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print 'created dir: %s ' % outputDirectory
    print 'bining created successfully... '
    print 'Note than any additional call to createBins will overwrite directory %s' % outputDirectory
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )


if args.createHists:
    
    import libPython.histUtils as tnpHist

    if args.doHLT:
        flagTotal = None
        if not args.flagForTotal is None:
            flagTotal = tnpConf.flags[args.flagForTotal]
    
    for sampleType in tnpConf.samplesDef.keys():
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : continue
        if sampleType == args.sample or args.sample == 'all' :
            print 'creating histogram for sample '
            sample.dump()
            var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if sample.mcTruth:
                var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if args.doHLT:
                tnpRoot.makePassFailHistograms__( sample, tnpConf.flags[args.flag], tnpBins, var , args.isPassOverTotal, flagTotal)
            else:
                tnpHist.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var )

    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
if sampleToFit is None:
    print '[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings'
    sys.exit(1)

sampleMC = tnpConf.samplesDef['mcNom']

if sampleMC is None:
    print '[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings'
    sys.exit(1)
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'mcRef'     , sampleMC )
    setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altBkgFit' , '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )



### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = tnpConf.samplesDef['mcNom']

if  args.doFit:
    sampleToFit.dump()
    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            if args.altSig and not args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altSig and args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            else:
                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )

    args.doPlot = True
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fileName = sampleToFit.nominalFit
    fitType  = 'nominalFit'
    if args.altSig : 
        fileName = sampleToFit.altSigFit
        fitType  = 'altSigFit'
    if args.altBkg : 
        fileName = sampleToFit.altBkgFit
        fitType  = 'altBkgFit'
        
    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( fileName, tnpBins['bins'][ib], plottingDir )

    print ' ===> Plots saved in <======='
#    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:

    import libPython.EGammaID_scaleFactors as egm_sf
    
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        'dataNominal' : sampleToFit.nominalFit,
        'dataAltSig'  : sampleToFit.altSigFit ,
        'dataAltBkg'  : sampleToFit.altBkgFit ,
        'mcNominal'   : sampleToFit.mcRef.histFile,
        'mcAlt'       : None,
        'tagSel'      : None
        }

    if not tnpConf.samplesDef['mcAlt' ] is None:
        info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    if not tnpConf.samplesDef['tagSel'] is None:
        info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print astr
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print astr
            fOut.write( astr + '\n' )
            
        astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltBkg' ][0],
            effis['dataAltSig' ][0],
            effis['mcAlt' ][0],
            effis['tagSel'][0],
            )
        print astr
        fOut.write( astr + '\n' )
    fOut.close()

    print 'Effis saved in file : ',  effFileName
    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi, doCut_and_Count =False)


####################################################################
##### dumping egamma txt file (cut and count) 
####################################################################
if args.doCutCount:

    import libPython.EGammaID_scaleFactors as egm_sf

    dataList = [] # make list for the comparison between data

    isHLTPrescaled  = False
    for sampleType in tnpConf.samplesDef.keys():
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : continue

        if not sample.isMC and not sample.hltPS is None:
            isHLTPrescaled = True

        if not sampleType == "dataToCompare" and not sampleType == 'tagSel' and not sampleType == 'mcAlt' and not sampleType == 'mcNom':
            dataList.append(sample.histFile)
            #tnpRoot.makePassFailHistograms( sample, tnpConf.flags[args.flag], tnpBins, var ) # create root root file with histograms

    print "isHLTPrescaled : " + str(isHLTPrescaled)

    #dataList = ['results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//data_Run2018test_passTrackIsoLeg1.root', 'results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//data_Run2017_passTrackIsoLeg1.root', 'results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//data_Run2016_passTrackIsoLeg1.root']
    fOutList = [] # list of efficiency txt files

    # make efficiency txt files for each datum
    for datumList in dataList :
        denomName = ''
        print "data name check " + datumList
        info = {
            'dataNominal' : datumList,
            'dataAltSig'  : None ,
            'dataAltBkg'  : None,
            'denominator' : None, # denominator for the ratio plot can be data or mc
            'mcAlt'       : None,
            'tagSel'      : None
            }

        if not tnpConf.samplesDef['mcNom' ] is None:
            info['denominator'    ] = tnpConf.samplesDef['mcNom' ].histFile
            denomName = tnpConf.samplesDef['mcNom' ].name
        if not tnpConf.samplesDef['dataToCompare' ] is None:
            info['denominator'    ] = tnpConf.samplesDef['dataToCompare' ].histFile
            denomName = tnpConf.samplesDef['dataToCompare' ].name
        if not tnpConf.samplesDef['mcAlt' ] is None:
            info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
        if not tnpConf.samplesDef['tagSel'] is None:
            info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

        effis = None
        # results/EGamma2018/tnpEleTrig/eta/passingHLTleg1//data_Run2018Av1_passingHLTleg1.root
        # ex) datumList.split('/')[6] is data_Run2018Av1_passingHLTleg1.root

        effFileName ='%s/egammaEffi%s.txt' % (outputDirectory, (datumList.split('.')[0]).split('/')[-1] + '_' + denomName)
        fOut = open( effFileName,'w')
        fOutList.append(effFileName)
       
        for ib in range(len(tnpBins['bins'])):
            effis = tnpRoot.getAllCnCEffiAsymError( info, tnpBins['bins'][ib] , args.isPassOverTotal) # TODO isHLTPrescaled --> isPassOverTotal 

            ### formatting assuming 2D bining -- to be fixed        
            v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
            v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
            if ib == 0 :
                astr = '### var1 : %s' % v1Range[1]
                print astr
                fOut.write( astr + '\n' )
                astr = '### var2 : %s' % v2Range[1]
                print astr
                fOut.write( astr + '\n' )
                
            astr =  '%+8.3f\t%+8.3f\t%+8.3f\t%+8.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f\t%5.3f' % (
                float(v1Range[0]), float(v1Range[2]),
                float(v2Range[0]), float(v2Range[2]),
                # included the third and fourth element for asymmetric low/upper error 
                effis['dataNominal'][0],effis['dataNominal'][1],effis['dataNominal'][2],effis['dataNominal'][3],
                effis['denominator'  ][0],effis['denominator'  ][1],effis['denominator'  ][2],effis['denominator'  ][3],
                effis['dataAltBkg' ][0],
                effis['dataAltSig' ][0],
                effis['mcAlt' ][0],
                effis['tagSel'][0],
                )
            print astr
            fOut.write( astr + '\n' )
        fOut.close()

        print 'Effis saved in file : ',  effFileName

    #fOutList = ['results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//egammaEffidata_Run2018test_passTrackIsoLeg1_data_Run2016.txt','results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//egammaEffidata_Run2017_passTrackIsoLeg1_data_Run2016.txt','results/EGamma2018/tnpEleTrig/et/passTrackIsoLeg1//egammaEffidata_Run2016_passTrackIsoLeg1_data_Run2016.txt'] # list of efficiency txt files
    if not args.onlyDoPlot:
       egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi, doCut_and_Count =True) 
    if args.onlyDoPlot:
       if 'et' == args.plotX : egm_sf.doPlots(fOutList,sampleToFit.lumi) #efficiency vs pt
       if 'nvtx' == args.plotX : egm_sf.doPlots(fOutList,sampleToFit.lumi, ['vtx','eta']) #efficiency vs nvtx
       if 'eta' == args.plotX : egm_sf.doPlots(fOutList,sampleToFit.lumi, ['eta','pT']) # efficiency vs eta 
