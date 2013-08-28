# encoding: utf-8

"""
    fuf ::= frequently used functions
"""
import getpass


def get_account_info(variable, prompt, pwd=False):
    if variable == '':
        if pwd:
            if switch['dbg']:
                return raw_input(prompt)
            else:
                return getpass.getpass(prompt)
        else:
            return raw_input(prompt)

    return variable


switch = {
    'info': True,
    'dbg': False,
    'err': True,
    'verbose': True
}

def log(level, msg):
    if switch[level]:
        print '%s: %s' % (level, msg)


def info(msg):
    log('info', msg)


def dbg(msg):
    log('dbg', msg)


def verbose(msg):
    log('verbose', msg)


def err(msg):
    log('err', msg)

