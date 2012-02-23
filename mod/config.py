# encoding: utf-8

import sys
from mod.fuf import info


CONFIG_KEY_STUDENT_ID = u'StudentID'
CONFIG_KEY_STUDENT_PWD = u'StudentPwd'
CONFIG_KEY_GMAIL_ACCOUNT = u'GMailAccount'
CONFIG_KEY_GMAIL_PWD = u'GMailPwd'
CONFIG_KEY_THIS_CALENDAR_TITLE = u'ThisCalendarTitle'
CONFIG_KEY_THIS_CALENDAR_COLOR = u'ThisCalendarColor'
CONFIG_KEY_THIS_CALENDAR_SUMMARY = u'ThisCalendarSummary'
CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE = u'IfThisCalendarFoundThenPerformDelete'
CONFIG_KEY_SKIP_OPTIONAL_FIELDS = u'SkipOptionalFields'
CONFIG_KEY_LOAD_COURSES_FROM_WEB = u'LoadCoursesFromWeb'
CONFIG_KEY_LOAD_COURSES_FROM_FILE = u'LoadCoursesFromFile'
CONFIG_KEY_SERIALIZED_COURSES_PATH = u'SerializedCoursesPath'
CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_EXIT = u'IfSerializedCoursesPathNotFoundThenPerformExit'
CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_CREATE = u'IfSerializedCoursesPathNotFoundThenPerformCreate'
CONFIG_KEY_FILTER_COURSE_BY_COURSE_NAME = u'FilterCourseByCourseName'
CONFIG_KEY_FILTER_COURSE_BY_TEACHER_NAME = u'FilterCourseByTeacherName'


configs = {
    CONFIG_KEY_STUDENT_ID: u'',
    CONFIG_KEY_STUDENT_PWD: u'',
    CONFIG_KEY_GMAIL_ACCOUNT: u'',
    CONFIG_KEY_GMAIL_PWD: u'',
    CONFIG_KEY_THIS_CALENDAR_TITLE: u'武大课表',
    CONFIG_KEY_THIS_CALENDAR_COLOR: u'#2952A3',
    CONFIG_KEY_THIS_CALENDAR_SUMMARY: u'created by whu-course-helper',
    CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE: True,
    CONFIG_KEY_SKIP_OPTIONAL_FIELDS: False,
    CONFIG_KEY_LOAD_COURSES_FROM_WEB: True,
    CONFIG_KEY_LOAD_COURSES_FROM_FILE: True,
    CONFIG_KEY_SERIALIZED_COURSES_PATH: True,
    CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_EXIT: False,
    CONFIG_KEY_IF_SERIALIZED_COURSES_PATH_NOT_FOUND_THEN_PERFORM_CREATE: True,
    CONFIG_KEY_FILTER_COURSE_BY_COURSE_NAME: True,
    CONFIG_KEY_FILTER_COURSE_BY_TEACHER_NAME: True
}

# note that if you are using linux or any other modern ide which supports unicode,
# please set the following variable to 'utf-8'
# warning: don't modify this if you don't know what you're doing!
ConsoleEncoding = sys.stdout.encoding

# warning: don't modify this if you don't know what you're doing!
FileEncoding = 'utf-8'


def readConfig():
    try:
        info('info', 'trying to load CONFIG_sample_en')
        f = unicode(open('CONFIG_sample_en', 'r').read(), FileEncoding)

        for line in f.split(u'\n'):
            if line.startswith(u'#'):
                continue

            if u'=' in line:
                l = [s.strip() for s in line.split(u'=')]
                if l[0] in configs:
                    info('dbg', 'config %s found, value=%s' % (l[0], eval(l[1])))
                    configs[l[0]] = eval(l[1])
                else:
                    info('err', 'unrecognized config parameter %s' % l[0])

    except IOError as err:
        if err.errno == 2:
            info('info', 'CONFIG_sample_en not found, using default config')
            return
        else:
            info('err', 'error while loading CONFIG_sample_en')
            return


readConfig()

