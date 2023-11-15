from datetime import datetime
from Utils.Log import Log


class TimeUtils:

    @staticmethod
    def calc_time_diff(s1, s2, fmt='%H:%M:%S'):
        delta = datetime.strptime(s2, fmt) - datetime.strptime(s1, fmt)
        return delta.seconds / 60

    @staticmethod
    def compare_time_to_now(time_str, fmt='%H:%M:%S'):
        module = 'compare_time_to_now'
        now = datetime.now()
        # t1 = datetime.strptime(now.strftime(fmt), fmt)
        # t2 = datetime.strptime(time_str, fmt)
        delta = datetime.strptime(now.strftime(fmt), fmt) - datetime.strptime(time_str, fmt)
        result = 'AFTER' if delta.days >= 0 else 'BEFORE'
        Log.print('L1', module, 'compare {} to {} -> {}'.format(now, time_str, result))
        return result

    @staticmethod
    def is_within_start_and_end_time(start_time_str, start_fmt, end_time_str, end_fmt):
        module = 'is_within_start_and_end_time'
        before_or_after_start = TimeUtils.compare_time_to_now(start_time_str, start_fmt)
        is_within = False
        if before_or_after_start == 'AFTER':
            before_or_after_end = TimeUtils.compare_time_to_now(end_time_str, end_fmt)
            if before_or_after_end == 'BEFORE':
                is_within = True
        Log.print('L1', module, 'Within is {}'.format(is_within))
        return is_within

    @staticmethod
    def is_this_year(dt):
        now = datetime.now()
        return now.year == dt.year

    @staticmethod
    def is_last_year(dt):
        now = datetime.now()
        return dt.year == (now.year - 1)
