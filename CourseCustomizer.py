from const import constants
from const.dict_keys import COURSE_NAME, TEACHER_NAME
from mod.config import *
from mod.exceptions import InvalidIDOrPasswordError, WrongCaptchaError
from mod.fuf import getAccountInfo, eliminateRepeatingCourses, openTxt
from mod.serialize import deserializeMyCourses, createCustomCourse, serializeCourses
from schools.whu import whu

usage = """usage:
\t(c)reate a new custom course
\t(d)elete a course
\t(l)oad from another local txt file
\t(s)ave changes
\ts(h)ow courses
\tcle(a)r courses
\tse(r)ialize courses from web
\tshow (u)sage
\t(e)xit"""


def init(path=configs[CONFIG_KEY_SERIALIZED_COURSES_PATH]):
    f = openTxt(path)
    try:
        if f:
            info('info', 'loading serialized courses from %s' % path)
            return deserializeMyCourses(f)
        else:
            return []
    except ValueError as err:
        if 'No JSON object could be decoded' in err.__str__():
            return []
        else:
            info('err', 'fatal error %s' % err)
    finally:
        f.close()


customCourses = eliminateRepeatingCourses(init())


def createNewCourse():
    customCourses.append(createCustomCourse())


def saveChanges(courses, path=configs[CONFIG_KEY_SERIALIZED_COURSES_PATH]):
    try:
        f = open(path, 'w')
        info('info', 'saving courses')
        if serializeCourses(eliminateRepeatingCourses(courses), f):
            info('info', 'serialization succeeded')
            f.close()
            if f.closed:
                info('dbg', '%s closed' % path)
    except IOError as err:
        info('err', 'an error occurred while trying to write %s\n%s' % (path, err))
        return


def serializeCoursesFromWeb(studentID, studentPwd):
    global customCourses

    _, courses = whu.readCourses(studentID, studentPwd, LoadCoursesFromFile=False)

    newCourses = [course for course in courses if course not in customCourses]
    info('info', '%s course(s) from web has been grabbed from your personal timetable, of which %s course(s) is new' % (len(courses), len(newCourses)))

    customCourses += courses


def getInterestingCourses(keyword):
    byCourseName = [(num, course) for num, course in enumerate(customCourses) if keyword in course.getProperty(COURSE_NAME)]
    byTeacherName = [(num, course) for num, course in enumerate(customCourses) if keyword in course.getProperty(TEACHER_NAME)]

    result = []
    if configs[CONFIG_KEY_FILTER_COURSE_BY_COURSE_NAME]:
        result = [item for item in byCourseName if item not in result]
    if configs[CONFIG_KEY_FILTER_COURSE_BY_TEACHER_NAME]:
        result += [item for item in byTeacherName if item not in result]

    return result


def selectSpecificCourse(justShowing=False):
    keyword = unicode(raw_input('keyword? '), ConsoleEncoding)

    interestedCourses = getInterestingCourses(keyword)

    for i, item in enumerate(interestedCourses):
        print (u'%s. %s' % (i, item[1])).encode(ConsoleEncoding)

    if justShowing:
        return None

    while True:
        raw = raw_input('num? ')
        if not raw.isdigit():
            info('err', 'invalid input, please input an integer')
            continue
        raw = int(raw)
        if raw not in range(0, len(interestedCourses)):
            info('err', 'invalid input, please input an integer in range 0 - %s' % (len(interestedCourses) - 1))
            continue
        return interestedCourses[raw][0]

    return None


def deleteCourse(num):
    info('info', '%s by %s will be deleted' % (customCourses[num].getProperty(COURSE_NAME), customCourses[num].getProperty(TEACHER_NAME)))
    con = raw_input('continue? (y/n)')

    if con == 'y':
        del customCourses[num]
    else:
        return


def clearCourses():
    global customCourses
    customCourses = []

    info('info', 'courses have been cleared')


operations = {
    'c': createNewCourse,
    'd': lambda: deleteCourse(selectSpecificCourse()),
    'l': lambda: init(raw_input('path? ')),
    's': lambda: saveChanges(customCourses),
    'h': lambda: selectSpecificCourse(justShowing=True),
    'r': lambda: serializeCoursesFromWeb(getAccountInfo(configs[CONFIG_KEY_STUDENT_ID], constants.ID_PROMPT),
                                 getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD], constants.PASSWORD_PROMPT, usePwdMode=True)),
    'a': clearCourses,
    'e': lambda: exit(0)
}


def main():
    print usage

    while True:
        cmd = raw_input('cmd? ')
        if cmd == 'u':
            print usage
        elif cmd not in operations:
            info('err', 'invalid input, please follow the usage')
            continue
        else:
            try:
                operations[cmd]()
            except InvalidIDOrPasswordError:
                info('err', 'invalid id or password')
            except WrongCaptchaError:
                info('err', 'wrong captcha')

    return None


if __name__ == '__main__':
    main()

