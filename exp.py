from datetime import datetime


def farid():
    dat = str(datetime.today().strftime('%Y-%m-%d'))
    return dat

dat = farid()
print(dat)