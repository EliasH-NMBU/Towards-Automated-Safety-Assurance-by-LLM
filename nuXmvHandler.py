import subprocess
import tempfile
import os


def check_equivalence_master(formula1, formula2):
    
    
    def normalize(f):
        return (f.replace("∧", "&")
                .replace("∨", "|")
                .replace("¬", "!")
                .replace("→", "->")
                .replace("≥", ">=")
                .replace("≤", "<=")
                .replace("=", "=")
                .replace("≠", "!=")
                )

    f1 = normalize(formula1)
    f2 = normalize(formula2)


    model = f"""
    MODULE main
    VAR
    alert : boolean;
    classifier : {{0, 1, 2}};
    dgt_3 : boolean;
    dgt_7 : boolean;
    distance_to_target : 0..10;
    halt : boolean;
    OpState : {{0, 1, 2, 3}};
    slowdown : boolean;
    turnoffUVC : boolean;

    LTLSPEC ({f1}) <-> ({f2})
    """

    with tempfile.NamedTemporaryFile(suffix=".smv", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(model)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["nuxmv.exe", tmp_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        #re.search(r"is\s+(true|false)", result_text, re.I)

        if "is true" in output:
            return True
        elif "is false" in output:
            return False
        else:
            print("⚠️ Unexpected NuXMV output format")
            return False
        
    finally:
        os.remove(tmp_path)


def check_equivalence_rover(formula1, formula2):
    
    
    def normalize(f):
        return (f.replace("∧", "&")
                .replace("∨", "|")
                .replace("¬", "!")
                .replace("→", "->")
                .replace("≥", ">=")
                .replace("≤", "<=")
                .replace("=", "=")
                .replace("≠", "!=")
                )

    f1 = normalize(formula1)
    f2 = normalize(formula2)


    model = f"""
    MODULE main
    VAR
    battery : 0..100;
    chargePosition : 0..100;
    recharge : boolean;
    goal : 0..100;
    pre_battery : 0..100;
    n : 0..100;
    plan : 0..100;
    chargeNeeded_var : 0..100;
    length_plan : 0..100;
    batteryFull : boolean;
    atGoal : boolean;
    Obstacle : boolean;
    currentPosition : 0..100;
    initialPosition : 0..100;
    currentPhysicalPosition : 0..100;
    start : 0..100;
    s0 : 0..100;
    obstacle : 0..100;
    speed : 0..100;
    removeGoalFromSet : boolean;

    LTLSPEC ({f1}) <-> ({f2})
    """

    with tempfile.NamedTemporaryFile(suffix=".smv", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(model)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["nuxmv.exe", tmp_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        error_output = result.stderr

        if "is true" in output:
            return True
        elif "is false" in output:
            return False
        else:
            print("⚠️ Unexpected NuXMV output format")
            print("---- STDOUT ----")
            print(output)
            print("---- STDERR ----")
            print(error_output)
            print("----------------")
            return False

        
    finally:
        os.remove(tmp_path)


def check_equivalence_lungV(formula1, formula2):
    
    
    def normalize(f):
        return (f.replace("∧", "&")
                .replace("∨", "|")
                .replace("¬", "!")
                .replace("→", "->")
                .replace("≥", ">=")
                .replace("≤", "<=")
                .replace("=", "=")
                .replace("≠", "!=")
                )

    f1 = normalize(formula1)
    f2 = normalize(formula2)

    model = f"""
    MODULE main
    VAR
    ADCConnFailure : boolean;
    ADCError : 0..10;
    ADCRetries : 0..10;
    BreathingCycleStart : boolean;
    CONT : boolean;
    ExpiratoryPhaseEnd : boolean;
    ExpiratoryTime : 0..5000;
    ExpiratoryTriggerSensitivity : 0..100;
    F : 0..100;
    Fail : boolean;
    FailSafeMode : boolean;
    FinalState : 0..10;
    GBPS : 0..1000;
    GUIConnected : boolean;
    GUIFailure : boolean;
    GUIResumeRequest : boolean;
    ITS_PCV : boolean;
    ITS_PSV : boolean;
    IToE : 0..10;
    IToE_AP : 0..10;
    InhaleTriggerSensitivityPCV : 0..100;
    InhaleTriggerSensitivityPSV : 0..100;
    ItoE : 0..10;
    ItoE_AP : 0..10;
    ItoE_PCV : 0..10;
    MaxP_insp : 0..100;
    MinPEEPAtmAnalyzer : 0..50;
    OutOfServiceWarning : boolean;
    PCVInspTimeEnd : boolean;
    PCVMode : boolean;
    PCVModeSelected : boolean;
    PSVMode : boolean;
    PSVModeSelected : boolean;
    P_insp : 0..100;
    P_inspAP : 0..100;
    P_inspPCV : 0..100;
    P_inspPSV : 0..100;
    Pass : boolean;
    PeakV_E : 0..1000;
    RM : boolean;
    RMButton : boolean;
    RR : 0..100;
    RR_AP : 0..100;
    RR_PCV : 0..100;
    Seconds : 0..10000;
    SelfTestFail : boolean;
    SelfTestMode : boolean;
    SensorUse : boolean;
    Skip : boolean;
    StandbyMode : boolean;
    StartUpDone : boolean;
    StartUpMode : boolean;
    V_E : 0..1000;
    _PRC_ : boolean;
    airSupplyConnected : boolean;
    alarmSettingsChanged : boolean;
    apnea : boolean;
    apneaAlarm : boolean;
    apneaLagTime : 0..10000;
    breathingCircuitConnected : boolean;
    breathingCycleDone : boolean;
    breathingCycleStart : boolean;
    breathingCycleTime : 0..10000;
    breathingTime : 0..10000;
    breathingTimerReset : boolean;
    buttonUnPressOr : boolean;
    checkCommsGUI : boolean;
    checkCommsSensors : boolean;
    checkCommsValves : boolean;
    confirmPSVParameters : boolean;
    defaultParamsLoaded : boolean;
    disableLeakCompensation : boolean;
    displayF : 0..100;
    displayO : 0..100;
    displayRR : 0..100;
    displayTV : 0..1000;
    dropPAW : boolean;
    enableLeakCompensation : boolean;
    enterAlarmThresholds : boolean;
    eraseLog : boolean;
    error : boolean;
    expClock : 0..10000;
    expirationPhaseEnd : boolean;
    expirationPhaseStart : boolean;
    expiratoryPause : boolean;
    expiratoryPauseButton : boolean;
    expiratoryPhase : boolean;
    expiratoryPhaseEnd : boolean;
    expiratoryState : boolean;
    gasSupplyFailure : boolean;
    highPriorityAlarm : boolean;
    inValveClose : boolean;
    inValveOpen : boolean;
    initDone : boolean;
    initFail : boolean;
    initStart : boolean;
    inspClock : 0..10000;
    inspiratoryPause : boolean;
    inspiratoryPauseButton : boolean;
    inspiratoryPhase : boolean;
    inspiratoryPhaseEnd : boolean;
    inspiratoryPhaseStart : boolean;
    inspiratoryPressure : 0..100;
    inspiratoryTime : 0..10000;
    leakCompensation : boolean;
    leakCompensationActive : boolean;
    leakCompensationEnable : boolean;
    loadLastParams : boolean;
    loadLog : boolean;
    logAlarmParams : boolean;
    logAlarmSettings : boolean;
    logCalibrationParams : boolean;
    logO : boolean;
    logParams : boolean;
    logPatientChange : boolean;
    logPowerSupply : boolean;
    logPreUseCheck : boolean;
    logVentilationParams : boolean;
    logVentilatorSettings : boolean;
    measureF : 0..100;
    measureO : 0..100;
    measurePSins : 0..100;
    measureRR : 0..100;
    measureTV : 0..1000;
    minExpiratoryTime : 0..10000;
    monitorInhaleTrigger : boolean;
    newPatient : boolean;
    off : boolean;
    operator : boolean;
    outValveClose : boolean;
    outValveOpen : boolean;
    paramAlarm_V : 0..100;
    paramMax_V : 0..100;
    paramMin_V : 0..100;
    param_V : 0..100;
    parametersStored : boolean;
    patientAttributesEntered : boolean;
    patientBreathTrigger : boolean;
    patientBreathingRequest : boolean;
    patientChanged : boolean;
    patientConnected : boolean;
    patientSafe : boolean;
    powerButton : boolean;
    powerConnected : boolean;
    powerFailure : boolean;
    powerOff : boolean;
    powerSupplyChanged : boolean;
    preUseCheckDone : boolean;
    pressureSensorConnFailure : boolean;
    pressureSensorError : boolean;
    pressureSensorRetries : 0..10;
    resumeVentilation : boolean;
    runSelfTest : boolean;
    saveLog : boolean;
    selfTestFailed : boolean;
    selfTestPassed : boolean;
    startMonitoring : boolean;
    startPCV : boolean;
    startPSV : boolean;
    startReportingHealthParams : boolean;
    stopVentilation : boolean;
    testAlarmsFail : boolean;
    testAlarmsPass : boolean;
    testAlarmsSkip : boolean;
    testFL : boolean;
    testLeaksFail : boolean;
    testLeaksPass : boolean;
    testLeaksSkip : boolean;
    testOxygenSensorFail : boolean;
    testOxygenSensorPass : boolean;
    testOxygenSensorSkip : boolean;
    testPSExpFail : boolean;
    testPSExpPass : boolean;
    testPSExpSkip : boolean;
    testPowerSwitchFail : boolean;
    testPowerSwitchPass : boolean;
    testPowerSwitchSkip : boolean;
    user : boolean;
    ventilating : boolean;
    ventilationOff : boolean;
    ventilationParamsAdjustable : boolean;
    ventilatorSettingsChanged : boolean;

    LTLSPEC ({f1}) <-> ({f2})
    """


    with tempfile.NamedTemporaryFile(suffix=".smv", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(model)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["nuxmv.exe", tmp_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        #re.search(r"is\s+(true|false)", result_text, re.I)

        if "is true" in output:
            return True
        elif "is false" in output:
            return False
        else:
            print("⚠️ Unexpected NuXMV output format")
            return False
        
    finally:
        os.remove(tmp_path)


if __name__ == "__main__":

    # Example usage
    f1 = "H((classifier = 1 & dgt_7) -> (OpState = 1))"
    f2 = "H((classifier = 1) -> (dgt_7 -> (OpState = 1)))"

    g1 = "H((OpState=1 → (alert ∧ ¬slowdown ∧ ¬halt ∧ ¬turnoffUVC)))"
    g2 = "(H ((OpState = 1) -> ((((! slowdown) & (! halt)) & alert) & (! turnoffUVC))))"

    h1 = "(H ((classifier = 2) -> ((! dgt_3) -> (OpState = 3))))"
    h2 = "H(((classifier = 2) ∧ ¬dgt_3) → (OpState = 3))"

    equiv = check_equivalence_master(h1, h2)
    print("\nEquivalent:", equiv)
