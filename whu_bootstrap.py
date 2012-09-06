from mod.config import configs, CONFIG_KEY_STUDENT_ID, CONFIG_KEY_STUDENT_PWD, readConfig
from const.constants import ID_PROMPT, PASSWORD_PROMPT
from mod.fuf import getAccountInfo
from schools.whu import whu
from schools.whu.CalendarAdapter import WhuGoogleCalendarAdapter

if __name__ == '__main__':
    readConfig()
    WhuGoogleCalendarAdapter(
        whu.readCourses(getAccountInfo(configs[CONFIG_KEY_STUDENT_ID],
                                       ID_PROMPT),
                        getAccountInfo(configs[CONFIG_KEY_STUDENT_PWD],
                                       PASSWORD_PROMPT,
                                       True))[1]
    ).doInsert()


