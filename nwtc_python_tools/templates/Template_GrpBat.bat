:: Remote Execution Batch File: {:s<GrpBatPath>}
{:s<TimeStamp>}

::@ECHO Off

@NET USE A:    "{:s<BatDir>}"    /persistent:no
@SET MESSFILE="A:\\Messages\{:s<GrpBatMsgName>}"

@rem #mlb NET USE

@SET HostName=%COMPUTERNAME%
@SET FAST={:s<FastExePath>}
@IF EXIST %FAST% GOTO FASTOK
  @ECHO Fast executable '{:s<FastExePath>}' does not exist!
  @ECHO RunIEC job is terminating
  @ECHO Fast executable '{:s<FastExePath>}' does not exist! >> %MESSFILE%
  @ECHO RunIEC job is terminating >> %MESSFILE%
  @EXIT
:FASTOK

:: Save current drive so we go back to the right place
FOR %%A in ("%CD%") DO SET MyDrive=%%~dA

@ECHO This job is running on: %HostName% at %Date% %Time%   >> %MESSFILE%
@ECHO   Batch file {:s<GrpBatPath>}                        >> %MESSFILE%
@ECHO   FAST: %FAST%                                        >> %MESSFILE%

:: Move to A:

@NET USE             >> %MESSFILE%
@A:   >> %MESSFILE%
FOR %%A in ("%CD%") DO SET RunDrive=%%~dA
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>})
@rem #mlb ECHO Running from: %RunDrive% ({:s<BatDir>}) >> %MESSFILE%

:: =================================== Simulations ======================

