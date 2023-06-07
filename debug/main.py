from date_and_hour import date_and_time_now
def log(error , file):

    error =  f"""{date_and_time_now()} -      {repr(error)}\n"""
    with open(file, 'a', encoding='utf8') as log:
        log.write(error)
