# encoding: utf-8

import sys
from mod.fuf import info

StudentID = ''
StudentPwd = ''

GMailAccount = ''
GMail_Pwd = ''


ThisCalendarTitle = u'武大课表'
ThisCalendarColor = u'#2952A3'
ThisCalendarSummary = u'created by WhuCoursesHelper'

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
    'StudentID': u'',
    'StudentPwd': u'',
    'GMailAccount': u'',
    'GMail_Pwd': u'',
    'ThisCalendarTitle': u'',
    'ThisCalendarColor': u'',
    'ThisCalendarSummary': u''
}

# note that if you are using linux or any other modern ide which supports unicode,
# please set the following variable to 'utf-8'
# warning: don't modify this if you don't know what you're doing!
ConsoleEncoding = sys.stdout.encoding

# warning: don't modify this if you don't know what you're doing!
FileEncoding = 'utf-8'
