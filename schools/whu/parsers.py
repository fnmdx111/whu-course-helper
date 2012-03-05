# encoding: utf-8
import re
from const.dict_keys import *
from mod.course_related import CourseSchedule, PublicCourse, MyCourse

def _validatePropertyContent(d, key, illegal=u'&nbsp;', legal=u'n/a'):
    if d[key] == illegal:
        d[key] = legal


def publicCoursesParser(rawCourseData):
    # the first 3 <tr> actually do not contain course data
    rawCourseData = rawCourseData[2:]

    courseData = []
    for tr in rawCourseData:
        properties = {}
        for propertyCount, td in enumerate(tr.findAll('td')):
            content = td.contents[1 if propertyCount == 3 else 0] # special case for student_capacity
            if content:
                content = content.lstrip().rstrip()
            properties[PublicCourse.KEYS[propertyCount]] = content

        course = PublicCourse(properties)

        # special case for days
        for key in PublicCourse.KEYS[8:15]:
            if course.getProperty(key) != u'&nbsp;':
                course.getProperties()[key] = ''.join(course.getProperties()[key].split('\n'))
                course.append(scheduleParser(CourseSchedule(), key, course.getProperty(key)))
            else:
#                course.setProperty(key, None)
                del course.getProperties()[key]

        #special case for textbooks
        _validatePropertyContent(course.getProperties(), TEXT_BOOK)
        #special case for remarks
        _validatePropertyContent(course.getProperties(), REMARKS)

        courseData.append(course)

    return courseData


def myCoursesParser(rawCourseData):
    courseData = []
    for tr in rawCourseData:
        properties = {}
        for propertyCount, td in enumerate(tr.findAll('td')):
            content = td.contents[0]
            if content:
                content = content.lstrip().rstrip()
            properties[MyCourse.KEYS[propertyCount]] = content

        course = MyCourse(properties)

        # special case for days
        for key in MyCourse.KEYS[13:20]:
            if course.getProperty(key) != u'&nbsp;':
                course.getProperties()[key] = ''.join(course.getProperties()[key].split('\n'))
                course.append(scheduleParser(CourseSchedule(), key, course.getProperty(key)))
            else:
#                course.setProperty(key, None)
                del course.getProperties()[key]

        #special case for major
        _validatePropertyContent(course.getProperties(), MAJOR)
        #special case for remarks
        _validatePropertyContent(course.getProperties(), REMARKS)

        courseData.append(course)

    return courseData

def genLocationByCourseSchedule(schedule):
    classroomAndBuilding = schedule[BUILDING]
    if schedule[BUILDING] != schedule[CLASSROOM]:
        classroomAndBuilding += u'-%s' % schedule[CLASSROOM]

    return classroomAndBuilding


KEYS_FOR_RE = CourseSchedule.KEYS[1:len(CourseSchedule.KEYS) - 1]
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
pattern2 = re.compile(ur'^([^\-]+)\s*\-\s*([A-Za-z0-9]+)$')
pattern3 = re.compile(ur'^(.+?)(\d+)$')
def scheduleParser(self, day, rawData):
    matches = PATTERN.search(rawData)

    self[DAY] = day

    if matches:
        for key in KEYS_FOR_RE:
            self[key] = matches.groupdict()[key]

        if not self[CLASSROOM]:
            self[BUILDING] = None
            return


        matches1 = pattern1.search(matches.groupdict().get(CLASSROOM, ''))
        matches2 = pattern2.search(matches.groupdict()[CLASSROOM]) or pattern3.search(matches.groupdict()[CLASSROOM])
        if matches1:
            self[BUILDING] = self[CLASSROOM]
        elif matches2:
            self[BUILDING] = matches2.group(1)
            self[CLASSROOM] = matches2.group(2)

    return self
