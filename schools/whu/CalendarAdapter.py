# encoding: utf-8

import __init__
import datetime
from mod.google_calendar_proxy import *
from mod.fuf import getAccountInfo
from schools.whu import whu
from schools.whu.constants import *
from schools.whu.parsers import genLocationByCourseSchedule


class WhuGoogleCalendarAdapter(object):

    """
        this adapter consumes courses of whu, and excrete dicts which GoogleCalendarProxy can understand
    """
    def __init__(self, whuCourses):
        self.whuCoursesDictList = []

        info('info', 'digesting courses')
        for course in whuCourses:
            consumedSchedules = []

            for schedule in course:
                actualDate = self.getActualDate(int(schedule[STARTING_WEEK]), schedule[DAY])

                d = {
                    ACTUAL_START_TIME: self.getActualTime(actualDate, schedule[STARTING_CLASS_NUMBER], u'START'),
                    ACTUAL_END_TIME: self.getActualTime(actualDate, schedule[ENDING_CLASS_NUMBER], u'END'),
                    COUNT: int(schedule[ENDING_WEEK]) - int(schedule[STARTING_WEEK]) + 1,
                    FREQUENCY: schedule[FREQUENCY],
                    BYDAY: CourseRecurrence.DAYS_TO_ABBRS[schedule[DAY]],
                    WHERE: u'%s区, %s' % (
                        schedule[DISTRICT],
                        genLocationByCourseSchedule(schedule)
                    )
                }

                consumedSchedules.append(d)

            whuCourse = {
                COURSE_NAME: course.getProperty(COURSE_NAME),
                TEACHER_NAME: course.getProperty(TEACHER_NAME),
                SCHEDULE: consumedSchedules
            }
            self.whuCoursesDictList.append(whuCourse)
        info('info', '%s courses digested' % len(self.whuCoursesDictList))

        self.proxy = GoogleCalendarProxy(getAccountInfo(configs[CONFIG_KEY_GMAIL_ACCOUNT], GMAIL_PROMPT), getAccountInfo(configs[CONFIG_KEY_GMAIL_PWD], PASSWORD_PROMPT, True), THIS_CALENDAR_TIMEZONE, THIS_CALENDAR_LOCATION)


    def getActualDate(self, startingWeek, day):
        dayNumber = DAYS_TO_NUMS[day]
        delta = datetime.timedelta(days=((startingWeek - 1) * 7 + dayNumber))

        semesterStartingDate = datetime.date(SEMESTER_STARTING_DATE[0], SEMESTER_STARTING_DATE[1], SEMESTER_STARTING_DATE[2])
        return semesterStartingDate + delta


    def getActualTime(self, actualDate, clsNumber, flag):
        clsTime = {
            u'1': ((8, 0), (8, 45)),
            u'2': ((8, 50), (9, 35)),
            u'3': ((9, 50), (10, 35)),
            u'4': ((10, 40), (11, 25)),
            u'5': ((11, 30), (12, 15)),
            u'6': ((13, 15), (14, 0)),
            u'7': ((14, 5), (14, 50)),
            u'8': ((14, 55), (15, 40)),
            u'9': ((15, 45), (16, 30)),
            u'10': ((16, 40), (17, 25)),
            u'11': ((17, 30), (18, 15)),
            u'12': ((19, 0), (19, 45)),
            u'13': ((19, 50), (20, 35)),
            u'14': ((20, 40), (21, 25))
        }
        pattern = u'%Y%m%dT%H%M%S'
        flag = 0 if flag == u'START' else 1

        # 2012 2 13 is the date when this semester starts
        dateTime = datetime.datetime(
            actualDate.year,
            actualDate.month,
            actualDate.day,
            clsTime[clsNumber][flag][0],
            clsTime[clsNumber][flag][1]
        )

        return dateTime.strftime(pattern)


    def doInsert(self):
        for item in self.whuCoursesDictList:
            self.proxy.insertCourse(
                item[SCHEDULE],
                item[COURSE_NAME],
                item[TEACHER_NAME]
            )


if __name__ == '__main__':
    WhuGoogleCalendarAdapter(whu.readCourses(getAccountInfo(configs[CONFIG_KEY_STUDENT_ID], ID_PROMPT), getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD], PASSWORD_PROMPT, True))[1]).doInsert()

