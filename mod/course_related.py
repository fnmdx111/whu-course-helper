# encoding: utf-8
from abc import abstractmethod
from const.dict_keys import *
import re


class Course(list):

    def __init__(self, properties=None):
        list.__init__(self)

        if not properties:
            return
        self.setProperties(properties)

    def setProperty(self, key, data):
        self._properties[key] = data

    def setProperties(self, properties):
        self._properties = {}
        for key in properties:
            self._properties[key] = properties[key]

    def getProperty(self, key):
        if key in self._properties:
            return self._properties[key]

    def getProperties(self):
        return self._properties

    @abstractmethod
    def __unicode__(self):
        pass

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class PublicCourse(Course):

    KEYS = (
        COURSE_NAME,
        TYPE,
        CREDIT,
        STUDENT_CAPACITY,
        TEACHER_NAME,
        TEACHER_TITLE,
        SCHOOL,
        PERIOD,
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY,
        REMARKS,
        TEXT_BOOK,
        YEAR,
        SEMESTER
    )

    def __unicode__(self):
        return u'''Course: {course_name} by {teacher_title} {teacher_name} at {school} within {period} class hour(s) of {year} {semester}
Credit: {credit}
Textbook: {text_book}
Remarks: {remarks}
Schedules are\n'''.format(**self.getProperties())\
        + u'\n'.join([item.__unicode__() for item in self])

class MyCourse(Course):

    KEYS = (
        OPERATION,
        COURSE_HEADER_STATUS,
        COURSE_HEADER,
        COURSE_NAME,
        COURSE_NUMBER,
        SCORE_TYPE,
        COURSE_TYPE,
        TEACHING_SCHOOL,
        TEACHER_NAME,
        PLANNING_SCHOOL, # wtf??
        MAJOR,
        CREDIT,
        PERIOD,
        MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY, # index of 13, 14, 15, 16, 17, 18, 19
        REMARKS,
        YEAR,
        SEMESTER
    )

    def __unicode__(self):
        return u'''{course_type} {score_type} course {course_name} with course header {course_header} by {teacher_name} at {teaching_school} within {period} class hour(s) of {year} {semester}
Credit: {credit}
Remarks: {remarks}
Course Status: {course_header_status}
Course Number: {course_number}
Major: {major}
Available Operation(s): {operation}
Remarks: {remarks}
Schedules are\n'''.format(**self.getProperties())\
        + u'\n'.join([item.__unicode__() for item in self])



class CourseSchedule(dict):

    KEYS = (
        DAY,
        STARTING_WEEK,
        ENDING_WEEK,
        FREQUENCY,
        STARTING_CLASS_NUMBER,
        ENDING_CLASS_NUMBER,
        DISTRICT,
        CLASSROOM,
        BUILDING
    )
    KEYS_FOR_RE = KEYS[1:len(KEYS) - 1]
    PATTERN = re.compile(ur'^.*'\
                         ur'(?P<%s>\d{1,2})\D+(?P<%s>\d{1,2})周'\
                         ur'\s*,\s*'\
                         ur'每(?P<%s>\d+)周'\
                         ur'\s*;\s*'\
                         ur'(?P<%s>\d{1,2})\D+(?P<%s>\d{1,2})节'\
                         ur'\s*,s*'\
                         ur'(?:(?P<%s>\d+)区)?'\
                         ur'\s*,\s*'\
                         ur'(?:(?P<%s>.+))?$' % KEYS_FOR_RE)
    pattern1 = re.compile(ur'^(\d+)$')
    pattern2 = re.compile(ur'^(.+)\s*-\s*(\d+)$')
    pattern3 = re.compile(ur'^(.+?)(\d+)$')

    def __init__(self, rawData=None, day=None, fromDict=None):
        dict.__init__(self)

        if fromDict:
            self._fromDict(fromDict)
            return

        matches = CourseSchedule.PATTERN.search(rawData)

        self[DAY] = day

        if matches:
            for key in CourseSchedule.KEYS_FOR_RE:
                self[key] = matches.groupdict()[key]

            if not self[CLASSROOM]:
                self[BUILDING] = None
                return


            matches1 = CourseSchedule.pattern1.search(matches.groupdict().get(CLASSROOM, ''))
            matches2 = CourseSchedule.pattern2.search(matches.groupdict()[CLASSROOM]) or CourseSchedule.pattern3.search(matches.groupdict()[CLASSROOM])
            if matches1:
                self[BUILDING] = self[CLASSROOM]
            elif matches2:
                self[BUILDING] = matches2.group(1)
                self[CLASSROOM] = matches2.group(2)


    def _fromDict(self, fromDict):
        for key in CourseSchedule.KEYS:
            self[key] = u'n/a'

        for key in fromDict:
            self[key] = fromDict[key]


    def __unicode__(self):
        s = self[DAY] + u'''\n\tweek {starting_week} to {ending_week} (every {frequency} week)
\tfrom class {starting_class_number} to {ending_class_number}
\tat district {district} '''.format(**self)

        building = self[BUILDING]
        classroom = self[CLASSROOM]
        if building == classroom:
            return s + (building if building else u'n/a')
        else:
            return s + u'%s-%s' % (building, classroom)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

