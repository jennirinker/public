:: Remote Execution Batch File: {:s<BatPath>}
{:s<BatCmnt>}

@ECHO Off

@NET USE A:    "{:s<BatDir>}"    /persistent:no
@SET MESSFILE="A:\\Messages\{:s<BatMsgName>}"
@ECHO Mounting file servers.                                         >  %MESSFILE%
@NET USE S:    "{:s<ExeDir>}"    /persistent:no >> %MESSFILE%

@rem #mlb NET USE

:: Check that the executable exists
@SET HostName=%COMPUTERNAME%
@SET EXE={:s<ExePath>}
@IF EXIST %EXE% GOTO EXEEXISTS
  @ECHO Executable '{:s<ExePath>}' does not exist!
  @ECHO {:s<BatName>} job is terminating
  @ECHO Executable '{:s<ExePath>}' does not exist! >> %MESSFILE%
  @ECHO {:s<BatName>} job is terminating >> %MESSFILE%
  @EXIT
:EXEEXISTS

:: Save current drive so we go back to the right place
FOR %%A in ("%CD%") DO SET MyDrive=%%~dA

@ECHO This job is running on: %HostName% at %Date% %Time%   >> %MESSFILE%
@ECHO   Batch file {:s<BatPath>}  >> %MESSFILE%
@ECHO   EXEPATH: %EXE%                            >> %MESSFILE%

:: Move to A:
@NET USE             >> %MESSFILE%
@A:   >> %MESSFILE%
FOR %%A in ("%CD%") DO SET RunDrive=%%~dA
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>})
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>}) >> %MESSFILE%

:: ====================== Run executable ====================

@ECHO  ================== Simulation {:s<FileID>} ================== >  %MESSFILE%
@ECHO  Running executable {:s<ExeName>}  >  %MESSFILE%
{:s<ExeCmnd>}  >> %MESSFILE%
@IF %ERRORLEVEL% == 0 GOTO :NOERROR
  @ECHO Error %ERRORLEVEL% while running executable {:s<ExeName>}!
  @ECHO {:s<BatName>} job is terminating
  @ECHO Error %ERRORLEVEL% while running executable {:s<ExeName>}! >> %MESSFILE%
  @ECHO {:s<BatName>} job is terminating >> %MESSFILE%
  @EXIT /B
:NOERROR
@ECHO Executable {:s<ExeName>} finished successfully.      >> %MESSFILE%

@ECHO This job ran on: %HostName% finishing at %Date% %Time%

