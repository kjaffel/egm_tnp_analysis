#############################################################
########## General settings
#############################################################

# flag to be Tested
flags = {
    'pass_HLT_Ele27_WPTight_Gsf'    : '(passHltEle27WPTightGsf == 1)',
    'pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVLLeg1L1match'    : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match == 1)', 
    'pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVLLeg2'  : '(passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2  == 1)',
    'pass_HLT_DoubleEle33_CaloIdL_MWSeedLegL1match'  : '(passHltDoubleEle33CaloIdLMWSeedLegL1match  == 1)',
    'pass_HLT_DoubleEle33_CaloIdL_MWUnsLeg'  : '(passHltDoubleEle33CaloIdLMWUnsLeg  == 1)',
    }

baseOutDir = 'results/TnP_RunIISummer20ULver21-07-22__ext3/UL2016_postVFP/tnpEleTrig/eta'

#############################################################
########## samples definition  - preparing the samples
#############################################################

### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples

#tnpTreeDir = 'GsfElectronToEleID'
tnpTreeDir = 'tnpEleTrig'

samplesDef = {
    'data'   : tnpSamples.UL2016_postVFP['data_RunUL2016F_postVFP'].clone(),
    'mcNom'  : tnpSamples.UL2016_postVFP['DY_madgraph_postVFP'].clone(),
    'mcAlt'  : tnpSamples.UL2016_postVFP['DY_amcatnloext_postVFP'].clone(),
    'tagSel' : tnpSamples.UL2016_postVFP['DY_madgraph_postVFP'].clone(),
    'dataToCompare' : None, #tnpSamples.UL2016_postVFP['data_RunUL2016F_postVFP'].clone(),
    }
## can add data sample easily
samplesDef['data'].add_sample( tnpSamples.UL2016_postVFP['data_RunUL2016G_postVFP'] )
samplesDef['data'].add_sample( tnpSamples.UL2016_postVFP['data_RunUL2016H_postVFP'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)
## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 33')

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#weightName = 'weight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking periods
weightName = 'weights_2016_run2016.totWeight' # FIXME 
putrees_path = '/storage/data/cms/store/user/kjaffel/TagandProbe/RunIISummer20UL_ver-2021-07-20__ext3/UL2016_postVFP/PU_Trees/'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('%s/DY_madgraph_postVFP_trig.pu.puTree.root' % putrees_path)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('%s/DY_amcatnloext_postVFP_trig.pu.puTree.root' % putrees_path)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('%s/DY_madgraph_postVFP_trig.pu.puTree.root' % putrees_path)


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
    { 'var' : 'el_sc_eta' , 'type': 'abs_float', 'bins': [0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 27.0, 28.5, 30.0, 35.0, 40.0, 45.0, 50.0,60.0,70.0,80.0,100.0, 150.0, 200.0, 250.0, 500.0, 600.0] },
              ]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut

#cutBase   = 'tag_sc_et > 30 && abs(tag_sc_eta) < 2.17'
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'
# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts__ = { 
    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    1 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    2 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    3 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    4 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    5 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    6 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    7 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    8 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
    9 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'
}

#### or remove any additional cut (default)
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [

    ### default
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",

    ]

tnpParAltSigFit = [
    ### default in Arun's setting
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[70.,50.,100.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
     
tnpParAltBkgFit = [
    #default
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",

    ]
        
