from libPython.tnpClassUtils import tnpSample

#github branches
#LegacyReReco2016: https://github.com/swagata87/egm_tnp_analysis/tree/Legacy2016_94XIDv2 
#ReReco2017: https://github.com/swagata87/egm_tnp_analysis/tree/tnp_2017datamc_IDV2_10_2_0
#PromptReco2018: https://github.com/swagata87/egm_tnp_analysis/tree/egm_tnp_Prompt2018_102X_10222018_MC102XECALnoiseFix200kRelVal
#UL2017: https://github.com/swagata87/egm_tnp_analysis/blob/UL2017Final/etc/inputs/tnpSampleDef.py

### eos repositories
eosLegacyReReco2016 = '/eos/cms/store/group/phys_egamma/swmukher/egmNtuple_V2ID_2016/'
eosReReco2017 = '/eos/cms/store/group/phys_egamma/swmukher/ntuple_2017_v2/'
eosReReco2018 = '/eos/cms/store/group/phys_egamma/swmukher/rereco2018/ECAL_NOISE/'
##eosUL2017 = '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2017/'
#eosUL2017 = '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2017_MINIAOD_Nm1/'
#eosUL2018 = '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2018_MINIAOD_Nm1/'
#eosUL2016 = '/eos/cms/store/group/phys_egamma/akapoor/Tag-and-Probe_Tree/UL2016_ntuples/'

## Khawla Jaffel 
eosUL2016_preVFP = ''
eosUL2016_postVFP = '/storage/data/cms/store/user/kjaffel/TagandProbe/RunIISummer20UL_ver-2021-07-20__ext3/UL2016_postVFP/'
eosUL2017 = '/storage/data/cms/store/user/kjaffel/TagandProbe/RunIISummer20UL_ver-2021-07-18__ext2/UL2017/'
eosUL2018 = ''

ReReco2017 = {
    'DY_madgraph'   : tnpSample('DY_madgraph', eosReReco2017 + 'DYJetsToLL.root', isMC = True, nEvts =  -1 ),
    'DY_1j_madgraph': tnpSample('DY_1j_madgraph', eosReReco2017 + 'DY1JetsToLLM50madgraphMLM.root',isMC = True, nEvts =  -1 ),
#   'DY_amcatnlo'   : tnpSample('DY_amcatnlo', eosMoriond18 + 'DYJetsToLLM50amcatnloFXFX.root', isMC = True, nEvts =  -1 ),
    'DY_amcatnloext': tnpSample('DY_amcatnloext', eosReReco2017 + 'DYJetsToLLM50amcatnloFXFXext.root', isMC = True, nEvts =  -1 ),
    
    'data_Run2017B' : tnpSample('data_Run2017B' , eosReReco2017 + 'RunB.root' , lumi = 4.793 ),
    'data_Run2017C' : tnpSample('data_Run2017C' , eosReReco2017 + 'RunC.root' , lumi = 9.753),
    'data_Run2017D' : tnpSample('data_Run2017D' , eosReReco2017 + 'RunD.root' , lumi = 4.320 ),
    'data_Run2017E' : tnpSample('data_Run2017E' , eosReReco2017 + 'RunE.root' , lumi = 8.802),
    'data_Run2017F' : tnpSample('data_Run2017F' , eosReReco2017 + 'RunF.root' , lumi = 13.567),
    }

LegacyReReco2016 = {
    'DY_madgraph' : tnpSample('DY_madgraph', eosLegacyReReco2016 + 'TnPTree_DY_M50_madgraphMLM.root', isMC = True, nEvts =  -1 ),
    'DY_amcatnlo' : tnpSample('DY_amcatnlo', eosLegacyReReco2016 + 'TnPTree_DY_M50_amcatnloFXFX.root', isMC = True, nEvts =  -1 ),

    'data_Run2016Bv2' : tnpSample('data_Run2017Bv2' , eosLegacyReReco2016 + 'TnPTree_2016B_2.root' , lumi = 5.785 ),
    'data_Run2016C' : tnpSample('data_Run2017C' , eosLegacyReReco2016 + 'TnPTree_2016C.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2017D' , eosLegacyReReco2016 + 'TnPTree_2016D.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2017E' , eosLegacyReReco2016 + 'TnPTree_2016E.root' , lumi = 3.947 ),
    'data_Run2016F' : tnpSample('data_Run2017F' , eosLegacyReReco2016 + 'TnPTree_2016F.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2017G' , eosLegacyReReco2016 + 'TnPTree_2016G.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2017H' , eosLegacyReReco2016 + 'TnPTree_2016H.root' , lumi = 7.813 ),
    }

ReReco2018 = {
    ### MiniAOD TnP for IDs scale 
    'DY_madgraph'   : tnpSample('DY_madgraph', eosReReco2018 + 'DYJetsToLLmadgraphMLM.root', isMC = True, nEvts =  -1 ),
    'DY_powheg'     : tnpSample('DY_powheg', eosReReco2018 + 'DYToEEpowheg.root', isMC = True, nEvts =  -1 ),
    
    'data_Run2018A' : tnpSample('data_Run2018A' , eosReReco2018 + 'RunA.root' , lumi = 10.723),  
    'data_Run2018B' : tnpSample('data_Run2018B' , eosReReco2018 + 'RunB.root' , lumi = 5.964),
    'data_Run2018C' : tnpSample('data_Run2018C' , eosReReco2018 + 'RunC.root' , lumi = 6.382),
    'data_Run2018D' : tnpSample('data_Run2018D' , eosReReco2018 + 'RunD.root' , lumi = 29.181), 
    }


UL2017 = {
    ### MiniAOD TnP for HLT scale factors
    'DY_madgraph'   : tnpSample('DY_madgraph', eosUL2017 + 'mc/DYJetsToEE.root ', isMC = True, nEvts =  -1 ),
    'DY_amcatnloext': tnpSample('DY_amcatnloext', eosUL2017 + 'mc/DYJetsToLL_amcatnloFXFX.root', isMC = True, nEvts =  -1 ),

    'data_RunUL2017B' : tnpSample('data_RunUL2017B' , eosUL2017 + 'data/SingleEle_RunB.root' , lumi = 4.793961427),
    'data_RunUL2017C' : tnpSample('data_RunUL2017C' , eosUL2017 + 'data/SingleEle_RunC.root' , lumi = 9.631214821 ),
    'data_RunUL2017D' : tnpSample('data_RunUL2017D' , eosUL2017 + 'data/SingleEle_RunD.root' , lumi = 4.247682053 ),
    'data_RunUL2017E' : tnpSample('data_RunUL2017E' , eosUL2017 + 'data/SingleEle_RunE.root' , lumi = 9.313642402 ),
    'data_RunUL2017F' : tnpSample('data_RunUL2017F' , eosUL2017 + 'data/SingleEle_RunF.root' , lumi = 13.510934811),
    }

UL2018 = {
    ### MiniAOD TnP for HLT scale factors
    'DY_madgraph'   : tnpSample('DY_madgraph', eosUL2018 + 'mc/DYJetsToLL_madgraphMLM.root', isMC = True, nEvts =  -1 ),
    'DY_amcatnloext': tnpSample('DY_amcatnloext', eosUL2018 + 'mc/DYJetsToLL_amcatnloFXFX.root', isMC = True, nEvts =  -1 ),
    
    'data_RunUL2018A' : tnpSample('data_RunUL2018A' , eosUL2018 + 'data/EGamma_RunA.root' , lumi = 14.02672485),
    'data_RunUL2018B' : tnpSample('data_RunUL2018B' , eosUL2018 + 'data/EGamma_RunB.root' , lumi = 7.060617355),
    'data_RunUL2018C' : tnpSample('data_RunUL2018C' , eosUL2018 + 'data/EGamma_RunC.root' , lumi = 6.894770971),
    'data_RunUL2018D' : tnpSample('data_RunUL2018D' , eosUL2018 + 'data/EGamma_RunD.root' , lumi = 31.74220577),
    }

UL2016_preVFP = {
    ### MiniAOD TnP for HLT scale factors
    'DY_madgraph_preVFP'   : tnpSample('DY_madgraph_preVFP', eosUL2016_preVFP + 'mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_preVFP_UL2016.root', isMC = True, nEvts =  -1 ),
    'DY_amcatnloext_preVFP': tnpSample('DY_amcatnloext_preVFP', eosUL2016_preVFP + 'mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_preVFP_UL2016.root', isMC = True, nEvts =  -1 ),
    
    'data_RunUL2016B_preVFP' : tnpSample('data_RunUL2016B_preVFP' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016B.root' , lumi = 0.030493962),
    'data_RunUL2016B_preVFP__ver2' : tnpSample('data_RunUL2016B_preVFP__ver2' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016B_ver2.root' , lumi = 5.879330594),
    'data_RunUL2016C_preVFP' : tnpSample('data_RunUL2016C_preVFP' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016C.root' , lumi = 2.64992914),
    'data_RunUL2016D_preVFP' : tnpSample('data_RunUL2016D_preVFP' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016D.root' , lumi = 4.292865604),
    'data_RunUL2016E_preVFP' : tnpSample('data_RunUL2016E_preVFP' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016E.root' , lumi = 4.185165152),
    'data_RunUL2016F_preVFP' : tnpSample('data_RunUL2016F_preVFP' , eosUL2016_preVFP + 'data/UL2016_SingleEle_Run2016F.root' , lumi = 2.725508364),
    }

UL2016_postVFP = {
    ### MiniAOD TnP for HLT scale factors
    'DY_madgraph_postVFP'   : tnpSample('DY_madgraph_postVFP', eosUL2016_postVFP + 'mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8__post-VFP.root', isMC = True, nEvts =  -1 ),
    'DY_amcatnloext_postVFP': tnpSample('DY_amcatnloext_postVFP', eosUL2016_postVFP + 'mc/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8__post-VFP.root', isMC = True, nEvts =  -1 ),

    'data_RunUL2016F_postVFP' : tnpSample('data_RunUL2016F_postVFP' , eosUL2016_postVFP + 'data/SingleElectron_RunUL2016F-postVFP.root' , lumi = 0.414987426),
    'data_RunUL2016G_postVFP' : tnpSample('data_RunUL2016G_postVFP' , eosUL2016_postVFP + 'data/SingleElectron_RunUL2016G-postVFP.root' , lumi = 7.634508755),
    'data_RunUL2016H_postVFP' : tnpSample('data_RunUL2016H_postVFP' , eosUL2016_postVFP + 'data/SingleElectron_RunUL2016H-postVFP.root' , lumi = 8.802242522),
    }
