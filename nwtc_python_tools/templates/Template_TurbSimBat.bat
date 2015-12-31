
:: =================================== Simulation {:s<FileID>} ======================

@SET SMSSFILE="A:\\Messages\{:s<TurbSimBatMsgName>}"
@ECHO  ========= Simulation {:s<FileID>} ========= >  %SMSSFILE%
@ECHO  Creating TurbSim input file for FileID {:s<FileID>}.  >> %SMSSFILE%

%TURBSIM% {:s<TurbSimInpPath>}  >> %SMSSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO {:s<TurbSimBatName>} ran successfully.      >> %SMSSFILE%
@ECHO  Output is at {:s<TurbSimOutPath>}. >> %SMSSFILE%
GOTO :SIMS1

:ERROR1
@ECHO   ==( {:s<TurbSimBatName>} failed )==
@ECHO   ==( {:s<TurbSimBatName>} failed )== >> %SMSSFILE%

:SIMS1
@ECHO This job ran on: %HostName% finishing at %Date% %Time%  >> %SMSSFILE%
:: EXIT /b 0
