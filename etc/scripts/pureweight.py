import etc.inputs.tnpSampleDef as tnpSamples
from libPython.tnpClassUtils import mkdir
import libPython.puReweighter as pu
import os

puType = 0
isUL = True
era = "UL2016"
ULegacy_tnpSamples_dictNm = ['UL2016_preVFP','UL2016_postVFP', 'UL2017', 'UL2018'] 
ReReco_tnpSamples_dictNm = ['LegacyReReco2016', 'ReReco2017', 'ReReco2018']

list_  = ULegacy_tnpSamples_dictNm if isUL else ReReco_tnpSamples_dictNm
#for suffix in list_ :

for sName in tnpSamples.UL2016_postVFP.keys():    
    sample = tnpSamples.UL2016_postVFP[sName]
    if sample is None : continue
#    if not 'rec' in sName : continue
#    if not 'Winter17' in sName : continue
    if not 'DY' in sName: continue
    if not sample.isMC: continue
        
    trees = {}
#    trees['ele'] = 'tnpEleIDs'
#    trees['pho'] = 'tnpPhoIDs'
#    trees['rec'] = 'GsfElectronToSC'
    trees['trig']= 'tnpEleTrig'
    for tree in trees:
#        dirout =  '/eos/cms/store/group/phys_egamma/swmukher/ntuple_2017_v2/PU/'
#        dirout =  '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2018_MINIAOD_Nm1/PU_Trees/'
#        dirout =  '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2018_AOD/PU_Trees/'
#        dirout =  '/eos/cms/store/group/phys_egamma/asroy/Tag-and-Probe_Tree/UL2016/PU_Trees/preVFP/'
        dirout = os.path.join('%s' %sample.path[0].split('mc')[0], 'PU_Trees/')
        mkdir(dirout)
        
        if   puType == 0 : sample.set_puTree( dirout + '%s_%s.pu.puTree.root'   % (sample.name,tree) )
        elif puType == 1 : sample.set_puTree( dirout + '%s_%s.nVtx.puTree.root' % (sample.name,tree) )
        elif puType == 2 : sample.set_puTree( dirout + '%s_%s.rho.puTree.root'  % (sample.name,tree) )
        sample.set_tnpTree(trees[tree]+'/fitter_tree')
        sample.dump()
        pu.reweight(sample, puType, era)
    
