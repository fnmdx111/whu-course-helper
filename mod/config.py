# encoding: utf-8
import os

import sys
from const.constants import info


CONFIG_KEY_STUDENT_ID = u'StudentID'
CONFIG_KEY_STUDENT_PWD = u'StudentPwd'
CONFIG_KEY_GMAIL_ACCOUNT = u'GMailAccount'
CONFIG_KEY_GMAIL_PWD = u'GMailPwd'
CONFIG_KEY_THIS_CALENDAR_TITLE = u'ThisCalendarTitle'
CONFIG_KEY_THIS_CALENDAR_COLOR = u'ThisCalendarColor'
CONFIG_KEY_THIS_CALENDAR_SUMMARY = u'ThisCalendarSummary'
CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE = u'IfThisCalendarFoundThenPerformDelete'

# these values are default values in case there isn't corresponding value in the `CONFIG' file
configs = {
    CONFIG_KEY_STUDENT_ID: u'',
    CONFIG_KEY_STUDENT_PWD: u'',
    CONFIG_KEY_GMAIL_ACCOUNT: u'',
    CONFIG_KEY_GMAIL_PWD: u'',
    CONFIG_KEY_THIS_CALENDAR_TITLE: u'武大课表',
    CONFIG_KEY_THIS_CALENDAR_COLOR: u'#2952A3',
    CONFIG_KEY_THIS_CALENDAR_SUMMARY: u'created by whu-course-helper',
    CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE: True,
}

def read_configs():
    global ConfigRead

    try:
        info('info', 'trying to load CONFIG')
        info('dbg', 'current working directory: %s' % os.getcwd())
        f = unicode(open('CONFIG', 'r').read(), 'utf-8')

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
            info('info', 'CONFIG not found, using default config')
            return
        else:
            info('err', 'error while loading CONFIG')
            return


