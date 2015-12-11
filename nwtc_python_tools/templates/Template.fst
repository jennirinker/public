--------------------------------------------------------------------------------
------- FAST INPUT FILE --------------------------------------------------------
{:s}	FASTCmnt1	- FAST Comment 1
{:s}	FASTCmnt2	- FAST Comment 2
---------------------- SIMULATION CONTROL --------------------------------------
{:5s}       Echo        - Echo input data to "echo.out" (flag)
   {:1.0f}        ADAMSPrep   - ADAMS preprocessor mode {1: Run FAST, 2: use FAST as a preprocessor to create an ADAMS model, 3: do both} (switch)
   {:1.0f}        AnalMode    - Analysis mode {1: Run a time-marching simulation, 2: create a periodic linearized model} (switch)
   {:1.0f}        NumBl       - Number of blades (-)
{:6.1f}      TMax        - Total run time (s)
{:8.3f}    DT          - Integration time step (s)
---------------------- TURBINE CONTROL -----------------------------------------
   {:1.0f}        YCMode      - Yaw control mode {0: none, 1: user-defined from routine UserYawCont, 2: user-defined from Simulink/Labview} (switch)
{:6.1f}      TYCOn       - Time to enable active yaw control (s) [unused when YCMode=0]
   {:1.0f}        PCMode      - Pitch control mode {0: none, 1: user-defined from routine PitchCntrl, 2: user-defined from Simulink/Labview} (switch)
   {:3.1f}      TPCOn       - Time to enable active pitch control (s) [unused when PCMode=0]
   {:1.0f}        VSContrl    - Variable-speed control mode {0: none, 1: simple VS, 2: user-defined from routine UserVSCont, 3: user-defined from Simulink/Labview} (switch)
{:9.2f}   VS_RtGnSp   - Rated generator speed for simple variable-speed generator control (HSS side) (rpm) [used only when VSContrl=1]
{:9.2f}   VS_RtTq     - Rated generator torque/constant generator torque in Region 3 for simple variable-speed generator control (HSS side) (N-m) [used only when VSContrl=1]
{:10.6f}  VS_Rgn2K    - Generator torque constant in Region 2 for simple variable-speed generator control (HSS side) (N-m/rpm^2) [used only when VSContrl=1]
{:9.4E}   VS_SlPc     - Rated generator slip percentage in Region 2 1/2 for simple variable-speed generator control (%) [used only when VSContrl=1]
   {:1.0f}        GenModel    - Generator model {1: simple, 2: Thevenin, 3: user-defined from routine UserGen} (switch) [used only when VSContrl=0]
{:5s}       GenTiStr    - Method to start the generator {T: timed using TimGenOn, F: generator speed using SpdGenOn} (flag)
{:5s}       GenTiStp    - Method to stop the generator {T: timed using TimGenOf, F: when generator power = 0} (flag)
{:6.1f}      SpdGenOn    - Generator speed to turn on the generator for a startup (HSS speed) (rpm) [used only when GenTiStr=False]
   {:3.1f}      TimGenOn    - Time to turn on the generator for a startup (s) [used only when GenTiStr=True]
{:6.1f}      TimGenOf    - Time to turn off the generator (s) [used only when GenTiStp=True]
   {:1.0f}        HSSBrMode   - HSS brake model {1: simple, 2: user-defined from routine UserHSSBr, 3: user-defined from Labview} (switch)
{:6.1f}      THSSBrDp    - Time to initiate deployment of the HSS brake (s)
{:6.1f}      TiDynBrk    - Time to initiate deployment of the dynamic generator brake [CURRENTLY IGNORED] (s)
{:6.1f}      TTpBrDp(1)  - Time to initiate deployment of tip brake 1 (s)
{:6.1f}      TTpBrDp(2)  - Time to initiate deployment of tip brake 2 (s)
{:6.1f}      TTpBrDp(3)  - Time to initiate deployment of tip brake 3 (s) [unused for 2 blades]
{:6.1f}      TBDepISp(1) - Deployment-initiation speed for the tip brake on blade 1 (rpm)
{:6.1f}      TBDepISp(2) - Deployment-initiation speed for the tip brake on blade 2 (rpm)
{:6.1f}      TBDepISp(3) - Deployment-initiation speed for the tip brake on blade 3 (rpm) [unused for 2 blades]
{:6.1f}      TYawManS    - Time to start override yaw maneuver and end standard yaw control (s)
{:6.1f}      TYawManE    - Time at which override yaw maneuver reaches final yaw angle (s)
   0.0      NacYawF     - Final yaw angle for yaw maneuvers (degrees)
{:6.1f}      TPitManS(1) - Time to start override pitch maneuver for blade 1 and end standard pitch control (s)
{:6.1f}      TPitManS(2) - Time to start override pitch maneuver for blade 2 and end standard pitch control (s)
{:6.1f}      TPitManS(3) - Time to start override pitch maneuver for blade 3 and end standard pitch control (s) [unused for 2 blades]
{:6.1f}      TPitManE(1) - Time at which override pitch maneuver for blade 1 reaches final pitch (s)
{:6.1f}      TPitManE(2) - Time at which override pitch maneuver for blade 2 reaches final pitch (s)
{:6.1f}      TPitManE(3) - Time at which override pitch maneuver for blade 3 reaches final pitch (s) [unused for 2 blades]
{:6.1f}      BlPitch(1)  - Blade 1 initial pitch (degrees)
{:6.1f}      BlPitch(2)  - Blade 2 initial pitch (degrees)
{:6.1f}      BlPitch(3)  - Blade 3 initial pitch (degrees) [unused for 2 blades]
{:6.1f}      BlPitchF(1) - Blade 1 final pitch for pitch maneuvers (degrees)
{:6.1f}      BlPitchF(2) - Blade 2 final pitch for pitch maneuvers (degrees)
{:6.1f}      BlPitchF(3) - Blade 3 final pitch for pitch maneuvers (degrees) [unused for 2 blades]
---------------------- ENVIRONMENTAL CONDITIONS --------------------------------
{:10.5f}  Gravity     - Gravitational acceleration (m/s^2)
---------------------- FEATURE FLAGS -------------------------------------------
{:5s}       FlapDOF1    - First flapwise blade mode DOF (flag)
{:5s}       FlapDOF2    - Second flapwise blade mode DOF (flag)
{:5s}       EdgeDOF     - First edgewise blade mode DOF (flag)
{:5s}       TeetDOF     - Rotor-teeter DOF (flag) [unused for 3 blades]
{:5s}       DrTrDOF     - Drivetrain rotational-flexibility DOF (flag)
{:5s}       GenDOF      - Generator DOF (flag)
{:5s}       YawDOF      - Yaw DOF (flag)
{:5s}       TwFADOF1    - First fore-aft tower bending-mode DOF (flag)
{:5s}       TwFADOF2    - Second fore-aft tower bending-mode DOF (flag)
{:5s}       TwSSDOF1    - First side-to-side tower bending-mode DOF (flag)
{:5s}       TwSSDOF2    - Second side-to-side tower bending-mode DOF (flag)
{:5s}       CompAero    - Compute aerodynamic forces (flag)
{:5s}       CompNoise   - Compute aerodynamic noise (flag)
---------------------- INITIAL CONDITIONS --------------------------------------
{:6.1f}     OoPDefl     - Initial out-of-plane blade-tip displacement (meters)
{:6.1f}     IPDefl      - Initial in-plane blade-tip deflection (meters)
{:6.1f}      TeetDefl    - Initial or fixed teeter angle (degrees) [unused for 3 blades]
{:6.1f}      Azimuth     - Initial azimuth angle for blade 1 (degrees)
{:6.1f}      RotSpeed    - Initial or fixed rotor speed (rpm)
{:6.1f}      NacYaw      - Initial or fixed nacelle-yaw angle (degrees)
{:6.1f}     TTDspFA     - Initial fore-aft tower-top displacement (meters)
{:6.1f}     TTDspSS     - Initial side-to-side tower-top displacement (meters)
---------------------- TURBINE CONFIGURATION -----------------------------------
{:8.3f}    TipRad      - The distance from the rotor apex to the blade tip (meters)
{:8.3f}    HubRad      - The distance from the rotor apex to the blade root (meters)
   {:1.0f}        PSpnElN     - Number of the innermost blade element which is still part of the pitchable portion of the blade for partial-span pitch control [1 to BldNodes] [CURRENTLY IGNORED] (-)
{:6.1f}      UndSling    - Undersling length [distance from teeter pin to the rotor apex] (meters) [unused for 3 blades]
{:6.1f}      HubCM       - Distance from rotor apex to hub mass [positive downwind] (meters)
{:7.2f}     OverHang    - Distance from yaw axis to rotor apex [3 blades] or teeter pin [2 blades] (meters)
{:9.4f}   NacCMxn     - Downwind distance from the tower-top to the nacelle CM (meters)
{:6.1f}      NacCMyn     - Lateral  distance from the tower-top to the nacelle CM (meters)
{:9.4f}   NacCMzn     - Vertical distance from the tower-top to the nacelle CM (meters)
{:7.2f}     TowerHt     - Height of tower above ground level [onshore] or MSL [offshore] (meters)
{:7.2f}     Twr2Shft    - Vertical distance from the tower-top to the rotor shaft (meters)
{:6.1f}      TwrRBHt     - Tower rigid base height (meters)
{:6.1f}      ShftTilt    - Rotor shaft tilt angle (degrees)
{:6.1f}      Delta3      - Delta-3 angle for teetering rotors (degrees) [unused for 3 blades]
{:6.1f}      PreCone(1)  - Blade 1 cone angle (degrees)
{:6.1f}      PreCone(2)  - Blade 2 cone angle (degrees)
{:6.1f}      PreCone(3)  - Blade 3 cone angle (degrees) [unused for 2 blades]
{:6.1f}      AzimB1Up    - Azimuth value to use for I/O when blade 1 points up (degrees)
---------------------- MASS AND INERTIA ----------------------------------------
{:6.1f}      YawBrMass   - Yaw bearing mass (kg)
{:10.4e}  NacMass     - Nacelle mass (kg)
{:10.4e}  HubMass     - Hub mass (kg)
{:6.1f}      TipMass(1)  - Tip-brake mass, blade 1 (kg)
{:6.1f}      TipMass(2)  - Tip-brake mass, blade 2 (kg)
{:6.1f}      TipMass(3)  - Tip-brake mass, blade 3 (kg) [unused for 2 blades]
{:10.4g}  NacYIner    - Nacelle inertia about yaw axis (kg m^2)
{:10.3f}  GenIner     - Generator inertia about HSS (kg m^2)
{:10.3e}  HubIner     - Hub inertia about rotor axis [3 blades] or teeter axis [2 blades] (kg m^2)
---------------------- DRIVETRAIN ----------------------------------------------
{:6.1f}      GBoxEff     - Gearbox efficiency (%)
{:6.1f}      GenEff      - Generator efficiency [ignored by the Thevenin and user-defined generator models] (%)
{:8.3f}    GBRatio     - Gearbox ratio (-)
{:5s}       GBRevers    - Gearbox reversal {T: if rotor and generator rotate in opposite directions} (flag)
{:6.1f}      HSSBrTqF    - Fully deployed HSS-brake torque (N-m)
{:6.1f}      HSSBrDT     - Time for HSS-brake to reach full deployment once initiated (sec) [used only when HSSBrMode=1]
"{:s}"    DynBrkFi    - File containing a mech-gen-torque vs HSS-speed curve for a dynamic brake [CURRENTLY IGNORED] (quoted string)
{:8.1e}    DTTorSpr    - Drivetrain torsional spring (N-m/rad)
{:8.1e}    DTTorDmp    - Drivetrain torsional damper (N-m/(rad/s))
---------------------- SIMPLE INDUCTION GENERATOR ------------------------------
{:6.1f}      SIG_SlPc    - Rated generator slip percentage (%) [used only when VSContrl=0 and GenModel=1]
{:6.1f}      SIG_SySp    - Synchronous (zero-torque) generator speed (rpm) [used only when VSContrl=0 and GenModel=1]
{:6.1f}      SIG_RtTq    - Rated torque (N-m) [used only when VSContrl=0 and GenModel=1]
{:6.1f}      SIG_PORt    - Pull-out ratio (Tpullout/Trated) (-) [used only when VSContrl=0 and GenModel=1]
---------------------- THEVENIN-EQUIVALENT INDUCTION GENERATOR -----------------
{:6.1f}      TEC_Freq    - Line frequency [50 or 60] (Hz) [used only when VSContrl=0 and GenModel=2]
{:6.0f}      TEC_NPol    - Number of poles [even integer > 0] (-) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_SRes    - Stator resistance (ohms) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_RRes    - Rotor resistance (ohms) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_VLL     - Line-to-line RMS voltage (volts) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_SLR     - Stator leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_RLR     - Rotor leakage reactance (ohms) [used only when VSContrl=0 and GenModel=2]
{:6.1f}      TEC_MR      - Magnetizing reactance (ohms) [used only when VSContrl=0 and GenModel=2]
---------------------- PLATFORM ------------------------------------------------
   {:.0f}        PtfmModel   - Platform model {0: none, 1: onshore, 2: fixed bottom offshore, 3: floating offshore} (switch)
"{:s}"    PtfmFile    - Name of file containing platform properties (quoted string) [unused when PtfmModel=0]
---------------------- TOWER ---------------------------------------------------
  {:2.0f}        TwrNodes    - Number of tower nodes used for analysis (-)
"{:s}"    TwrFile - Name of file containing tower properties (quoted string)
---------------------- NACELLE-YAW ---------------------------------------------
{:6.1f}      YawSpr      - Nacelle-yaw spring constant (N-m/rad)
{:6.1f}      YawDamp     - Nacelle-yaw damping constant (N-m/(rad/s))
{:6.1f}      YawNeut     - Neutral yaw position--yaw spring force is zero at this yaw (degrees)
---------------------- FURLING -------------------------------------------------
{:5s}       Furling     - Read in additional model properties for furling turbine (flag)
"{:s}"    FurlFile    - Name of file containing furling properties (quoted string) [unused when Furling=False]
---------------------- ROTOR-TEETER --------------------------------------------
   {:1.0f}        TeetMod     - Rotor-teeter spring/damper model {0: none, 1: standard, 2: user-defined from routine UserTeet} (switch) [unused for 3 blades]
{:6.1f}      TeetDmpP    - Rotor-teeter damper position (degrees) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetDmp     - Rotor-teeter damping constant (N-m/(rad/s)) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetCDmp    - Rotor-teeter rate-independent Coulomb-damping moment (N-m) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetSStP    - Rotor-teeter soft-stop position (degrees) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetHStP    - Rotor-teeter hard-stop position (degrees) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetSSSp    - Rotor-teeter soft-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]
{:6.1f}      TeetHSSp    - Rotor-teeter hard-stop linear-spring constant (N-m/rad) [used only for 2 blades and when TeetMod=1]
---------------------- TIP-BRAKE -----------------------------------------------
{:6.1f}      TBDrConN    - Tip-brake drag constant during normal operation, Cd*Area (m^2)
{:6.1f}      TBDrConD    - Tip-brake drag constant during fully-deployed operation, Cd*Area (m^2)
{:6.1f}      TpBrDT      - Time for tip-brake to reach full deployment once released (sec)
---------------------- BLADE ---------------------------------------------------
"{:s}"    BldFile(1) - Name of file containing properties for blade 1 (quoted string)
"{:s}"    BldFile(2) - Name of file containing properties for blade 2 (quoted string)
"{:s}"    BldFile(3) - Name of file containing properties for blade 3 (quoted string) [unused for 2 blades]
---------------------- AERODYN -------------------------------------------------
"{:s}"         ADFile     - Name of file containing AeroDyn input parameters (quoted string)
---------------------- NOISE ---------------------------------------------------
"{:s}"    NoiseFile   - Name of file containing aerodynamic noise input parameters (quoted string) [used only when CompNoise=True]
---------------------- ADAMS ---------------------------------------------------
"{:s}"    ADAMSFile  - Name of file containing ADAMS-specific input parameters (quoted string) [unused when ADAMSPrep=1]
---------------------- LINEARIZATION CONTROL -----------------------------------
"{:s}"   LinFile    - Name of file containing FAST linearization parameters (quoted string) [unused when AnalMode=1]
---------------------- OUTPUT --------------------------------------------------
{:5s}       SumPrint    - Print summary data to "<RootName>.fsm" (flag)
{:1.0f}           OutFileFmt  - Format for tabular (time-marching) output file(s) (1: text file [<RootName>.out], 2: binary file [<RootName>.outb], 3: both) (switch)
{:5s}       TabDelim    - Use tab delimiters in text tabular output file? (flag)
"{:s}"  OutFmt      - Format used for text tabular output (except time).  Resulting field should be 10 characters. (quoted string)  [not checked for validity!]
{:5.1f}      TStart      - Time to begin tabular output (s)
  {:2.0f}        DecFact     - Decimation factor for tabular output {1: output every time step} (-)
{:6.1f}      SttsTime    - Amount of time between screen status messages (sec)
{:6.1f}      NcIMUxn     - Downwind distance from the tower-top to the nacelle IMU (meters)
{:6.1f}      NcIMUyn     - Lateral  distance from the tower-top to the nacelle IMU (meters)
{:6.1f}      NcIMUzn     - Vertical distance from the tower-top to the nacelle IMU (meters)
{:6.1f}      ShftGagL    - Distance from rotor apex [3 blades] or teeter pin [2 blades] to shaft strain gages [positive for upwind rotors] (meters)
   {:1.0f}        NTwGages    - Number of tower nodes that have strain gages for output [0 to 9] (-)
   {:1.0f}        TwrGagNd    - List of tower nodes that have strain gages [1 to TwrNodes] (-) [unused if NTwGages=0]
   {:1.0f}        NBlGages    - Number of blade nodes that have strain gages for output [0 to 9] (-)
   {:1.0f}        BldGagNd    - List of blade nodes that have strain gages [1 to BldNodes] (-) [unused if NBlGages=0]
            OutList     - The next line(s) contains a list of output parameters.  See OutList.xlsx for a listing of available output channels, (-)
{:s}	OutList
END of FAST input file (the word "END" must appear in the first 3 columns of this last line).
--------------------------------------------------------------------------------
