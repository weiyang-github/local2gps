# encoding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import socket
import struct
import time
from datetime import datetime, timedelta
import exceptions
import colorama
import logging
import argparse

console_level_fore_color_tab = {
    'debug': colorama.Fore.RESET,
    'info' : colorama.Fore.GREEN,
    'warning': colorama.Fore.YELLOW,
    'error': colorama.Fore.RED
}

def user_logger_creat(name=None, format=None, filename=None):
    """
    creat the logging object.
    """
    # Default log format
    LOG_FORMAT_STRING = "%(asctime)s.%(msecs)03d %(name)s %(module)-8s %(levelname)-8s %(message)s"

    if format:
        LOG_FORMAT_STRING = format
    
    if name:
        log_fn = name + '.log'
    else:
        log_fn = 'root.log'

    if filename:
        log_fn = filename

    # setup root logger object
    # logging.basicConfig(format=LOG_FORMAT_STRING, datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stdout, level=logging.DEBUG)

    # get logger object, if name is undefined, the object is root
    logger_obj = logging.getLogger(name=name)

    logger_formatter = logging.Formatter(fmt=LOG_FORMAT_STRING, datefmt='%Y-%m-%d %H:%M:%S')

    # set logger handle.
    logger_handle1 = logging.FileHandler(log_fn, mode='a')
    logger_handle1.setFormatter(logger_formatter)
    logger_handle1.setLevel(logging.INFO)
    logger_obj.addHandler(logger_handle1)

    logger_handle2 = logging.StreamHandler(stream=sys.stdout)
    logger_handle2.setFormatter(logger_formatter)
    logger_handle2.setLevel(logging.DEBUG)
    logger_obj.addHandler(logger_handle2)

    logger_obj.setLevel(logging.DEBUG)

    return logger_obj


def console_print(level, msg, fore_col=None):
    col = console_level_fore_color_tab.get(level, colorama.Fore.RED)
    if fore_col:
        col = fore_col
    print col + msg + colorama.Style.RESET_ALL


def arg_parse_setup(args=None):
    Version = '0.0.1'
    epi = """When the time zone is negative, you need to add a space 
    before '-' and use quotes marks, such as ' -8:00'
"""
    parser = argparse.ArgumentParser(description='convert local time to gps time', epilog=epi)
    parser.add_argument('-v','--version', action='version', version=Version)
    parser.add_argument('-z', '--zone', metavar='[+/-]HH:MM', dest='zone', default=None, help="local time zone, default value is +08:00")
    parser.add_argument("-p", dest='leaps', default=None, help="leap senconds since gps epoch, default value is 13s since 2000")
    # parser.add_argument("local_time", default=None, help="local time to convert")
    parser.add_argument("local_time", metavar="Y-m-d H:M:S", nargs='?', default=None, help="local time to convert. if not exit, the system current time will be taken")

    if args:
        return parser.parse_args(args.split())
    else:
        return parser.parse_args()

def time_zone_parse(tz):
    tz_sec = 0
    try:
        [hour, min] = tz.split(':')
        hour = int(hour)
        min = int(min)
        if min < 0 or min > 59: 
            return False, 0
        if hour < 0:
            tz_sec = hour * 3600 - min * 60
        else:
            tz_sec = hour * 3600 + min * 60
        return True, tz_sec
    except Exception as e:
        return False, 0

def leap_second_parse(ls):
    lp_sec = 0
    try:
        lp_sec = int(ls)
        return True, lp_sec
    except Exception as e:
        return False, 0
    
def main():
    args = arg_parse_setup()
    # LOG = user_logger_creat(name='local2gps', format="%(asctime)s.%(msecs)03d %(module)-8s %(levelname)-8s %(message)s")

    leap_seconds = 13
    time_zone = 8*3600
    gps_epoch = datetime(1980,1,6,0,0,0)



    if args.zone: 
        tz_ok, tz_val = time_zone_parse(args.zone)
        if tz_ok:
            time_zone = tz_val
            # print time_zone
        else:
            console_print('error', 'time zone foramt is error') 
            return
    
    if args.leaps:
        ls_ok, ls_val = leap_second_parse(args.leaps)
        if ls_ok:
            leap_seconds =  ls_val
            # print leap_seconds
        else:
            console_print('error', 'leap seconds foramt is error')
            return
    
    if args.local_time:
        try:
            lt = datetime.strptime(args.local_time, '%Y-%m-%d %H:%M:%S')
            utc = lt - timedelta(seconds=time_zone)
        except Exception as e:
            console_print('error', 'local time foramt is error')
            return
    else:
        utc_now = datetime.utcnow()
        utc_now_str = utc_now.strftime('%Y-%m-%d %H:%M:%S') # 忽略毫秒
        utc = datetime.strptime(utc_now_str, '%Y-%m-%d %H:%M:%S')


    if utc < gps_epoch:
        console_print('error', 'local time can not convert')
        return
    
    dt_interval = utc - gps_epoch
    sec_interval = dt_interval.total_seconds() # 第一种方法
    gps_time = sec_interval  + leap_seconds
    # sec_interval = dt_interval.days * 3600 * 24 + dt_interval.seconds #第二种方法

    print "UTC: ", utc.strftime("%Y-%m-%d %H:%M:%S")
    print "GPS: ", int(gps_time)

if __name__ == '__main__':
    main()
    