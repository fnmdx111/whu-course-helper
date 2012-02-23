# encoding: utf-8

"""
    fuf ::= frequently used functions
"""
import getpass
from const.constants import switch, info
from const.dict_keys import CLASSROOM, BUILDING
from mod.config import CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_CREATE, configs, CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_EXIT


def getAccountInfo(variable, prompt, usePwdMode=False):
    if variable == u'':
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


def eliminateRepeatingCourses(l):
    result = []
    for item in l:
        if item not in result:
            result.append(item)

    return result


def openTxt(path):
    try:
        return open(path, 'r')
    except IOError as err:
        if err.errno == 2:
            if configs[CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_EXIT]:
                info('err', '%s not found, program will now shutdown' % path)
                exit(0)
            elif configs[CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_CREATE]:
                info('info', '%s not found, creating %s' % (path, path))
                try:
                    f = open(path, 'w')
                    f.close()
                    return open(path, 'r')
                except Exception as err:
                    info('err', 'error creating %s, program will now shutdown\ndetail: %s' % (path, err))
                    exit(0)


