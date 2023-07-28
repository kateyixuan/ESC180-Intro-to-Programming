def initialize():
    global cur_balance_owing_intst, cur_balance_owing_recent # cur_balance_owing_intst records the balance
                                                             # of money owed that is collecting interest.
                                                             # cur_balance_owed_recent records the balance of
                                                             # monthly purchases. The amount stored in
                                                             # this variable gets put inside cur_balance_owed
                                                             # _intst every month and resets to 0.

    global last_update_day, last_update_month # last_update_day is the day of the most recent past purchase
                                              # last_updaye_month is the month of the most recent purchase
    global last_country, last_country2 # last_country is the country where the most recent purchase was made
                                       # last_country2 is the country where the next most recent purchase was
                                       # made (the country before last_country)

    global deactivate_card # Is True when the card is deactivated and is False if card is not deactivated
    deactivate_card = False

    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0

    last_update_day, last_update_month = -1, -1

    last_country = None
    last_country2 = None

    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    '''Compare the last updated date to test the day and month of the action to see if it is possible (cannot have an action be done from the past). Return True if date of action, day 1, is same or later than the last updated date, day 2 '''
    if day1 >= day2 and month1 >= month2:
        return True
    elif day1 < day2 and month1 > month2:
        return True
    else:
        return False


def all_three_different(c1, c2, c3):
    '''Test whether all three countries are different. Return True if purchases are made in three different countries, False otherwise. Assign the variable deactivate_card as True or False. '''
    global deactivate_card
    if deactivate_card == True:
        return True
    elif c1 == None or c2 == None or c3 == None:
        deactivate_card = False
        return False
    elif c1 != c2 and c2 != c3 and c1 != c3:
        deactivate_card = True
        return True
    else:
        deactivate_card = False
        return False


def purchase(amount, day, month, country):
    '''Store amount of purchase in recent balance (cur_balance_owing_recent) or interest balance (cur_balance_owing_intst)depending on the date of purchase. Day and month is the date of purchase and country is the location of the purchase, used to determine whether or not the card should be deactivated. Return "error" if card is deactivated.   '''
    global last_update_day, last_update_month
    global last_country, last_country2
    global cur_balance_owing_recent, cur_balance_owing_intst

    all_three_different(country, last_country, last_country2)

    if date_same_or_later(day, month, last_update_day, last_update_month) == True and deactivate_card == False:
        if last_update_month == -1 or month == last_update_month:
            cur_balance_owing_recent += amount # No interest is added since it is in the same month.
        elif last_update_month + 1 == month: # Move recent balance in balance collecting interest since it is
                                             # after a month. Interest is added to the interest balance but
                                             # does not collect interest until a month later (2 months after
                                             # purchase).
            cur_balance_owing_intst = cur_balance_owing_recent + (cur_balance_owing_intst * 1.05)
            cur_balance_owing_recent = amount
        elif last_update_month < month: # If there is a long period of time from last updated month and
                                        # purchase, interest still collects over the period of time you were
                                        # inactive on the balance inside recent balance (that is not updated
                                        # unless you make a purchase) and the interest balance.
            cur_balance_owing_intst = (cur_balance_owing_recent * (1.05 ** (month -  last_update_month -1))) + (cur_balance_owing_intst * (1.05 **(month -  last_update_month)))  # subtract 1 because it does not include
                                                                     # the month of this action.
            cur_balance_owing_recent = amount

        last_update_day = day        # Update the most recent date, month and country
        last_update_month = month
        last_country2 = last_country
        last_country = country

    if deactivate_card == True:
        return "error"

def amount_owed(day, month):
    '''Return amount owed, stored in recent balance and interest balance. Return error if the date is before the last updated date. Day and month is the date of the action. '''
    global last_update_day, last_update_month
    global last_country, last_country2
    global cur_balance_owing_recent, cur_balance_owing_intst

    if date_same_or_later(day, month, last_update_day, last_update_month) == True:
        if last_update_month == month: # no interest is applied since it is the same month therefore there is
                                       # no action under this condition except for updating the date.
            last_update_day = day
            last_update_month = month
            return cur_balance_owing_intst + cur_balance_owing_recent
        elif last_update_month + 1 == month:  # Since it has only been a month, interest is only applied to
                                              # the balance already collecting interest and not the recent
                                              # balance. However, the recent balance is moved into interest
                                              # balance.
            cur_balance_owing_intst = (cur_balance_owing_intst * 1.05) + cur_balance_owing_recent
            cur_balance_owing_recent = 0
            last_update_day = day
            last_update_month = month
            return cur_balance_owing_intst + cur_balance_owing_recent
        elif last_update_month < month: # Apply interest on balance collecting interest and also to the
                                        # recent balance (which is moved into the interest balance, which is
                                        # why recent balance resets to 0)
            cur_balance_owing_intst = (cur_balance_owing_intst * (1.05)) + cur_balance_owing_recent
            cur_balance_owing_recent = 0
            cur_balance_owing_intst *= 1.05**(month - last_update_month - 1) # Subtract 1 because it does not
                                                                             # include the month you are
                                                                             # making the purchase.
            last_update_day = day
            last_update_month = month
            return cur_balance_owing_intst + cur_balance_owing_recent
    else:
        return "error"



def pay_bill(amount, day, month):
    '''Compute bill payments and return the recent balance and the interest balance. Return "error" if date is before last updated date. '''
    global last_update_day, last_update_month
    global last_country, last_country2
    global cur_balance_owing_recent, cur_balance_owing_intst


    if date_same_or_later(day, month, last_update_day, last_update_month) == True: # Check date of action to
                                                                                   # apply the correct amount
                                                                                   # interest before bill is
                                                                                   # payed.
        if last_update_month == month:
            last_update_day = day
            last_update_month = month
        elif last_update_month + 1 == month:
            cur_balance_owing_intst = (cur_balance_owing_intst * 1.05) + cur_balance_owing_recent
            cur_balance_owing_recent = 0
            last_update_day = day
            last_update_month = month
        elif last_update_month < month:
            cur_balance_owing_intst = (cur_balance_owing_intst * (1.05)) + cur_balance_owing_recent
            cur_balance_owing_recent = 0
            cur_balance_owing_intst *= 1.05**(month - last_update_month - 1)
            last_update_day = day
            last_update_month = month


        if amount <= (cur_balance_owing_intst + cur_balance_owing_recent): # Change the balance owed by
                                                                           # subtracting the amount payed to
                                                                           # both the recent and interest
                                                                           # balance. Subtract from interest
                                                                           # balance first, then if there is
                                                                           # money left over, then subtract
                                                                           # from recent balance.
            if cur_balance_owing_intst == 0:
                cur_balance_owing_recent -= amount
            elif cur_balance_owing_intst != 0:
                cur_balance_owing_intst = cur_balance_owing_intst - amount
                if cur_balance_owing_intst <= 0:
                    cur_balance_owing_recent += cur_balance_owing_intst
                    cur_balance_owing_intst = 0
            elif cur_balance_owing_recent != 0:
                cur_balance_owing_intst -= amount
                amount -= cur_balance_owing_intst
        else:
            return "error"
    else:
        return "error"

        last_update_day = day
        last_update_month = month
        return cur_balance_owing_intst, cur_balance_owing_recent


# Initialize all global variables outside the main block.
initialize()

if __name__ == '__main__':
    # Test base of purchase and pay_bill with interest
    initialize()
    purchase(200, 3, 5, "Canada")
    purchase(200, 4, 5, "China")
    purchase(200, 5, 6, "Canada") # 600
    pay_bill(200, 5, 7) # ((400)*1.05)+200) - 200 = 420
    print("Now owing:", amount_owed(5, 8)) # (220 * 1.05) + (200*1.05) = 441.0

    # Test for card deactivation error
    initialize()
    purchase(30, 4, 4, "France")
    purchase(10000, 2, 6, "Australia") # 30 + 10000 = 10030
    purchase(500, 4, 6, "Canada") #error still 10030
    purchase(300, 3, 7, "Canada") #error
    print("Now owing:", amount_owed(3, 7)) # (30*1.05**2) + (10000*1.05) = 10033.075

    # Large time increments between actions
    initialize()
    purchase(500, 1, 2, "Canada")
    print("Now owing", amount_owed(2, 7)) # 500*1.05**4 = 607.753125
    purchase(500, 1, 8, "China") # 500*1.05^5 + 500 = 1138.14078125
    print("Now owing:", amount_owed(30, 11)) # 500*1.05^8 + 500*1.05^2 = 1289.97772189
    print("Now owing", amount_owed(30, 12)) # 500*1.05^9 + 500*1.05^3 = 1354.47660799

    # Paying off debt fully including interest
    initialize()
    purchase(100, 3, 2, "Canada")
    pay_bill(110.25, 3, 5) # 100*1.05**2 - 110.25 = 0
    print("Now owing:", amount_owed(3, 6)) # 0.0

    # Paying off debt partially with purchases, error, and large time increments
    initialize()
    purchase(30, 1, 1, "Canada")
    purchase(30, 2, 8, "India") # (30*1.05**6) + 30 = 70.2028692188
    purchase(50, 3, 8, "United States") #error 70.2028692188
    print("Now owing:", amount_owed(3, 8))# 70.2028692188
    pay_bill(60, 3, 12) # (30*1.05**10) + (30*1.05**3) = 83.5955888033 - 60 = 23.5955888033
    print("Now owing:", amount_owed(3, 12)) # 23.5955888033
    purchase(30, 4, 12, "United States") # card is still deactivated and cannot purchase
    print("Now owing:", amount_owed(4, 12)) # 23.5955888033

    # Paying off debt fully with more purchases after
    initialize()
    purchase(10, 1, 2, "Canada")
    purchase(10, 2, 4, "Brazil") # (10*1.05) + 10 = 20.5
    print("Now owing:", amount_owed(2, 4)) # 20.5
    pay_bill(20.5, 3, 4) # 0.0
    purchase(30, 5, 4, "Canada") # 30
    print("Now owing:", amount_owed(5, 4)) #30

    # Paying off debt more than once
    initialize()
    purchase(30, 1, 2, "Canada")
    purchase(30, 2, 5, "Italy") # (30*1.05**2) + 30 = 63.075
    print("Now owing:", amount_owed(2, 5)) # 63.075
    pay_bill(30, 3, 5) # 30*1.05^2 + 30 = 63.075 - 30 = 33.075
    purchase(30, 5, 6, "Canada") # 3.075*1.05 + 30 + 30
    print("Now owing:", amount_owed(5, 7)) # 3.075*1.05^2 + 30*1.05 + 30 = 64.8901875

