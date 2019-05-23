from dateutil.relativedelta import relativedelta
import datetime


class DayCount:

    '''DayCount class. Counts days
    for different day count conventions
    as a fraction of year
    '''

    @classmethod
    def count_days(cls, date_start=None, date_end=None, day_count=None):

        '''Counts days as a fraction of year
        for act/360 or act/act day count conventions.
        Other day count conventions may be added later
        '''

        if date_start is None or date_end is None:
            raise ValueError("###Input date_start and date_end in datetime format###")
        if day_count is None:
            raise ValueError("###Input day count convention###")
        if date_end < date_start:
            raise ValueError("###date_end must be greater than or equal to date_start###")
        if day_count == 'act/360':
            t_years = cls.count_days_act_360(date_start, date_end)
            return t_years
        elif day_count == 'act/act':
            t_years = cls.count_days_act_act(date_start, date_end)
            return t_years
        else:
            raise ValueError("###day_count must be either 'act/360' or 'act/act'###")
            return t_years

    @classmethod
    def count_days_act_360(cls, date_start, date_end):

        '''Counts days as a fraction of year
        for act/360 day count convention
        '''

        t_years = (date_end - date_start).days / 360
        return t_years

    @classmethod
    def count_days_act_act(cls, date_start, date_end):

        '''Counts days as a fraction of year
        for act/act day count convention
        '''

        t_years = 0
        year_start = date_start.year
        year_end = date_end.year
        if year_end == year_start:
            t_years += (date_end - date_start).days / cls.year_days(year_end)
        else:
            t_years += (date_end - datetime.datetime(year_end-1, 12, 31)).days
            t_years /= cls.year_days(year_end)
            year_end -= 1
            while year_end > year_start:
                date_end_temp = datetime.datetime(year_end, 12, 31)
                date_start_temp = datetime.datetime(year_end-1, 12, 31)
                t_years += (date_end_temp - date_start_temp).days / cls.year_days(year_end)
                year_end -= 1
            date_end_temp = datetime.datetime(year_end, 12, 31)
            t_years += (date_end_temp - date_start).days / cls.year_days(year_end)
        return t_years

    @classmethod
    def year_days(cls, year):

        '''Counts the number of days in a year
        '''

        year_days = (datetime.datetime(year, 12, 31) - datetime.datetime(year-1, 12, 31)).days
        return year_days
