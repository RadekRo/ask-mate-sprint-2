from datetime import datetime 

def get_current_date():
    date_and_time_without_seconds = str(datetime.now())[0:19]
    return date_and_time_without_seconds

