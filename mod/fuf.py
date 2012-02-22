# encoding: utf-8

"""
    fuf ::= frequently used functions
"""
import getpass
from const.constants import switch
from const.dict_keys import CLASSROOM, BUILDING


def info(channel, msg):
    if switch[channel]:
        print '%s: %s' % (channel, msg)


def getAccountInfo(variable, prompt, usePwdMode=False):
    if variable is None or variable == '':
        if usePwdMode:
            if switch['dbg']:
                return raw_input(prompt)
            else:
                return getpass.getpass(prompt)
        else:
            return raw_input(prompt)

    return variable


def genLocationByCourseSchedule(schedule):
    classroomAndBuilding = schedule[BUILDING]
    if schedule[BUILDING] != schedule[CLASSROOM]:
        classroomAndBuilding += u'-%s' % schedule[CLASSROOM]

    return classroomAndBuilding

