# encoding: utf-8


import atom

import gdata
from const.constants import *
from mod.config import *
import gdata.calendar
import gdata.calendar.client


class GoogleCalendarProxy(object):

    app_source = u'czh-WhuCourseHelper-%s' % VERSION

    def __init__(self, gmail_account, gmail_pwd, calendar_timezone, calendar_location):
        self.calendarClient = gdata.calendar.client.CalendarClient(source=GoogleCalendarProxy.app_source)
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
                            calendar_timezone,
                            calendar_location
                        ))
                    else:
                        self.currentCalendar = calendar
                    break
            else:
                self.currentCalendar = self.calendarClient.InsertCalendar(new_calendar=self.genNewCalendar(
                    configs[CONFIG_KEY_THIS_CALENDAR_TITLE],
                    configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY],
                    configs[CONFIG_KEY_THIS_CALENDAR_COLOR],
                    calendar_timezone,
                    calendar_location
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


    def insertCourse(self, schedules, title, content, echo=True):
        for schedule in schedules:
            event = gdata.calendar.data.CalendarEventEntry()

            event.title = atom.data.Title(text=title)
            event.content = atom.data.Content(text=content)
            event.where.append(gdata.data.Where(value=schedule[WHERE]))

            event.recurrence = gdata.data.Recurrence(text=CourseRecurrence(schedule).recurrenceData)

            if echo:
                info('info', u'inserting %s %s at %s' % (title, content, event.where[0].value))
            self.calendarClient.InsertEvent(event, self.currentCalendar.content.src)


class CourseRecurrence(object):
    PATTERN = u'DTSTART;TZID=Asia/Shanghai:{dtstart}\n'\
              u'DTEND;TZID=Asia/Shanghai:{dtend}\n'\
              u'RRULE:FREQ=WEEKLY;COUNT={count};INTERVAL={freq};BYDAY={byday}\n'\
              u'BEGIN:VTIMEZONE\n'\
              u'TZID:Asia/Shanghai\n'\
              u'X-LIC-LOCATION:Asia/Shanghai\n'\
              u'BEGIN:STANDARD\n'\
              u'TZOFFSETFROM:+0800\n'\
              u'TZOFFSETTO:+0800\n'\
              u'TZNAME:CST\n'\
              u'DTSTART:19700101T000000\n'\
              u'END:STANDARD\n'\
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
        """
            schedule passed to __init__ should be a dict which contains following keys:
                actual_start_time: a date object
                actual_end_time: a date object
                count: int
                frequency: int
                day: day constant defined in dict_keys.py
                where: unicode object
        """
        data = {
            u'dtstart': schedule[ACTUAL_START_TIME],
            u'dtend': schedule[ACTUAL_END_TIME],
            u'count': schedule[COUNT],
            u'freq': schedule[FREQUENCY],
            u'byday': schedule[BYDAY]
        }
        self.recurrenceData = CourseRecurrence.PATTERN.format(**data)


    def __unicode__(self):
        return self.recurrenceData


    def __str__(self):
        return self.__unicode__().encode('utf-8')


