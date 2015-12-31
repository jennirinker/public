
:: =================================== Simulation {:s<FileID>} ======================

@SET SMSSFILE="A:\\Messages\{:s<TurbSimInpBatMsgName>}"
@ECHO  ========= Simulation {:s<FileID>} ========= >  %SMSSFILE%
@ECHO  Creating TurbSim input file for FileID {:s<FileID>}.  >> %SMSSFILE%

python %TURBSIMINP% {:s<TurbSimInpCmnd>}  >> %SMSSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO {:s<TurbSimInpBatName>} ran successfully.      >> %SMSSFILE%
@ECHO  Output is at {:s<TurbSimInpPath>}. >> %SMSSFILE%
GOTO :SIMS1

:ERROR1
@ECHO   ==( {:s<TurbSimInpBatName>} failed )==
@ECHO   ==( {:s<TurbSimInpBatName>} failed )== >> %SMSSFILE%

:SIMS1
@ECHO This job ran on: %HostName% finishing at %Date% %Time%  >> %SMSSFILE%
:: EXIT /b 0
