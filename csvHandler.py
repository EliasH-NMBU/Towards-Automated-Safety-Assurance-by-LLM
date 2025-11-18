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

    print(f"✅ Loaded {len(data)} rows successfully.")
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
        "Obstacle(currentPosition) (Internal, boolean): True if there is an obstacle at the rover's current position.\n"
        "speed (Input, integer): The rovers velocity, typically in km/h.\n"
        "removeGoalFromSet (Output, boolean): Command to remove a completed goal from the navigation goal list.\n"
        "atGoal (Input, boolean): Status flag that becomes true when the rover reaches its goal position.\n"
        "currentPosition (Input, integer): Current position of the rover from navigation.\n"
        "goal (Input, integer): The target position currently assigned to the rover.\n"
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
        "F (Internal, integer): Measured or displayed flow parameter.\n"
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


def save_results_to_csv(results, output_path=None):

    # Ensure directory exists
    os.makedirs("results", exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d%H%M%S")

    # Default filename
    if output_path is None:
        output_path = f"results/{date_str}_ptLTL_results.csv"

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