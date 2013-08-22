# encoding: utf-8
from mod.config import configs, CONFIG_KEY_STUDENT_ID, CONFIG_KEY_STUDENT_PWD, read_configs
from const.constants import ID_PROMPT, PASSWORD_PROMPT
from mod.fuf import get_account_info
from schools.whu import whu
from schools.whu.calender_adapter import WhuGoogleCalendarAdapter

if __name__ == '__main__':
    read_configs()
    _, courses = whu.read_courses(get_account_info(configs[CONFIG_KEY_STUDENT_ID],
                                                   ID_PROMPT),
                                  get_account_info(configs[CONFIG_KEY_STUDENT_PWD],
                                                   PASSWORD_PROMPT,
                                                   True))
    WhuGoogleCalendarAdapter(courses).do_insertion()


