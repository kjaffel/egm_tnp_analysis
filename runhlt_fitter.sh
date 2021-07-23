#!/bin/bash
variables=(
'et'
'eta'
'nVtx')

flags=(
'pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVLLeg2' 
'pass_HLT_Ele27_WPTight_Gsf'
'pass_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVLLeg1L1match'
'pass_HLT_DoubleEle33_CaloIdL_MWSeedLegL1match'
'pass_HLT_DoubleEle33_CaloIdL_MWUnsLeg')

for var in ${variables[*]}; do
    for flag in ${flags[*]}; do
            echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            echo " Tag-and-Probe working on : Efficency vs $var  for Flag = $flag"
            echo " main-cmd :  python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doCutCount --onlyDoPlot --plotX ${var} --doHLT"
            echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

            python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --checkBins --doHLT 
            python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --createBins --doHLT
            python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --createHists --doHLT
            python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doCutCount --onlyDoPlot --plotX ${var} --doHLT
                # Nominal fit
            #python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doFit
                # MC fit to constrain alternate signal parameters [note this is the only MC fit that makes sense]
            #python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doFit --mcSig --altSig
                # Alternate signal fit (using constraints from previous fits)
            #python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doFit --altSig
                # Alternate background fit (using constraints from previous fits)
            #python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --doFit --altBkg
                # egm txt ouput file. Once all fits are fine, put everything in the egm format txt file
            #python tnpEGM_fitter.py etc/config/HLTsettings/settings_${var}_HLT.py --flag ${flag} --sumUp
    done
done
