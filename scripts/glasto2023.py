#!/usr/bin/env python3

import time
import glasto as gl

# incognito??
incognito = True

# disable js??
disablejs = False

# disable images for faster loading?
disableimages=True

# change cache size?
cache=4096

# try a proxy with "8.8.8.8:88"
proxy=None

# run without browser - kind of pointless but faster.
headless=False

# refresh rate - seconds
refreshrate = 0.0001

# try one of these URLS
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-deposits/worthy-farm/1300000"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/addregistrations"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023/worthy-farm/1300001"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-ticket-coach-travel-deposits/worthy-farm/1450012"
# DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-ticket-coach-travel/worthy-farm/2500011"
DEPOSIT_23_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-deposits/worthy-farm/2500011"

PHRASES_TO_CHECK = [
    "enter the registration number",
    "postcode for each person"
    "registration details"
]

# first is lead booker
# Group 6
REG_DETAILS=[
    {
        'number': "1343715140", 
        'postcode': "NW6 4LD"
    },
    {
        'number': "3046662564", 
        'postcode': "B75 6RR"
    },
    {
        'number': "3363253908", 
        'postcode': "BA2 8TY"
    },
    {
        'number': "2786673517", 
        'postcode': "HA8 5SY"
    },
    {
        'number': "3809560973", 
        'postcode': "NW1 9EX"
    },
]

# Group 3
# REG_DETAILS=[
#     {
#         'number': "442257501", 
#         'postcode': "SE22 9JU"
#     },
#     {
#         'number': "3269539459", 
#         'postcode': "SE22 0PU"
#     },
#     {
#         'number': "1709972710", 
#         'postcode': "CV5 8EN"
#     },
#     {
#         'number': "2988532062", 
#         'postcode': "SE15 4RB"
#     },
#     {
#         'number': "3278389915", 
#         'postcode': "CB4 1JQ"
#     },
#     {
#         'number': "2547218061", 
#         'postcode': "SK6 7GY"
#     },
# ]

if len(REG_DETAILS) == 0:
    raise RuntimeError(
        "Must have at least one registration!")

if len(REG_DETAILS) > 6:
    raise RuntimeError(
        "Cannot accept more than 1 + 5 registration details!")

def attemptconnection(client, url):
    if client.establishconnection(url, phrases_to_check=PHRASES_TO_CHECK):
        print("success")
        print(client.attempts)
        try:
            gl.tofile(client.content, "reg_page_2023.html")
        except:
            pass
        if client.submit_registration(REG_DETAILS):
            print("Registration details submission success!")
            # save the html data
            try:
                gl.tofile(client.content, "reg_check_2023.html")
            except:
                pass

            try:
                # then click 'confirm' button and save html data again
                client.clickbutton('Confirm')
                gl.tofile(client.pagesource, "payment_page_2023.html")
            except:
                pass

            # we cannot go beyond this automated, 
            # since entering credit cards details automatically
            # is terribly risky.
            # instead leave the page open for us to do that
            # and save the content

            # todo: ????
            return
        else:
            print("Registration details submission failed!")

    # try again??
    # attemptconnection(client, url)

# main
s = gl.Service(gl.DRIVER_PATH)
c = gl.Twenty23(s, timeout=4, refreshrate=refreshrate, verbose=False, 
    disablejs=disablejs, incognito=incognito, disableimages=disableimages, 
    cache=cache, headless=headless, proxy=proxy)
attemptconnection(c, DEPOSIT_23_URL)

# backup sleep 
time.sleep(1500000) # Hack - leave it open to fill in details