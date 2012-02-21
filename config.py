# encoding: utf-8
from mod.fuf import info

STUDENT_ID = ''
STUDENT_PWD = ''

GMAIL_ACCOUNT = ''
GMAIL_PWD = ''


THIS_CALENDAR_TITLE = u'武大课表'
THIS_CALENDAR_COLOR = u'#2952A3'
THIS_CALENDAR_SUMMARY = u'created by WhuCoursesHelper'

OnThisCalendarFoundPerformDelete = True
DetectAlreadyInsertedCourse = False # not implemented
SkipOptionalFields = True

LoadCoursesFromWeb = True
LoadCoursesFromFile = True

SerializedCoursesPath = 'serialized_courses.txt'


# the following function's functionality hasn't been tested, therefore it will be closed until it is tested.
def fromFile(path='config'):
    try:
        f = open(path, 'r')
        for line in f.readlines():
            for key in GLOBALS:
                if key in line:
                    GLOBALS[key] = line.split('=')[1]
    except Exception as err:
        info('err', err)


GLOBALS = {
    'STUDENT_ID': u'',
    'STUDENT_PWD': u'',
    'GMAIL_ACCOUNT': u'',
    'GMAIL_PWD': u'',
    'THIS_CALENDAR_TITLE': u'',
    'THIS_CALENDAR_COLOR': u'',
    'THIS_CALENDAR_SUMMARY': u''
}