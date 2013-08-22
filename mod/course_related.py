# encoding: utf-8
from abc import abstractmethod
from const.dict_keys import *


class Course(list):

    def __init__(self, properties=None):
        list.__init__(self)

        if not properties:
            return
        self.set_properties(properties)

    def set_property(self, key, data):
        self._properties[key] = data

    def set_properties(self, properties):
        self._properties = {}
        for key in properties:
            self._properties[key] = properties[key]

    def property(self, key):
        if key in self._properties:
            return self._properties[key]

    def properties(self):
        return self._properties

    @abstractmethod
    def __unicode__(self):
        pass

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        if self.property(COURSE_NAME) == other.property(COURSE_NAME):
            if self.property(TEACHER_NAME) == other.property(TEACHER_NAME):
                return True

        return False


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
Schedules are\n'''.format(**self.properties())\
        + u'\n'.join([item.__unicode__() if item else u'' for item in self])



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


    def __init__(self, fromDict=None):
        super(CourseSchedule, self).__init__()

        if fromDict:
            self._fromDict(fromDict)
            return


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


