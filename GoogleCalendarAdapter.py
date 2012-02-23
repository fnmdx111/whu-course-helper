# encoding: utf-8

# TODO make this script irrelevant to specific school


import atom
import datetime

import gdata
from const.constants import *
from mod.config import *
import gdata.calendar
import gdata.calendar.client
from mod import whu
from mod.fuf import getAccountInfo, genLocationByCourseSchedule


class GoogleCalendarAdapter(object):

    app_source = u'czh-WhuCourseHelper-%s' % VERSION

    def __init__(self, gmail_account, gmail_pwd):
        self.calendarClient = gdata.calendar.client.CalendarClient(source=GoogleCalendarAdapter.app_source)
        try:
            info('info', 'logging in as %s' % gmail_account)
            self.calendarClient.ClientLogin(gmail_account, gmail_pwd, self.calendarClient.source)

            for calendar in self.calendarClient.GetOwnCalendarsFeed().entry:
                if calendar.summary and calendar.summary.text == configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY]:
                    if configs[CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE]:
                        info('info', 'previously created calendar %s found, deleting' % calendar.title.text)
                        self.calendarClient.Delete(calendar.GetEditLink().href)
                        self.currentCalendar = self.calendarClient.InsertCalendar(new_calendar=self.genNewCalendar(
                            configs[CONFIG_KEY_THIS_CALENDAR_TITLE],
                            configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY],
                            configs[CONFIG_KEY_THIS_CALENDAR_COLOR],
                            THIS_CALENDAR_TIMEZONE,
                            THIS_CALENDAR_LOCATION
                        ))
                    else:
                        self.currentCalendar = calendar
                    break
            else:
                print 'title:', configs[CONFIG_KEY_THIS_CALENDAR_TITLE]
                self.currentCalendar = self.calendarClient.InsertCalendar(new_calendar=self.genNewCalendar(
                    configs[CONFIG_KEY_THIS_CALENDAR_TITLE],
                    configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY],
                    configs[CONFIG_KEY_THIS_CALENDAR_COLOR],
                    THIS_CALENDAR_TIMEZONE,
                    THIS_CALENDAR_LOCATION
                ))
            info('dbg', 'calendar id = %s' % self.currentCalendar.content.src)

        except gdata.client.RequestError as err:
            info('err', err)
            return

    def genNewCalendar(self, title, summary, color, timezone, location):
        new_calendar = gdata.calendar.data.CalendarEntry()
        new_calendar.title = atom.data.Title(text=title)
        new_calendar.summary = atom.data.Summary(text=summary)
        new_calendar.color = gdata.calendar.data.ColorProperty(value=color)
        new_calendar.timezone = gdata.calendar.data.TimeZoneProperty(value=timezone)
        new_calendar.where.append(gdata.calendar.data.CalendarWhere(value=location))
        new_calendar.selected = gdata.calendar.data.SelectedProperty(value='true')

        return new_calendar


    def insertCourse(self, course, title, content, echo=True):
        for schedule in course:
            event = gdata.calendar.data.CalendarEventEntry()

            event.title = atom.data.Title(text=title)
            event.content = atom.data.Content(text=content)
            event.where.append(gdata.data.Where(value=u'%s区, %s' % (
                                                    schedule[DISTRICT],
                                                    genLocationByCourseSchedule(schedule)
                                                )))

            event.recurrence = gdata.data.Recurrence(text=CourseRecurrence(schedule).recurrenceData)

            if echo:
                info('info', u'inserting %s %s at %s' % (title, content, event.where[0].value))
            self.calendarClient.InsertEvent(event, self.currentCalendar.content.src)


class CourseRecurrence(object):
    PATTERN = u'DTSTART;TZID=Asia/Shanghai:{dtstart}\n' \
              u'DTEND;TZID=Asia/Shanghai:{dtend}\n' \
              u'RRULE:FREQ=WEEKLY;COUNT={count};INTERVAL={freq};BYDAY={byday}\n' \
              u'BEGIN:VTIMEZONE\n' \
              u'TZID:Asia/Shanghai\n' \
              u'X-LIC-LOCATION:Asia/Shanghai\n' \
              u'BEGIN:STANDARD\n' \
              u'TZOFFSETFROM:+0800\n' \
              u'TZOFFSETTO:+0800\n' \
              u'TZNAME:CST\n' \
              u'DTSTART:19700101T000000\n' \
              u'END:STANDARD\n' \
              u'END:VTIMEZONE\n'

    DAYS_TO_ABBRS = {
        MONDAY: u'MO',
        TUESDAY: u'TU',
        WEDNESDAY: u'WE',
        THURSDAY: u'TH',
        FRIDAY: u'FR',
        SATURDAY: u'SA',
        SUNDAY: u'SU'
    }

    def __init__(self, schedule):
        date = self.getActualDate(
            int(schedule[STARTING_WEEK]),
            schedule[DAY]
        )
        data = {
            u'dtstart': self.getActualTime(date, schedule[STARTING_CLASS_NUMBER], u'START'),
            u'dtend': self.getActualTime(date, schedule[ENDING_CLASS_NUMBER], u'END'),
            u'count': int(schedule[ENDING_WEEK]) - int(schedule[STARTING_WEEK]) + 1,
            u'freq': schedule[FREQUENCY],
            u'byday': CourseRecurrence.DAYS_TO_ABBRS[schedule[DAY]]
        }
        self.recurrenceData = CourseRecurrence.PATTERN.format(**data)


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

    def __unicode__(self):
        return self.recurrenceData

    def __str__(self):
        return self.__unicode__().encode('utf-8')


def syncToGoogleCalendar():
    _, courses = whu.readCourses(getAccountInfo(configs[CONFIG_KEY_STUDENT_ID], ID_PROMPT), getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD], PASSWORD_PROMPT, True))

    adapter = GoogleCalendarAdapter(getAccountInfo(configs[CONFIG_KEY_GMAIL_ACCOUNT], GMAIL_PROMPT), getAccountInfo(configs[CONFIG_KEY_GMAIL_PWD], PASSWORD_PROMPT, True))

    for item in courses:
        adapter.insertCourse(
            item,
            item.getProperty(COURSE_NAME),
            item.getProperty(TEACHER_NAME)
        )

if __name__ == '__main__':
    try:
        syncToGoogleCalendar()
    except Exception as err:
        info('err', 'got fatal error: %s' % err )
        exit(0)
