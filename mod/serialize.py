# encoding: utf-8

import json
from mod.config import *
from mod.course_related import MyCourse, CourseSchedule
from const.constants import  ABBR_DAYS_TO_DAYS
from const.dict_keys import *
from mod.fuf import info

def serializeCourses(courses, f):
    """
        note that i only choose json for serialization,
        because pickle isn't really safe according to the python manual
    """
    coursesDicts = []

    for item in courses:
        d = item.getProperties()
        d[SCHEDULE] = item[:]

        coursesDicts.append(d)

    print >> f, json.dumps(coursesDicts, ensure_ascii=False).encode(FileEncoding)

    return True


def deserializeMyCourses(f):
    courses_dicts = json.load(f)

    courses = []
    for item in courses_dicts:
        course = MyCourse()

        schedules = item[SCHEDULE][:]
        del item[SCHEDULE]

        course.setProperties(item)
        for schedule in schedules:
            course.append(CourseSchedule(fromDict=schedule))

        courses.append(course)

    return courses


def createCustomCourse(scheduleParser, necessaryFields, optionalFields, schedulePattern, scheduleExample, scheduleParameterCount):
    def _promptInput(fieldName, necessary=True):
        return unicode(raw_input('%s field(%s)? ' % ('necessary' if necessary else 'optional', fieldName)), ConsoleEncoding)

    courseDict = {}
    for key in MyCourse.KEYS:
        courseDict[key] = u'n/a'

    info('info', 'beginning to input fields, press enter to ignore')
    for field in necessaryFields:
        while True:
            input = _promptInput(field)
            if input == '':
                info('err', 'necessary fields cannot be ignored')
                continue
            else:
                courseDict[field] = input
                break

    if not configs[CONFIG_KEY_SKIP_OPTIONAL_FIELDS]:
        for field in optionalFields:
            input = _promptInput(field, necessary=False)
            if input != '':
                courseDict[field] = input

    thisCourse = MyCourse(courseDict)

    info('info', 'schedules example %s\nenter q to end schedules inputting\navailable weekdays are mon, tue, wed, thu, fri, sat, sun' % scheduleExample)
    while True:
        input = unicode(raw_input('schedule? '), ConsoleEncoding)

        if input == 'q':
            break
        else:
            l = input.split(u' ')

            if len(l) != scheduleParameterCount:
                info('err', 'invalid input')
                continue


            thisSchedule = scheduleParser(CourseSchedule(), ABBR_DAYS_TO_DAYS[l[0]], schedulePattern.format(*l[1:]))

            thisCourse.append(thisSchedule)

    return thisCourse

