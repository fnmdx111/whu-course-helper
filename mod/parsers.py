# encoding: utf-8
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
                course.append(CourseSchedule(course.getProperty(key), key))
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
                course.append(CourseSchedule(course.getProperty(key), key))
            else:
#                course.setProperty(key, None)
                del course.getProperties()[key]

        #special case for major
        _validatePropertyContent(course.getProperties(), MAJOR)
        #special case for remarks
        _validatePropertyContent(course.getProperties(), REMARKS)

        courseData.append(course)

    return courseData

