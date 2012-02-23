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


def createCustomCourse():
    def _promptInput(fieldName, necessary=True):
        return unicode(raw_input('%s field(%s)? ' % ('necessary' if necessary else 'optional', fieldName)), ConsoleEncoding)

    schedulePattern = u'{0}-{1}周,每{2}周;{3}-{4}节,{5}区,{6}'
    scheduleExample = u'周一 1-15周,每1周;3-5节,3区,附1-302 => mon 1 15 1 3 5 3 附1-302'

    necessaryFields = (
        COURSE_NAME,
        TEACHER_NAME,
    )
    optionalFields = (
        SCORE_TYPE,
        COURSE_TYPE,
        MAJOR,
        CREDIT,
        PERIOD,
        REMARKS
    )

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

            if len(l) != 8:
                info('err', 'invalid input')
                continue

            thisSchedule = CourseSchedule(schedulePattern.format(*l[1:]), ABBR_DAYS_TO_DAYS[l[0]])

            thisCourse.append(thisSchedule)

    return thisCourse

