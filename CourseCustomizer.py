from const import constants
from const.dict_keys import COURSE_NAME, TEACHER_NAME
from mod import whu
from mod.config import *
from mod.fuf import getAccountInfo
from mod.serialize import deserializeMyCourses, createCustomCourse, serializeCourses

usage = """usage:
\t(c)reate a new custom course
\t(d)elete a course
\t(l)oad from another local txt file
\t(s)ave changes
\ts(h)ow courses
\tse(r)ialize courses from web
\tshow (u)sage
\t(e)xit"""


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
                    return open(path, 'w')
                except Exception as err:
                    info('err', 'error creating %s, program will now shutdown\ndetail: %s' % (path, err))
                    exit(0)


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


customCourses = init()


def createNewCourse():
    customCourses.append(createCustomCourse())


def saveChanges(courses, path=configs[CONFIG_KEY_SERIALIZED_COURSES_PATH]):
    try:
        f = open(path, 'w')
        info('info', 'saving courses')
        if serializeCourses(courses, f):
            info('info', 'serialization succeeded')
            f.close()
    except IOError as err:
        info('err', 'an error occurred while trying to write %s\n%s' % (path, err))
        return


def serializeCoursesFromWeb(studentID, studentPwd):
    global customCourses

    _, courses = whu.readCourses(studentID, studentPwd, LoadCoursesFromFile=False)

    customCourses += courses
    info('info', '%s course(s) from web has been grabbed from your personal timetable' % len(courses))


def getInterestingCourses(keyword):
    byCourseName = [course for course in customCourses if keyword in course.getProperty(COURSE_NAME)]
    byTeacherName = [course for course in customCourses if keyword in course.getProperty(TEACHER_NAME)]

    result = []
    if configs[CONFIG_KEY_FILTER_COURSE_BY_COURSE_NAME]:
        result += byCourseName
    if configs[CONFIG_KEY_FILTER_COURSE_BY_TEACHER_NAME]:
        result += byTeacherName

    return result


def selectSpecificCourse(justShowing=False):
    keyword = raw_input('keyword? ')

    interestedCourses = getInterestingCourses(keyword)

    for i, course in enumerate(interestedCourses):
        print (u'%s. %s' % (i, course)).encode(ConsoleEncoding)

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
        return raw

    return None


def deleteCourse(num):
    info('info', '%s by %s will be deleted' % (customCourses[num].getProperty(COURSE_NAME), customCourses[num].getProperty[TEACHER_NAME]))
    con = raw_input('continue? (y/n)')

    if con == 'y':
        del customCourses[num]
    else:
        return


operations = {
    'c': createNewCourse,
    'd': lambda: deleteCourse(selectSpecificCourse()),
    'l': lambda: init(raw_input('path? ')),
    's': lambda: saveChanges(customCourses),
    'h': lambda: selectSpecificCourse(justShowing=True),
    'r': lambda: serializeCoursesFromWeb(getAccountInfo(configs[CONFIG_KEY_STUDENT_ID], constants.ID_PROMPT),
                                 getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD], constants.PASSWORD_PROMPT, usePwdMode=True)),
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
            operations[cmd]()

    return None


if __name__ == '__main__':
    main()

