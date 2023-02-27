from datetime import datetime, timedelta


class MaxDaysRangeError(Exception):
    pass


def valid_date_query_param(date: str | None) -> bool:
    '''Check whether date is in YYYY-MM-DD format'''
    date_format = '%Y-%m-%d'
    if date is None:
        return False
    try:
        datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def date_ranges(start_date: str, end_date: str, days_range: int = 7, max_range: int = 35) -> list[tuple[str, str]]:
    '''
    Based on start_date and end_date in YYYY-MM-DD format generate date ranges specified by days_range parameter also in YYYY-MM-DD format

    If delta between dates is negative, dates are switched
    If delta between specified start and end date exceeds max_range parameter value MaxDaysRangeError exception is raised
    '''
    if (days_range < 1):
        raise ValueError('Only positive integers allowed')
    date_format = '%Y-%m-%d'
    start_datetime = datetime.strptime(start_date, date_format)
    end_datetime = datetime.strptime(end_date, date_format)
    delta = end_datetime - start_datetime
    delta_days = abs(delta.days)
    if (delta_days < 0):
        start_datetime, end_datetime = end_datetime, start_datetime
    if (abs(delta_days) > max_range):
        raise MaxDaysRangeError(
            'Maximum range of days for specified dates exceeded')
    elif delta_days == 0:
        return [(start_date, end_date)]
    days_ranges = [(i, min(i+days_range-1, delta_days))
                   for i in range(0, delta_days, days_range)]
    return [(datetime.strftime(start_datetime + timedelta(days=start), date_format), datetime.strftime(start_datetime + timedelta(days=end), date_format)) for start, end in days_ranges]


def parse_neos(nasa_api_resp: dict) -> list[dict]:
    # Output the list of the objects containing  the object name, size estimate, time and distance of the closest encounter.
    '''
    Parse needed information from nasa api response
    Raises KeyError error if well-known schema for parsing is broken
    '''
 #   total_count = nasa_api_resp['element_count']
    near_earth_objects = nasa_api_resp['near_earth_objects']
    parsed_neos = [{'name': entry['name'],
                    'estimated_diameter': entry['estimated_diameter'],
                    'close_approach_miss_distance': entry['close_approach_data'][0]['miss_distance'],
                    "close_approach_date_full": entry['close_approach_data'][0]['close_approach_date_full']}
                   for key in near_earth_objects.keys() for entry in near_earth_objects[key]]
    return parsed_neos
