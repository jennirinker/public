
:: =================================== Simulation {:s<FileID>} ======================

@SET SMSSFILE="A:\\Messages\{:s<FastInpBatMsgName>}"
@ECHO  ========= Simulation {:s<FileID>} ========= >  %SMSSFILE%
@ECHO  Creating Fast input file for FileID {:s<FileID>}.  >> %SMSSFILE%

python %FASTINP% {:s<FastInpCmnd>}  >> %SMSSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO {:s<FastInpBatName>} ran successfully.      >> %SMSSFILE%
@ECHO  Output is at {:s<FastInpPath>}. >> %SMSSFILE%
GOTO :SIMS1

:ERROR1
@ECHO   ==( {:s<FastInpBatName>} failed )==
@ECHO   ==( {:s<FastInpBatName>} failed )== >> %SMSSFILE%

:SIMS1
@ECHO This job ran on: %HostName% finishing at %Date% %Time%  >> %SMSSFILE%
:: EXIT /b 0
