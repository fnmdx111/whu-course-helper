# encoding: utf-8

from const.constants import *
from mod.config import *
import gdata.calendar
import gdata.calendar.client
import gdata.client
import gdata.calendar.data
import atom.data
import gdata.data
from mod.fuf import get_account_info, info, dbg, err


class GoogleCalendarProxy(object):

    app_source = u'czh-WhuCourseHelper-%s' % VERSION

    def __init__(self, calendar_timezone, calendar_location):
        gmail_account = get_account_info(configs[CONFIG_KEY_GMAIL_ACCOUNT],
                                         GMAIL_PROMPT)
        gmail_pwd = get_account_info(configs[CONFIG_KEY_GMAIL_PWD],
                                     PASSWORD_PROMPT,
                                     True)

        self.client = gdata.calendar.client.CalendarClient(
            source=GoogleCalendarProxy.app_source
        )

        try:
            info('logging in as %s' % gmail_account)
            self.client.ClientLogin(gmail_account, gmail_pwd,
                                    self.client.source)

            for calendar in self.client.GetOwnCalendarsFeed().entry:
                if calendar.summary and\
                   calendar.summary.text == configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY]:
                    if configs[CONFIG_KEY_IF_THIS_CALENDAR_FOUND_THEN_PERFORM_DELETE]:
                        info('previously created calendar %s found,'
                             'deleting' % calendar.title.text)
                        self.client.Delete(calendar.GetEditLink().href)
                        self.current_calendar = self.client.InsertCalendar(
                            new_calendar=self.gen_calender(
                                configs[CONFIG_KEY_THIS_CALENDAR_TITLE],
                                configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY],
                                configs[CONFIG_KEY_THIS_CALENDAR_COLOR],
                                calendar_timezone,
                                calendar_location
                            )
                        )
                    else:
                        self.current_calendar = calendar
                    break
            else:
                self.current_calendar = self.client.InsertCalendar(
                    new_calendar=self.gen_calender(
                        configs[CONFIG_KEY_THIS_CALENDAR_TITLE],
                        configs[CONFIG_KEY_THIS_CALENDAR_SUMMARY],
                        configs[CONFIG_KEY_THIS_CALENDAR_COLOR],
                        calendar_timezone,
                        calendar_location
                    )
                )
            dbg('calendar id = %s' % self.current_calendar.content.src)

        except gdata.client.RequestError as e:
            err(e)
            return

    def gen_calender(self, title, summary, color, timezone, location):
        new_calendar = gdata.calendar.data.CalendarEntry()
        new_calendar.title = atom.data.Title(text=title)
        new_calendar.summary = atom.data.Summary(text=summary)
        new_calendar.color = gdata.calendar.data.ColorProperty(value=color)
        new_calendar.timezone = gdata.calendar.data.TimeZoneProperty(value=timezone)
        new_calendar.where.append(gdata.calendar.data.CalendarWhere(value=location))
        new_calendar.selected = gdata.calendar.data.SelectedProperty(value='true')

        return new_calendar


    def insert(self, schedules, title, content, echo=True):
        for schedule in schedules:
            event = gdata.calendar.data.CalendarEventEntry()

            event.title = atom.data.Title(text=title)
            event.content = atom.data.Content(text=content)
            event.where.append(gdata.data.Where(value=schedule[WHERE]))

            event.recurrence = gdata.data.Recurrence(
                text=CourseRecurrence(schedule).recurrence_text
            )

            if echo:
                info('inserting %s %s at %s' % (title, content,
                                                event.where[0].value))
            self.client.InsertEvent(event, self.current_calendar.content.src)

    def insert_day(self, schedules, echo=True):
        for schedule in schedules:
            event = gdata.calendar.data.CalendarEventEntry()
            event.title = atom.data.Title(text=schedule['title'])
            event.when.append(gdata.calendar.data.When
                              (start=schedule['start_date'], end=schedule['end_date']))

            if echo:
                info('inserting %s at %s to %s' % (schedule['title'],
                                                   schedule['start_date'], schedule['end_date']))
            self.client.InsertEvent(event, self.current_calendar.content.src)


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
        self.recurrence_text = CourseRecurrence.PATTERN.format(**data)


    def __unicode__(self):
        return self.recurrence_text


    def __str__(self):
        return self.__unicode__().encode('utf-8')


