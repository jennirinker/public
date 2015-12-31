
:: =================================== Simulation {:s<FileID>} ======================

@SET SMSSFILE="A:\\Messages\{:s<FastBatMsgName>}"
@ECHO  ========= Simulation {:s<FileID>} ========= >  %SMSSFILE%
@ECHO  Creating Fast input file for FileID {:s<FileID>}.  >> %SMSSFILE%

%FAST% {:s<FastInpPath>}  >> %SMSSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO {:s<FastBatName>} ran successfully.      >> %SMSSFILE%
@ECHO  Output is at {:s<FastOutPath>}. >> %SMSSFILE%
GOTO :SIMS1

:ERROR1
@ECHO   ==( {:s<FastBatName>} failed )==
@ECHO   ==( {:s<FastBatName>} failed )== >> %SMSSFILE%

:SIMS1
@ECHO This job ran on: %HostName% finishing at %Date% %Time%  >> %SMSSFILE%
:: EXIT /b 0
