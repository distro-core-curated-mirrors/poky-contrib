from datetime import date

def past(monthsago):
    """ Get the isotime 'months' ago"""

    today = date.today()
    year, month, day = today.year, today.month, today.day

    # all cases older that 11 months, just take those from last year
    if monthsago > 11:
        return date(year-1, month, day).isoformat()
    
    deltamonths = month - monthsago
    if deltamonths <= 0:
        year -= 1
        month = 12 + deltamonths
    else:
        month -= monthsago
    
    return date(year, month, day).isoformat()
