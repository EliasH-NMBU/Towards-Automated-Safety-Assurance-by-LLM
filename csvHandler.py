import csv
import os
from datetime import datetime

DATE = datetime.now().strftime("%Y%m%d")


def load_and_validate_csv(filepath: str):

    required_columns = ["ID", "NL description", "FRETish", "LTL"]

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}") 

    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Normalize header names (strip spaces, handle BOM)
        headers = [h.strip() for h in reader.fieldnames or []]

        # Verify all required columns
        missing = [col for col in required_columns if col not in headers]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        # Normalize data rows
        data = []
        for row in reader:
            clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}
            data.append(clean_row)

    print(f"Loaded {len(data)} rows successfully.")
    return data


def get_master_variable_table_info():

    return (
        "Variable Mapping Table:\n"
        "------------------------\n"
        "alert (Output, boolean): Mitigation to sound an alert under determined condition.\n"
        "classifier (Input, integer): Identification variable for human detected by system. 0 = None, 1 = worker, 2 = untrained person\n"
        "dgt_3 (Internal, boolean): distance greater than 3 meters.\n"
        "dgt_7 (Internal, boolean): distance greater than 7 meters.\n"
        "distance_to_target (Input, integer): Distance to identified human in meters.\n"
        "halt (Output, boolean): Mitigation to stop the robot.\n"
        "OpState (Output, integer): Current active mitigation state. From 0 to 3\n"
        "slowdown (Output, boolean): Mitigation to slow down the robot.\n"
        "turnoffUVC (Output, boolean): Mitigation to turn off UV lights.\n"
    )


def get_rover_variable_table_info():

    return (
        "Variable Mapping Table:\n"
        "------------------------\n"
        "chargePosition (Internal, integer): Encodes the coordinate or ID of the fixed charging station location.\n"
        "recharge (Internal, boolean): Flag indicating that the rover needs to recharge its battery.\n"
        "goal (Internal, integer): Identifier or coordinate of the rovers current navigation target.\n"
        "pre_battery (Internal, integer): Previous timesteps battery value, used for energy consumption calculations.\n"
        "n (Internal, integer): Normalization factor or total number of plan steps used in energy calculation.\n"
        "plan (Internal, integer): Represents the active route or sequence of waypoints being executed by the rover.\n"
        "length_plan (Internal, integer): The total number of steps or waypoints in the current navigation plan.\n"
        "chargeNeeded_var (Internal, integer): Estimated amount of charge required to reach the charging station.\n"
        "batteryFull (Internal, boolean): Indicates that the rovers battery has reached full charge capacity.\n"
        "atGoal (Internal, boolean): True if the rover has arrived at its current goal location.\n"
        "currentPosition (Input, integer): The rovers current logical position according to navigation data.\n"
        "initialPosition (Input, integer): The initial or starting position of the rover when the mission begins.\n"
        "currentPhysicalPosition (Input, integer): The physical location reported by sensors (used to check accuracy).\n"
        "start (Internal, integer): Initial map or system state in the vision/map validation process.\n"
        "s0 (Constant, integer): Static reference position used to validate the starting state.\n"
        "x (Internal, integer): Static Charging station location\n"
        "y (Internal, integer): Static Initial rover position\n"
        "obstacle (Input, integer): Position identifier of an obstacle detected by the vision subsystem.\n"
        "Obstacle_currentPosition (Internal, boolean): True if there is an obstacle at the rover's current position.\n"
        "speed (Input, integer): The rovers velocity, typically in km/h.\n"
        "removeGoalFromSet (Output, boolean): Command to remove a completed goal from the navigation goal list.\n"
        "atGoal (Input, boolean): Status flag that becomes true when the rover reaches its goal position.\n"
        "currentPosition (Input, integer): Current position of the rover from navigation.\n"
        "goal (Input, integer): The target position currently assigned to the rover.\n"
    )

def get_drone_variable_table_info():

    return (
        "Variable Mapping Table:\n"
        "------------------------\n"

        # Simulation & execution modes
        "SimulationMode (Internal, boolean): Indicates whether the system is operating in simulation mode.\n"
        "SimulationModeRaspberry (Internal, boolean): Indicates simulation mode is active on the Raspberry Pi.\n"
        "HILSimulationGazebo (Internal, boolean): True when hardware-in-the-loop simulation using Gazebo is active.\n"
        "AutonomousFlightMode (Internal, boolean): Indicates the drone is operating in autonomous flight mode.\n"
        "RemoteControlFlightMode (Internal, boolean): Indicates the drone is being operated via remote control.\n"
        "FailsafeFlightMode (Internal, boolean): Indicates the system has entered a failsafe flight mode.\n"
        "RealMode (Internal, boolean): Indicates that the system is operating in real (non-simulated) mode.\n"
        "HILSimulation (Internal, boolean): Indicates that hardware-in-the-loop simulation is active.\n"

        # Simulation control & communication
        "SimulateCommunications (Internal, boolean): Enables simulated communication between system components.\n"
        "SimulatePackageSending (Internal, boolean): Enables simulation of package/message transmission.\n"
        "SimulateFailureTransition (Internal, boolean): Triggers simulated failure state transitions.\n"
        "SimulatePacketLoss (Internal, boolean): Enables simulation of packet loss in communications.\n"
        "SimulationLoopStart (Event, boolean): Becomes true when a simulation loop begins.\n"
        "SimulationLoopFinish (Event, boolean): Becomes true when a simulation loop completes.\n"
        "SimulationDataSaved (Internal, boolean): Indicates that simulation data has been successfully stored.\n"

        # Failure detection & fault handling
        "JetsonFailureDetectionRunning (Internal, boolean): Indicates that Jetson-based failure detection is active.\n"
        "JetsonFailureTransitionToNucleo (Internal, boolean): Indicates a failure-triggered control transition from Jetson to Nucleo.\n"
        "RaspberryFailureDetectionRunning (Internal, boolean): Indicates failure detection is running on the Raspberry Pi.\n"
        "ActiveNucleoFailureDetectionRunning (Internal, boolean): Indicates failure detection is active on the currently active Nucleo.\n"
        "NucleoFailureSwitchActiveNucleo (Internal, boolean): Indicates failure-triggered switching between Nucleo controllers.\n"
        "ActiveNucleo (Internal, boolean): Indicates which Nucleo controller is currently active.\n"
        "NucleoOnline (Internal, boolean): Indicates the Nucleo controller is online and responsive.\n"

        # Control authority & messaging
        "JetsonControl (Internal, boolean): Indicates that control authority is held by the Jetson.\n"
        "JetsonControlDisplay (Internal, boolean): Indicates Jetson control status is being displayed.\n"
        "NucleoOneControl (Internal, boolean): Indicates that Nucleo One currently has control authority.\n"
        "SendNucleoOneControlMessage (Output, boolean): Command to send a control message to Nucleo One.\n"
        "NucleoTwoControl (Internal, boolean): Indicates that Nucleo Two currently has control authority.\n"
        "SendNucleoTwoControlMessage (Output, boolean): Command to send a control message to Nucleo Two.\n"
        "NulceoControl (Internal, boolean): Indicates that control authority is held by a Nucleo controller.\n"
        "NucleoControlDisplay (Internal, boolean): Indicates Nucleo control status is being displayed.\n"
        "NucleoControl (Internal, boolean): Indicates that a Nucleo controller has control authority.\n"
        "DisplayCurrentController (Internal, boolean): Indicates which controller is currently in control is being displayed.\n"
        "SendBatteryDischargeRateData (Output, boolean): Command to transmit battery discharge rate information.\n"
        "MonitorBatteryDischargeRate (Internal, boolean): Enables monitoring of the battery discharge rate.\n"
        "MonitorAngularVelocity (Internal, boolean): Enables monitoring of angular velocity data.\n"
        "SendAngularVelocityData (Output, boolean): Command to send angular velocity data.\n"
        "NucleoOneFailureDetectionRunning (Internal, boolean): Indicates that failure detection is active on Nucleo One.\n"
        "true (Internal, boolean): Constant variable always set to true for logical operations.\n"
        "false (Internal, boolean): Constant variable always set to false for logical operations.\n"

        # Control loop & algorithm execution
        "ControlLoopStart (Event, boolean): Indicates the start of a control loop execution.\n"
        "ControlLoopFinish (Event, boolean): Indicates the completion of a control loop execution.\n"
        "ControlLoopStartRaspberry (Event, boolean): Indicates the control loop has started on the Raspberry Pi.\n"
        "ControlLoopStartNucleo (Event, boolean): Indicates the control loop has started on the Nucleo controller.\n"
        "ControlAlgorithmStart (Event, boolean): Indicates the control algorithm has started execution.\n"
        "ControlAlgorithmFinish (Event, boolean): Indicates the control algorithm has finished execution.\n"
        "EvaluateControllerPerformance (Internal, boolean): Indicates controller performance evaluation is active.\n"
        "MeasureControlTransition (Internal, boolean): Indicates measurement of control handover transitions.\n"
        "CollectHardwareExecutionTimes (Internal, boolean): Enables collection of hardware execution timing data.\n"
        "AssessHardwareTimePerformance (Internal, boolean): Indicates assessment of hardware timing performance.\n"

        # Communication quality & packet loss
        "MonitorCommunicationQuality (Internal, boolean): Enables monitoring of communication quality.\n"
        "PacketLossRate (Internal, integer): Encoded packet loss rate percentage.\n"
        "AcceptablePacketLoss (Internal, integer): Maximum acceptable packet loss percentage threshold.\n"

        # Power & energy management
        "MonitorPowerConsumption (Internal, boolean): Enables monitoring of power consumption.\n"
        "ReturnPowerConsumptionData (Output, boolean): Command to transmit power consumption data.\n"
        "ManageEnergySources (Internal, boolean): Indicates active management of onboard energy sources.\n"
        "MonitorBatteryStatus (Internal, boolean): Enables monitoring of battery health status.\n"
        "SendBatteryStatusData (Output, boolean): Command to send battery status data.\n"
        "MonitorBatteryLevel (Internal, boolean): Enables monitoring of battery charge level.\n"
        "SendBatteryLevelData (Output, boolean): Command to send battery level data.\n"
        "MonitorBatteryVoltage (Internal, boolean): Enables monitoring of battery voltage.\n"
        "SendBatteryVoltageData (Output, boolean): Command to send battery voltage data.\n"
        "MonitorVoltageBusConsumption (Internal, boolean): Enables monitoring of voltage bus consumption.\n"
        "SendVoltageBusConsumptionData (Output, boolean): Command to send voltage bus consumption data.\n"
        "NucleoTwoFailureDetectionRunning (Internal, boolean): Indicates that failure detection is active on Nucleo Two.\n"

        # System & health monitoring
        "OverallSystemHealthMonitoring (Internal, boolean): Enables overall system health monitoring.\n"
        "ElectricSystemsHealthMonitoring (Internal, boolean): Enables monitoring of electrical system health.\n"
        "ServoMonitoring (Internal, boolean): Enables servo subsystem monitoring.\n"
        "BatteryMonitoring (Internal, boolean): Enables battery monitoring subsystem.\n"
        "UseRealTimeClock (Internal, boolean): Indicates use of a real-time clock for timing measurements.\n"
        "MonitoringEnabled (Internal, boolean): Global enable flag for monitoring functionality.\n"
        "MonitoringEnabledRaspberry (Internal, boolean): Enables monitoring on the Raspberry Pi.\n"

        # Sensor monitoring & data transmission
        "MonitorGroundSpeed (Internal, boolean): Enables monitoring of ground speed.\n"
        "SendGroundSpeedData (Output, boolean): Command to send ground speed data.\n"
        "MonitorWindSpeed (Internal, boolean): Enables monitoring of wind speed.\n"
        "SendWindSpeedData (Output, boolean): Command to send wind speed data.\n"
        "MonitorPitotTube (Internal, boolean): Enables monitoring of pitot tube sensor.\n"
        "SendPitotTubeData (Output, boolean): Command to send pitot tube data.\n"
        "MonitorAlphaVane (Internal, boolean): Enables monitoring of angle-of-attack vane.\n"
        "SendAlphaVaneData (Output, boolean): Command to send alpha vane data.\n"
        "MonitorBetaVane (Internal, boolean): Enables monitoring of sideslip vane.\n"
        "SendBetaVaneData (Output, boolean): Command to send beta vane data.\n"
        "MonitorServoMotors (Internal, boolean): Enables monitoring of servo motors.\n"
        "SendServoMotorsData (Output, boolean): Command to send servo motor data.\n"
        "MonitorTiltAngles (Internal, boolean): Enables monitoring of tilt angles.\n"
        "SendTiltAngleData (Output, boolean): Command to send tilt angle data.\n"
        "MonitorAccelerations (Internal, boolean): Enables monitoring of acceleration data.\n"
        "SendAccelerationsData (Output, boolean): Command to send acceleration data.\n"
        "MonitorBarometerAltitude (Internal, boolean): Enables monitoring of barometric altitude.\n"
        "SendBarometerAltitudeData (Output, boolean): Command to send barometric altitude data.\n"
        "MonitorRow (Internal, boolean): Enables monitoring of roll angle.\n"
        "SendRowData (Output, boolean): Command to send roll data.\n"
        "MonitorPitch (Internal, boolean): Enables monitoring of pitch angle.\n"
        "SendPitchData (Output, boolean): Command to send pitch data.\n"
        "MonitorYaw (Internal, boolean): Enables monitoring of yaw angle.\n"
        "SendYawData (Output, boolean): Command to send yaw data.\n"

        # IMU & navigation sensors
        "MonitorAccelerometerData (Internal, boolean): Enables monitoring of accelerometer data.\n"
        "SendAccelerometerData (Output, boolean): Command to send accelerometer data.\n"
        "MonitorGyroscopeData (Internal, boolean): Enables monitoring of gyroscope data.\n"
        "SendGyroscopeData (Output, boolean): Command to send gyroscope data.\n"
        "MonitorMagnetometerData (Internal, boolean): Enables monitoring of magnetometer data.\n"
        "SendMagnetometerData (Output, boolean): Command to send magnetometer data.\n"
        "MonitorCompassData (Internal, boolean): Enables monitoring of compass data.\n"
        "SendCompassData (Output, boolean): Command to send compass data.\n"

        # GPS & positioning
        "MonitorGPSLatitude (Internal, boolean): Enables monitoring of GPS latitude.\n"
        "MonitorGPSLongitude (Internal, boolean): Enables monitoring of GPS longitude.\n"
        "MonitorGPSAltitude (Internal, boolean): Enables monitoring of GPS altitude.\n"
        "MonitorGPSHomePosition (Internal, boolean): Enables monitoring of GPS home position.\n"
        "SendGPSData (Output, boolean): Command to send GPS data.\n"
        "SatelliteShadowing (Internal, boolean): Indicates satellite signal shadowing conditions.\n"
        "NoReceptionLoS (Internal, boolean): Indicates loss of line-of-sight satellite reception.\n"
        "SignalDiffraction (Internal, boolean): Indicates signal diffraction effects.\n"
        "MultipathEffects (Internal, boolean): Indicates multipath signal interference.\n"
        "PositioningAccuracy (Internal, boolean): Indicates acceptable positioning accuracy.\n"
        "MonitorRTKData (Internal, boolean): Enables monitoring of RTK correction data.\n"
        "SendRTKData (Output, boolean): Command to send RTK data.\n"

        # Mechanical & thermal monitoring
        "MonitorMotorRPM (Internal, boolean): Enables monitoring of motor RPM.\n"
        "SendMotorRPM (Output, boolean): Command to send motor RPM data.\n"
        "MonitorPropellerRPM (Internal, boolean): Enables monitoring of propeller RPM.\n"
        "SendPropellerRPMData (Output, boolean): Command to send propeller RPM data.\n"
        "MonitorComponentsTemeratures (Internal, boolean): Enables monitoring of component temperatures.\n"
        "SendComponentsTemperaturesData (Output, boolean): Command to send component temperature data.\n"
        "MonitorInternalTemperature (Internal, boolean): Enables monitoring of internal temperature.\n"
        "SendInternalTemperatureData (Output, boolean): Command to send internal temperature data.\n"
        "MonitorBayAreaTemperature (Internal, boolean): Enables monitoring of bay area temperature.\n"
        "SendBayAreaTemperatureData (Output, boolean): Command to send bay area temperature data.\n"

        # Electrical current monitoring
        "MonitorBrushlessCurrent (Internal, boolean): Enables monitoring of brushless motor current.\n"
        "MonitorESCCurrent (Internal, boolean): Enables monitoring of ESC current.\n"
        "MonitorServoMotorCurrent (Internal, boolean): Enables monitoring of servo motor current.\n"
    )



def get_abzrover_variable_table_info():

    return (
        "Variable Mapping Table:\n"
        "------------------------\n"
        "currentPosition (Input, coordinate): Rover's current estimated (x,y) position from Vision.\n"
        "obstacles (Input, set of coordinates): Positions of obstacles identified by Vision.\n"
        "GSObstacles (Input, set of coordinates): Obstacles sent from the ground station.\n"
        "prioritisedGoals (Input, ordered list of coordinates): Sorted mission goals from the ground station.\n"
        "chargers (Input, list of coordinates): Locations of charging stations.\n"
        "invalidMap (Output, boolean): Flag sent to ground when MapValidator detects inconsistent map data.\n"
        "goal (Internal, coordinate): The currently selected navigation target from the GRA.\n"
        "safeLocation (Input, coordinate): A fallback location the ground station can command the rover to navigate to.\n"
        "recharge (Internal, boolean): Flag indicating the rover must charge before proceeding.\n"
        "atGoal (Internal, boolean): True when rover physically reaches the current goal.\n"
        "systemState (Internal, structured record): Snapshot of planner, hardware, and sensor states sent to FailureMode.\n"
        "noplan (Output, boolean): Value returned by a planner when no valid route exists.\n"
        "plan2C (Internal/Output, list of coordinates): Final plan selected by ComputePlan2Charging.\n"
        "plan2D (Internal/Output, list of coordinates): Final plan selected by ComputePlan2Destination.\n"
        "plans (Internal, list of lists): All candidate paths generated by a planner.\n"
        "batteryLevel (Internal, integer): Current battery charge as measured by BatteryMonitor.\n"
        "measuredBattery (Internal, integer): Raw battery reading before 5 percentage deduction.\n"
        "recharge flag (Internal, boolean): Flag set by HI1 indicating insufficient battery to complete mission.\n"
        "movementCommands (Output, actuator instruction): Low-level drive command sent to the hardware.\n"
        "velocityCommands (Output, actuator instruction): Low-level velocity control signals.\n"
        "solarPanelsOpen (Internal, boolean): Indicates whether the solar panels are deployed.\n"
        "communicationData (Input/Output, structured message): Messages exchanged with the ground station.\n"
        "completed (Output, boolean): Mission-completed message sent to ground station.\n"
        "noMoreViablePlans (Output, boolean): Planner failure message sent via Communication2Ground.\n"
        "failed2Reconnect (Internal/Output, boolean): Flag set when 3 consecutive reconnection attempts fail.\n"
        "helperId (Output, integer): ID of assisting rover broadcast in Communication2Rovers.\n"
        "location (Input, coordinate): Position broadcasts sent between rovers.\n"
        "failure (Input, boolean): Broadcast notification indicating another rover is in failure mode.\n"
        "failureCause (Internal, symbolic): Diagnosis result produced by FailureReasoningAgent.\n"
        "reboot (Output, boolean): Recovery instruction triggered by FailureMode.\n"
        "requestHelp (Output, boolean): Recovery instruction requesting assistance from ground or nearby rovers.\n"
        "waitForHelpTimer (Internal, integer): Timeout counter used when waiting for remote assistance.\n"
        "planTimeout (Internal, boolean): Flag raised when planner takes too long (planning failure).\n"
        "connectionStatus (Internal, enum): Status of point-to-point communication link to ground.\n"
        "responseData (Input, message): Data received from ground after communication wait.\n"
        "obstacleAccuracy (Internal, float): Vision system accuracy metric (>95%).\n"
        "perturbationInput (Input, sensor data): Slightly altered sensor values for robustness testing.\n"
        "batteryNeededToGoal (Internal, integer): Estimated energy needed to reach current goal.\n"
        "batteryNeededToCharger (Internal, integer): Estimated energy needed to reach nearest charger.\n"
    )


def get_pipeline_variable_table_info():
# variable_1, input integer variable_2, integer variable_3, bool variable_4, bool variable_5, integer constant variable_6, internal integer
    return (
        "Variable Mapping Table:\n"
        "------------------------\n"
        "variable_1 (Input, integer)\n"
        "variable_2 (Input, integer)\n"
        "variable_3 (Input, boolean)\n"
        "variable_4 (Input, boolean)\n"
        "variable_5 (Constant, integer)\n"
        "variable_6 (Internal, integer)\n"

    )


def get_lung_ventilator_variable_table_info():

    return (
        "Variable Mapping Table:\n"
        "------------------------\n"
        "ADCConnFailure (Internal, boolean): Indicates that the ADC communication link has failed.\n"
        "ADCError (Internal, integer): Error code from the ADC system.\n"
        "ADCRetries (Internal, integer): Number of retries made to reconnect the ADC.\n"
        "BreathingCycleStart (Internal, boolean): Marks the start of a breathing cycle.\n"
        "CONT (Internal, boolean): Generic control continuation flag used in cycle timing.\n"
        "ExpiratoryPhaseEnd (Internal, boolean): True when the expiratory phase finishes.\n"
        "ExpiratoryTime (Internal, integer): Duration of the expiration phase in ms.\n"
        "ExpiratoryTriggerSensitivity (Input, integer): Flow threshold for triggering expiration.\n"
        "Fail (Internal, boolean): Generic fault or error indicator.\n"
        "FailSafeMode (Internal, boolean): System safety fallback mode active.\n"
        "FinalState (Internal, integer): Recorded last state of ventilator before reset or shutdown.\n"
        "GBPS (Internal, integer): Communication throughput for diagnostic data.\n"
        "GUIConnected (Input, boolean): True if GUI is connected to the controller.\n"
        "GUIFailure (Internal, boolean): Indicates a communication fault with the GUI.\n"
        "GUIResumeRequest (Input, boolean): GUI command to resume ventilation.\n"
        "ITS_PCV (Internal, boolean): Inspiratory Trigger Sensitivity for PCV mode enabled.\n"
        "ITS_PSV (Internal, boolean): Inspiratory Trigger Sensitivity for PSV mode enabled.\n"
        "IToE (Internal, integer): Ratio or timing of inspiration to expiration.\n"
        "IToE_AP (Internal, integer): I:E ratio in apnea mode.\n"
        "InhaleTriggerSensitivityPCV (Input, integer): Patient-trigger sensitivity in PCV mode.\n"
        "InhaleTriggerSensitivityPSV (Input, integer): Patient-trigger sensitivity in PSV mode.\n"
        "ItoE (Internal, integer): Same as IToE, used for compatibility naming.\n"
        "ItoE_AP (Internal, integer): Apnea-specific inspiration-expiration ratio.\n"
        "ItoE_PCV (Internal, integer): I:E ratio for PCV mode.\n"
        "MaxP_insp (Input, integer): Maximum inspiratory pressure setting.\n"
        "MinPEEPAtmAnalyzer (Input, integer): Minimum PEEP setting allowed by analyzer.\n"
        "OutOfServiceWarning (Output, boolean): Indicates ventilator is out of service.\n"
        "PCVInspTimeEnd (Internal, boolean): Marks the end of PCV inspiration time.\n"
        "PCVMode (Input, boolean): Pressure-controlled ventilation mode active.\n"
        "PCVModeSelected (Input, boolean): Indicates PCV mode has been selected by user.\n"
        "PSVMode (Input, boolean): Pressure-support ventilation mode active.\n"
        "PSVModeSelected (Input, boolean): Indicates PSV mode has been selected.\n"
        "P_insp (Input, integer): Target inspiratory pressure.\n"
        "P_inspAP (Input, integer): Apnea pressure setting.\n"
        "P_inspPCV (Input, integer): PCV mode target pressure.\n"
        "P_inspPSV (Input, integer): PSV mode target pressure.\n"
        "Pass (Internal, boolean): Indicates that a self-test or check has passed.\n"
        "PeakV_E (Internal, integer): Peak expiratory flow or volume.\n"
        "RM (Internal, boolean): Recruitment maneuver active.\n"
        "RMButton (Input, boolean): User button to start recruitment maneuver.\n"
        "RR (Input, integer): Respiratory rate setting.\n"
        "RR_AP (Internal, integer): Respiratory rate in apnea mode.\n"
        "RR_PCV (Internal, integer): Respiratory rate in PCV mode.\n"
        "Seconds (Internal, integer): Time counter in seconds.\n"
        "SelfTestFail (Internal, boolean): Indicates self-test procedure failed.\n"
        "SelfTestMode (Internal, boolean): True when self-test procedure is running.\n"
        "SensorUse (Internal, boolean): Indicates sensors are currently being read.\n"
        "Skip (Internal, boolean): Skips current test or step.\n"
        "StandbyMode (Internal, boolean): System in standby.\n"
        "StartUpDone (Internal, boolean): Startup procedure finished successfully.\n"
        "StartUpMode (Internal, boolean): System running startup initialization.\n"
        "V_E (Internal, integer): Minute ventilation volume.\n"
        "_PRC_ (Internal, boolean): Internal process flag.\n"
        "airSupplyConnected (Input, boolean): True when air supply is detected and available.\n"
        "alarmSettingsChanged (Internal, boolean): Indicates alarm thresholds were changed.\n"
        "apnea (Internal, boolean): Indicates no spontaneous breathing detected.\n"
        "apneaAlarm (Output, boolean): Alarm triggered due to apnea.\n"
        "apneaLagTime (Internal, integer): Time delay before apnea alarm activates.\n"
        "breathingCircuitConnected (Input, boolean): True when breathing circuit is attached.\n"
        "breathingCycleDone (Internal, boolean): True when a breathing cycle completes.\n"
        "breathingCycleStart (Internal, boolean): Indicates start of a breathing cycle.\n"
        "breathingCycleTime (Internal, integer): Duration of current breathing cycle.\n"
        "breathingTime (Internal, integer): Time between breath start and end.\n"
        "breathingTimerReset (Internal, boolean): Timer reset flag between breaths.\n"
        "buttonUnPressOr (Internal, boolean): Intermediate flag for button release detection.\n"
        "checkCommsGUI (Internal, boolean): Communication test flag for GUI.\n"
        "checkCommsSensors (Internal, boolean): Communication test flag for sensors.\n"
        "checkCommsValves (Internal, boolean): Communication test flag for valves.\n"
        "confirmPSVParameters (Input, boolean): User confirmation for PSV parameter changes.\n"
        "defaultParamsLoaded (Internal, boolean): True if default parameters were loaded.\n"
        "disableLeakCompensation (Internal, boolean): Disables automatic leak compensation.\n"
        "displayF (Output, integer): Flow rate displayed on GUI.\n"
        "displayO (Output, integer): Oxygen percentage displayed.\n"
        "displayRR (Output, integer): Respiratory rate displayed.\n"
        "displayTV (Output, integer): Tidal volume displayed.\n"
        "dropPAW (Internal, boolean): Drop detected in airway pressure.\n"
        "enableLeakCompensation (Internal, boolean): Enables leak compensation function.\n"
        "enterAlarmThresholds (Internal, boolean): Operator entering alarm thresholds.\n"
        "eraseLog (Internal, boolean): Command to erase stored logs.\n"
        "error (Internal, boolean): General error flag.\n"
        "expClock (Internal, integer): Expiration phase clock counter.\n"
        "expirationPhaseEnd (Internal, boolean): Marks the end of expiration phase.\n"
        "expirationPhaseStart (Internal, boolean): Marks the start of expiration phase.\n"
        "expiratoryPause (Internal, boolean): True if expiratory pause is active.\n"
        "expiratoryPauseButton (Input, boolean): User button for expiratory pause.\n"
        "expiratoryPhase (Internal, boolean): Indicates system in expiratory phase.\n"
        "expiratoryPhaseEnd (Internal, boolean): Duplicate marker for end of expiration.\n"
        "expiratoryState (Internal, boolean): Flag for ventilator in expiration state.\n"
        "gasSupplyFailure (Internal, boolean): Indicates gas supply loss.\n"
        "highPriorityAlarm (Output, boolean): High-priority alarm indicator.\n"
        "inValveClose (Output, boolean): Closes inspiratory valve.\n"
        "inValveOpen (Output, boolean): Opens inspiratory valve.\n"
        "initDone (Internal, boolean): Initialization completed.\n"
        "initFail (Internal, boolean): Initialization failed.\n"
        "initStart (Internal, boolean): Initialization started.\n"
        "inspClock (Internal, integer): Inspiration phase clock counter.\n"
        "inspiratoryPause (Internal, boolean): True when inspiratory pause active.\n"
        "inspiratoryPauseButton (Input, boolean): User button for inspiratory pause.\n"
        "inspiratoryPhase (Internal, boolean): Indicates ventilator is in inspiration.\n"
        "inspiratoryPhaseEnd (Internal, boolean): Marks the end of inspiration.\n"
        "inspiratoryPhaseStart (Internal, boolean): Marks the start of inspiration.\n"
        "inspiratoryPressure (Internal, integer): Airway pressure during inspiration.\n"
        "inspiratoryTime (Internal, integer): Duration of inspiration phase.\n"
        "leakCompensation (Internal, boolean): Leak compensation active.\n"
        "leakCompensationActive (Internal, boolean): Indicates leak compensation loop running.\n"
        "leakCompensationEnable (Internal, boolean): Enables leak compensation algorithm.\n"
        "loadLastParams (Internal, boolean): Loads last saved configuration.\n"
        "loadLog (Internal, boolean): Loads data from log memory.\n"
        "logAlarmParams (Internal, boolean): Logs alarm parameters.\n"
        "logAlarmSettings (Internal, boolean): Logs alarm threshold changes.\n"
        "logCalibrationParams (Internal, boolean): Logs calibration parameters.\n"
        "logO (Internal, boolean): Logs oxygen readings.\n"
        "logParams (Internal, boolean): Logs all active ventilator parameters.\n"
        "logPatientChange (Internal, boolean): Logs patient connection/disconnection.\n"
        "logPowerSupply (Internal, boolean): Logs power supply events.\n"
        "logPreUseCheck (Internal, boolean): Logs pre-use check results.\n"
        "logVentilationParams (Internal, boolean): Logs core ventilation settings.\n"
        "logVentilatorSettings (Internal, boolean): Logs ventilator configuration changes.\n"
        "measureF (Internal, integer): Measured flow.\n"
        "measureO (Internal, integer): Measured oxygen percentage.\n"
        "measurePSins (Internal, integer): Measured pressure support inspiration.\n"
        "measureRR (Internal, integer): Measured respiratory rate.\n"
        "measureTV (Internal, integer): Measured tidal volume.\n"
        "minExpiratoryTime (Internal, integer): Minimum expiration time limit.\n"
        "monitorInhaleTrigger (Internal, boolean): Monitors patient inspiratory effort trigger.\n"
        "newPatient (Internal, boolean): Indicates a new patient profile loaded.\n"
        "off (Internal, boolean): True when ventilator is powered down.\n"
        "operator (Input, boolean): Represents the human operator interaction.\n"
        "outValveClose (Output, boolean): Closes expiratory valve.\n"
        "outValveOpen (Output, boolean): Opens expiratory valve.\n"
        "paramAlarm_V (Internal, integer): Alarm threshold for variable V.\n"
        "paramMax_V (Internal, integer): Maximum limit for parameter V.\n"
        "paramMin_V (Internal, integer): Minimum limit for parameter V.\n"
        "param_V (Internal, integer): Current value of parameter V.\n"
        "parametersStored (Internal, boolean): True if parameters have been saved.\n"
        "patientAttributesEntered (Input, boolean): Indicates that patient data is entered.\n"
        "patientBreathTrigger (Internal, boolean): Detected patient breath effort.\n"
        "patientBreathingRequest (Internal, boolean): Detected spontaneous breathing request.\n"
        "patientChanged (Internal, boolean): Patient connection data changed.\n"
        "patientConnected (Input, boolean): Indicates patient presence on circuit.\n"
        "patientSafe (Internal, boolean): True when all safety limits are within normal.\n"
        "powerButton (Input, boolean): Hardware power on/off switch.\n"
        "powerConnected (Internal, boolean): Indicates power source connection.\n"
        "powerFailure (Internal, boolean): Power failure detected.\n"
        "powerOff (Internal, boolean): System is turned off.\n"
        "powerSupplyChanged (Internal, boolean): Power source state changed.\n"
        "preUseCheckDone (Internal, boolean): Pre-use self-test completed.\n"
        "pressureSensorConnFailure (Internal, boolean): Pressure sensor communication failure.\n"
        "pressureSensorError (Internal, boolean): Pressure sensor malfunction.\n"
        "pressureSensorRetries (Internal, integer): Retry count for pressure sensor reconnection.\n"
        "resumeVentilation (Input, boolean): User input to resume ventilation.\n"
        "runSelfTest (Input, boolean): Command to start self-test procedure.\n"
        "saveLog (Internal, boolean): Command to save log data.\n"
        "selfTestFailed (Internal, boolean): Self-test did not pass.\n"
        "selfTestPassed (Internal, boolean): Self-test successfully passed.\n"
        "startMonitoring (Internal, boolean): Activates monitoring mode.\n"
        "startPCV (Input, boolean): User input to start PCV mode.\n"
        "startPSV (Input, boolean): User input to start PSV mode.\n"
        "startReportingHealthParams (Internal, boolean): Begins transmission of health data.\n"
        "stopVentilation (Input, boolean): User command to stop ventilation.\n"
        "testAlarmsFail (Internal, boolean): Alarm test failed.\n"
        "testAlarmsPass (Internal, boolean): Alarm test passed.\n"
        "testAlarmsSkip (Internal, boolean): Alarm test skipped.\n"
        "testFL (Internal, boolean): Test flow sensor.\n"
        "testLeaksFail (Internal, boolean): Leak test failed.\n"
        "testLeaksPass (Internal, boolean): Leak test passed.\n"
        "testLeaksSkip (Internal, boolean): Leak test skipped.\n"
        "testOxygenSensorFail (Internal, boolean): Oxygen sensor test failed.\n"
        "testOxygenSensorPass (Internal, boolean): Oxygen sensor test passed.\n"
        "testOxygenSensorSkip (Internal, boolean): Oxygen sensor test skipped.\n"
        "testPSExpFail (Internal, boolean): Pressure support expiration test failed.\n"
        "testPSExpPass (Internal, boolean): Pressure support expiration test passed.\n"
        "testPSExpSkip (Internal, boolean): Pressure support expiration test skipped.\n"
        "testPowerSwitchFail (Internal, boolean): Power switch test failed.\n"
        "testPowerSwitchPass (Internal, boolean): Power switch test passed.\n"
        "testPowerSwitchSkip (Internal, boolean): Power switch test skipped.\n"
        "user (Input, boolean): Represents the human operator presence.\n"
        "ventilating (Internal, boolean): True when system is currently ventilating.\n"
        "ventilationOff (Internal, boolean): Indicates ventilation has stopped.\n"
        "ventilationParamsAdjustable (Internal, boolean): True when parameters can be modified.\n"
        "ventilatorSettingsChanged (Internal, boolean): Indicates ventilator configuration has changed.\n"
    )


def save_results_to_csv(results, output_path=None, temperature="0"):

    # Ensure directory exists
    os.makedirs("results", exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d%H%M%S")

    # Default filename
    if output_path is None and temperature == "0":
        output_path = f"results/{date_str}_ptLTL_results.csv"

    if output_path is None and temperature != "0":
        output_path = f"results/{date_str}_ptLTL_results_{temperature}.csv"

    fieldnames = ["Summary", "ID", "ptLTL", "Generated ptLTL", "Equivalence Check"]

    with open(output_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Results saved to {output_path}")


if __name__ == "__main__":
    # Test the function
    filepath = "masterFiles/masterUseCaseReq.csv"  # Replace with your CSV file path
    try:
        data = load_and_validate_csv(filepath)
        for entry in data:
            print(entry)

        print("Test data acquasition: ", data[0]["NL description"])  # Example access
    except Exception as e:
        print(f"Error: {e}")