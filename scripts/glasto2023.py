#!/usr/bin/env python3

import time
import glasto as gl

# incognito??
incognito = False

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
DEPOSIT_23_URL = "https://glastonbury.seetickets.com/event/glastonbury-2023-deposits/worthy-farm/2500000"

PHRASES_TO_CHECK = [
    "enter the registration number",
    "postcode for each person"
    "registration details"
]

# first is lead booker
# Group 7
REG_DETAILS=[
    {
        'number': "123123123", 
        'postcode': "A1 4AB"
    },
    {
        'number': "123123123", 
        'postcode': "A1 4AB"
    },
    {
        'number': "123123123", 
        'postcode': "A1 4AB"
    },
    {
        'number': "123123123", 
        'postcode': "A1 4AB"
    },
    {
        'number': "123123123", 
        'postcode': "A1 4AB"
    },
]

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
print(DEPOSIT_23_URL)
s = gl.Service(gl.DRIVER_PATH)
c = gl.Twenty23(s, timeout=4, refreshrate=refreshrate, verbose=False, 
    disablejs=disablejs, incognito=incognito, disableimages=disableimages, 
    cache=cache, headless=headless, proxy=proxy)
attemptconnection(c, DEPOSIT_23_URL)

# backup sleep 
time.sleep(4500000) # Hack - leave it open to fill in details