#!/usr/bin/env python


import unittest
import os
import sys
import math
import time
from motor_lib import motor_lib
lib = motor_lib()
from motor_globals import motor_globals
globals = motor_globals()
import capv_lib

###

polltime = 0.2

class Test(unittest.TestCase):
    motor = os.getenv("TESTEDMOTORAXIS")
    capv_lib.capvput(motor + '-DbgStrToLOG', "Start " + os.path.basename(__file__)[0:20])

    hlm = capv_lib.capvget(motor + '.HLM')
    llm = capv_lib.capvget(motor + '.LLM')

    per10_UserPosition  = round((9 * llm + 1 * hlm) / 10)
    per20_UserPosition  = round((8 * llm + 2 * hlm) / 10)
    msta                = int(capv_lib.capvget(motor + '.MSTA'))

    def getAcceleration(self, motor, tc_no):
        print('%s: getAcceleration %s' % (tc_no, motor))
        res = capv_lib.capvget(motor + '-Acc-RB', use_monitor=False)
        return res


    # Assert that motor is homed
    def test_TC_401(self):
        motor = self.motor
        tc_no = "TC-401"
        if not (self.msta & lib.MSTA_BIT_HOMED):
            self.assertNotEqual(0, self.msta & lib.MSTA_BIT_HOMED, 'MSTA.homed (Axis has been homed)')
        lib.initializeMotorRecordSimulatorAxis(motor, '1211')

    # 10% dialPosition
    def test_TC_402(self):
        tc_no = "TC-402-10-percent"
        print('%s' % tc_no)
        motor = self.motor
        if (self.msta & lib.MSTA_BIT_HOMED):
            ret = lib.move(self.motor, self.per10_UserPosition, 60)
            assert (ret == 0)

    # 20% dialPosition
    def test_TC_403(self):
        tc_no = "TC-403-20-percent"
        print('%s' % tc_no)
        motor = self.motor
        if (self.msta & lib.MSTA_BIT_HOMED):
            saved_ACCL = float(capv_lib.capvget(motor + '.ACCL'))
            saved_VELO = float(capv_lib.capvget(motor + '.VELO'))
            used_ACCL = saved_ACCL + 1.0 # Make sure we have an acceleration != 0
            capv_lib.capvput(motor + '.ACCL', used_ACCL)
            ret = lib.move(self.motor, self.per20_UserPosition, 60)
            resacc = self.getAcceleration(motor, tc_no)
            expacc = saved_VELO / used_ACCL
            capv_lib.capvput(motor + '.ACCL', saved_ACCL)
            print('%s ACCL=%f expacc=%f resacc=%f' % (tc_no,used_ACCL,expacc,resacc))
            assert lib.calcAlmostEqual(self.motor, tc_no, expacc, resacc, 2)
            assert (ret == 0)


    # JOGR
    def test_TC_404(self):
        tc_no = "TC-404-JOGR"
        print('%s' % tc_no)
        motor = self.motor
        if (self.msta & lib.MSTA_BIT_HOMED):
            accl = float(capv_lib.capvget(motor + '.ACCL'))
            jvel = float(capv_lib.capvget(motor + '.JVEL'))
            saved_JAR = float(capv_lib.capvget(motor + '.JAR'))
            used_JAR = jvel / (accl + 2.0)
            capv_lib.capvput(motor + '.JAR', used_JAR)
            capv_lib.capvput(motor + '.JOGR', 1, wait=True)
            resacc = self.getAcceleration(motor, tc_no)
            expacc = used_JAR
            capv_lib.capvput(motor + '.JAR', saved_JAR)
            print('%s JAR=%f expacc=%f resacc=%f' % (tc_no,used_JAR,expacc,resacc))

            assert lib.calcAlmostEqual(self.motor, tc_no, expacc, resacc, 2)

