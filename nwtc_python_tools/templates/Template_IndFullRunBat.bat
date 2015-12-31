:: Remote Execution Batch File: {:s<IndFullRunBatPath>}
{:s<IndFullRunBatCmnt>}

@ECHO Off

@NET USE A:    "{:s<BatDir>}"    /persistent:no
@SET MESSFILE="A:\\Messages\{:s<IndFullRunBatMsgName>}"

@rem #mlb NET USE

:: Check that all executables exist
@SET HostName=%COMPUTERNAME%
@SET TURBSIMINP={:s<TurbSimInpExePath>}
@SET TURBSIM={:s<TurbSimExePath>}
@SET FASTINP={:s<FastInpExePath>}
@SET FAST={:s<FastExePath>}
@IF EXIST %TURBSIMINP% GOTO TURBSIMINPOK
  @ECHO TurbSim input file executable '{:s<TurbSimInpExePath>}' does not exist!
  @ECHO {:s<IndFullRunBatName>} job is terminating
  @ECHO TurbSim input file executable  '{:s<TurbSimInpExePath>}' does not exist! >> %MESSFILE%
  @ECHO {:s<IndFullRunBatName>} job is terminating >> %MESSFILE%
  @EXIT
:TURBSIMINPOK
@IF EXIST %TURBSIM% GOTO TURBSIMOK
  @ECHO TurbSim executable '{:s<TurbSimExePath>}' does not exist!
  @ECHO {:s<IndFullRunBatName>} job is terminating
  @ECHO TurbSim executable '{:s<TurbSimExePath>}' does not exist! >> %MESSFILE%
  @ECHO {:s<IndFullRunBatName>} job is terminating >> %MESSFILE%
  @EXIT
:TURBSIMOK
@IF EXIST %FASTINP% GOTO FASTINPOK
  @ECHO Fast input file executable '{:s<FastInpExePath>}' does not exist!
  @ECHO {:s<IndFullRunBatName>} job is terminating
  @ECHO Fast input file executable '{:s<FastInpExePath>}' does not exist! >> %MESSFILE%
  @ECHO {:s<IndFullRunBatName>} job is terminating >> %MESSFILE%
  @EXIT
:FASTINPOK
@IF EXIST %FAST% GOTO FASTOK
  @ECHO Fast executable '{:s<FastExePath>}' does not exist!
  @ECHO {:s<IndFullRunBatName>} job is terminating
  @ECHO Fast executable '{:s<FastExePath>}' does not exist! >> %MESSFILE%
  @ECHO {:s<IndFullRunBatName>} job is terminating >> %MESSFILE%
  @EXIT
:FASTOK

:: Save current drive so we go back to the right place
FOR %%A in ("%CD%") DO SET MyDrive=%%~dA

@ECHO This job is running on: %HostName% at %Date% %Time%   >> %MESSFILE%
@ECHO   Batch file {:s<IndFullRunBatPath>}  >> %MESSFILE%
@ECHO   TURBSIMINP: %TURBSIMINP%                            >> %MESSFILE%
@ECHO   TURBSIM: %TURBSIM%                                  >> %MESSFILE%
@ECHO   FASTINP: %FASTINP%                                  >> %MESSFILE%
@ECHO   FAST: %FAST%                                        >> %MESSFILE%

:: Move to A:
@NET USE             >> %MESSFILE%
@A:   >> %MESSFILE%
FOR %%A in ("%CD%") DO SET RunDrive=%%~dA
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>})
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>}) >> %MESSFILE%

:: ====================== TurbSim/FAST runs ====================

:: --- Create TurbSim input file ---
@ECHO  Creating TurbSim input file for FileID {:s<FileID>} 
@ECHO  Creating TurbSim input file for FileID {:s<FileID>} >> %MESSFILE%
@CALL "A:\\{:s<TurbSimInpBatName>}"
@ECHO  FileID {:s<FileID>} TurbSimInp  ERRORLEVEL %ERRORLEVEL% >> %MESSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO TurbSim input file generated successfully.      >> %SMSSFILE%

:: --- Run TurbSim ---
:RUNTURBSIM
@ECHO  Running TurbSim for FileID {:s<FileID>}
@ECHO  Running TurbSim for FileID {:s<FileID>}>> %MESSFILE%
@CALL "A:\\{:s<TurbSimBatName>}"
@ECHO FileID {:s<FileID>} TurbSim ERRORLEVEL %ERRORLEVEL% >> %MESSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO TurbSim run successfully.      >> %SMSSFILE%
   
:: --- Create FAST input file ---
:FASTINP
@ECHO  Creating FAST input file for FileID {:s<FileID>}
@ECHO  Creating FAST input file for FileID {:s<FileID>} >> %MESSFILE%
@CALL "A:\\{:s<FastInpBatName>}"
@ECHO  FileID {:s<FileID>} FastInp ERRORLEVEL %ERRORLEVEL% >> %MESSFILE%
   IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO FAST input file generated successfully.      >> %SMSSFILE%
   
:: --- Run FAST ---
:RUNFAST
@ECHO  Running FAST for FileID {:s<FileID>}
@ECHO  Running FAST for FileID {:s<FileID>} >> %MESSFILE%
@CALL "A:\\{:s<FastBatName>}"
@ECHO  FileID {:s<FileID>} Fast ERRORLEVEL %ERRORLEVEL% >> %MESSFILE%
	IF ERRORLEVEL 1 GOTO :ERROR1
@ECHO Fast run successfully.      >> %SMSSFILE%
GOTO :ENDSIMS
   
:ERROR1 
@ECHO   ==( {:s<IndFullRunBatName>} failed )==
@ECHO   ==( Halting simulations )==
@ECHO   ==( {:s<IndFullRunBatName>} failed )== >> %SMSSFILE%
@ECHO   ==( Halting simulations )== >> %SMSSFILE%

:ENDSIMS
@ECHO This job ran on: %HostName% finishing at %Date% %Time%
