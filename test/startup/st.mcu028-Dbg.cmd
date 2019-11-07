require EthercatMC,USER

epicsEnvSet("ECM_NUMAXES",   "2")
epicsEnvSet("MOTOR_PORT",    "$(SM_MOTOR_PORT=MCU1)")

epicsEnvSet("IPADDR",        "$(SM_IPADDR=192.168.88.78)")
epicsEnvSet("IPPORT",        "$(SM_IPPORT=5000)")
epicsEnvSet("ASYN_PORT",     "$(SM_ASYN_PORT=MC_CPU1)")
epicsEnvSet("PREFIX",        "$(SM_PREFIX=LabS-MCAG:)")
epicsEnvSet("P",             "$(SM_PREFIX=LabS-MCAG:)")
epicsEnvSet("EGU",           "$(SM_EGU=mm)")
epicsEnvSet("PREC",          "$(SM_PREC=3)")

epicsEnvSet("ECM_OPTIONS",          "")
# Controller
< EthercatMCController.iocsh


# Axis 1
epicsEnvSet("MOTOR_NAME",    "$(SM_MOTOR_NAME=MC-MCU-28:m1)")
epicsEnvSet("AXIS_NO",       "$(SM_AXIS_NO=1)")
epicsEnvSet("DESC",          "$(SM_DESC=Lower)")
epicsEnvSet("AXISCONFIG",    "HomProc=1;HomPos=-63")


< EthercatMCAxis.iocsh
< EthercatMCAxisdebug.iocsh
< EthercatMCAxishome.iocsh


epicsEnvSet("MOTOR_NAME",    "$(SM_MOTOR_NAME=MC-MCU-28:m2)")
epicsEnvSet("AXIS_NO",       "$(SM_AXIS_NO=2)")
epicsEnvSet("DESC",          "$(SM_DESC=Upper)")
epicsEnvSet("AXISCONFIG",    "HomProc=1;HomPos=0")

< EthercatMCAxis.iocsh
< EthercatMCAxisdebug.iocsh
< EthercatMCAxishome.iocsh

