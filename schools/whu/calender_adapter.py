# encoding: utf-8

import __init__
import datetime
from mod.google_calendar_proxy import *
from mod.fuf import get_account_info, info
from schools.whu import whu
from schools.whu.constants import *
from schools.whu.parsers import gen_location_by_schedule


class WhuGoogleCalendarAdapter(object):

    """
        this adapter consumes courses of whu,
        and excrete dicts which GoogleCalendarProxy can understand
    """
    def __init__(self, courses):
        self.courses = []

        info('digesting courses')
        for course in courses:
            schedules = []

            for schedule in course:
                if not schedule:
                    continue

                actual_date = self.get_actual_date(int(schedule[STARTING_WEEK]),
                                                   schedule[DAY])

                d = {
                    ACTUAL_START_TIME:
                        self.get_actual_time(actual_date,
                                             schedule[STARTING_CLASS_NUMBER],
                                             'START'),
                    ACTUAL_END_TIME:
                        self.get_actual_time(actual_date,
                                             schedule[ENDING_CLASS_NUMBER],
                                             'END'),
                    COUNT:
                        int(schedule[ENDING_WEEK]) -\
                        int(schedule[STARTING_WEEK]) + 1,
                    FREQUENCY:
                        schedule[FREQUENCY],
                    BYDAY:
                        CourseRecurrence.DAYS_TO_ABBRS[schedule[DAY]],
                    WHERE:
                        u'%s区, %s' % (schedule[DISTRICT],
                                       gen_location_by_schedule(schedule))
                }

                schedules.append(d)

            course = {
                COURSE_NAME: course.property(COURSE_NAME),
                TEACHER_NAME: course.property(TEACHER_NAME),
                SCHEDULE: schedules
            }
            self.courses.append(course)
        info('%s courses digested' % len(self.courses))

        self.proxy = GoogleCalendarProxy(THIS_CALENDAR_TIMEZONE,
                                         THIS_CALENDAR_LOCATION)


    def get_actual_date(self, startingWeek, day):
        day_number = DAYS_TO_NUMS[day]
        delta = datetime.timedelta(days=((startingWeek - 1) * 7 + day_number))

        semester_starting_date = datetime.date(SEMESTER_STARTING_DATE[0],
                                               SEMESTER_STARTING_DATE[1],
                                               SEMESTER_STARTING_DATE[2])
        return semester_starting_date + delta


    def get_actual_time(self, actual_date, cls_number, flag):
        cls_time = {
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
        date_time = datetime.datetime(
            actual_date.year,
            actual_date.month,
            actual_date.day,
            cls_time[cls_number][flag][0],
            cls_time[cls_number][flag][1]
        )

        return date_time.strftime(pattern)


    def do_insertion(self):
        for item in self.courses:
            self.proxy.insert(
                item[SCHEDULE],
                item[COURSE_NAME],
                item[TEACHER_NAME]
            )


if __name__ == '__main__':
    _, courses = whu.read_courses(
        get_account_info(configs[CONFIG_KEY_STUDENT_ID],
                         ID_PROMPT),
        get_account_info(configs[CONFIG_KEY_STUDENT_PWD],
                         PASSWORD_PROMPT,
                         True)
    )
    WhuGoogleCalendarAdapter(courses).do_insertion()

