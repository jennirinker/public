
:: =================================== Simulation {:s<SimID>} ======================

@SET SMSSFILE="A:\\Messages\{:s<IndBatMsgName>}"
@ECHO  ========= Simulation {:s<SimID>} ========= >  %SMSSFILE%
@ECHO  Running FAST for case {:s<IndBatName>}.  >> %SMSSFILE%

%FAST% {:s<FastInPath>}   >> %SMSSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO Case {:s<IndBatName>} successfully ran.      >> %SMSSFILE%
@ECHO  Output is at {:s<FastOutName>}. >> %SMSSFILE%
GOTO :SIMS1

:ERROR1
@ECHO   ==( Case {:s<IndBatName>} failed )==
@ECHO   ==( Case {:s<IndBatName>} failed )== >> %SMSSFILE%

:SIMS1
@ECHO This job ran on: %HostName% finishing at %Date% %Time%  >> %SMSSFILE%
:: EXIT /b 0
