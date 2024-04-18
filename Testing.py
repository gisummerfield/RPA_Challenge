from datetime import datetime
from dateutil.relativedelta import relativedelta


months = 6

def get_start_of_search_range(months):
    if months < 2:
        return datetime(datetime.now().year, datetime.now().month, 1)
    else:
        return datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(months=months-1)




