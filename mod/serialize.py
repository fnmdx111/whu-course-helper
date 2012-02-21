# encoding: utf-8

import json
from mod.course_related import MyCourse, CourseSchedule
from const.constants import  ABBR_DAYS_TO_DAYS, CONSOLE_ENCODING
from config import SkipOptionalFields
from const.dict_keys import *
from mod.fuf import info

def serializeCourses(courses, path='serialized_courses.txt'):
    """
        note that i only choose json for serialization,
        because pickle isn't really safe according to the python manual
    """
    coursesDicts = []

    for item in courses:
        d = item.getProperties()
        d[SCHEDULE] = item[:]

        coursesDicts.append(d)

    with open(path, 'w') as f:
        print >> f, json.dumps(coursesDicts, ensure_ascii=False).encode('utf-8')


def deserializeMyCourses(path='serialized_courses.txt'):
    with open(path, 'r') as f:
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
        return unicode(raw_input('%s field(%s)? ' % ('necessary' if necessary else 'optional', fieldName)), CONSOLE_ENCODING)

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

    if not SkipOptionalFields:
        for field in optionalFields:
            input = _promptInput(field, necessary=False)
            if input != '':
                courseDict[field] = input

    thisCourse = MyCourse(courseDict)

    info('info', 'schedules example %s\nenter q to end schedules inputting\navailable weekdays are mon, tue, wed, thu, fri, sat, sun' % scheduleExample)
    while True:
        input = unicode(raw_input('schedule? '), CONSOLE_ENCODING)

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


if __name__ == '__main__':
    serializeCourses([createCustomCourse(), createCustomCourse()])
    courses = deserializeMyCourses()

    for item in courses:
        print item
