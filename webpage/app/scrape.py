import requests
import urllib
import datetime
import time
import pytz
import calendar
from pytz import timezone
from datetime import datetime
from bs4 import BeautifulSoup

# TO DO
# [Errno 32] Broken pipe - error
# -4000 on time.
# Scrape time and location.
# Make scraping faster and more efficient
# incorporate database and get rid of only getting 10 events.

# Helper function that checks if a string can be converted to an int.
def isint(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#get_content2 and get_event2 are now the functions that I am using.
def get_content(): #returns a list of recent blitzes
    # Get the month and week of month of today.
    date = datetime.now().date() 
    year = date.year
    year = year % 2000  # only the last two digits of year.
    month = date.month
    padded_month = ("%02d" % month)
    day = date.day
    week_of_month = ((day + 6)/7)
    letter_for_week = chr(ord('a') + week_of_month - 1) # first week is A, etc.

    last_year = year
    last_month = month
    last_week = week_of_month - 1
    # Get the previous week.
    if week_of_month == 1:
        last_month = month - 1
        last_week = 5
        if month == 1:
            last_month = 12
            last_year = year - 1
        if last_month == 2:
            last_week = 4
    padded_last_month = ("%02d" % last_month)
    letter_for_last_week = chr(ord('a') + last_week - 1) # first week is A, etc.

    # Scrape for this week.
    listserv_url = 'https://listserv.dartmouth.edu/scripts/wa.exe?A1=ind' + str(year) + str(padded_month) + letter_for_week + '&L=CAMPUS-EVENTS&O=D&H=0&D=1&T=1'

    # Finds the correct link for the list of this week's events, 
    # then gets the basic info for all of those events

    r = requests.get(listserv_url) # stores url response in var "r"
    soup = BeautifulSoup(r.text) # stores url response in a BeautifulSoup object for later parsing
    events = [] # initialize vars
    iterator = 0
    for link in soup.find_all('a'): # go through every link from the url
        if iterator > 0: # we only want to go through this loop once, iterator makes sure of that
            break
        href = link.get('href') # href now holds the href of the link
        if href: # if href isn't None
            if  '/scripts/wa.exe?A1=' in href: # if href contains this string, it's what we're looking for
                   r = requests.get('https://listserv.dartmouth.edu'+href) # makes a new request from this link
                   soup2 = BeautifulSoup(r.text) # puts it into beautifulsoup format
                   for event in soup2.find_all('a'): # for all of the links on this page
                       if event.get('href'):
                           if '/scripts/wa.exe?A2=' in event.get('href'):
                               data = []
                               data.append(event.text) # add the event title
                               data.append(urllib.quote_plus(event.get('href'))) # add the url for the event
                               events.append(data)
                   iterator = iterator + 1

    # Scrape for last week
    # NOTE: I will move this soup/link/event/iterator stuff into a separate function,
    # once I know it is okay to do that.
    # h: yeah that'd be good! also might want to get the "from" field (who the event was sent from) as well since that's part of it
    listserv_url2 = 'https://listserv.dartmouth.edu/scripts/wa.exe?A1=ind' + str(last_year) + str(padded_last_month) + letter_for_last_week + '&L=CAMPUS-EVENTS&O=D&H=0&D=1&T=1'

       #same comments as above for this loop
    r = requests.get(listserv_url2)
    soup3 = BeautifulSoup(r.text)
    iterator = 0
    for link in soup3.find_all('a'):
        if iterator > 0:
            break
        href = link.get('href')
        if href:
            if  '/scripts/wa.exe?A1=' in href:
                   r = requests.get('https://listserv.dartmouth.edu'+href)
                   soup4 = BeautifulSoup(r.text)
                   for event in soup4.find_all('a'):
                       if event.get('href'):
                           if '/scripts/wa.exe?A2=' in event.get('href'):
                               data = []
                               data.append(event.text)
                               data.append(urllib.quote_plus(event.get('href')))
                               events.append(data)
                   iterator = iterator + 1
    return events

def get_event(event_url): # This method returns all the relevant information for a specific event URL given
    #initialize vars
    url = ''
    txt = ''
    data = []
    event_url = ''+urllib.unquote_plus(event_url)
    event_subject = ''

    #get request
    r = requests.get('https://listserv.dartmouth.edu'+event_url)
    soup = BeautifulSoup(r.text)

    #get subject, from, and date
    event_subject = soup.find(text="Subject:").findNext('a').contents[0]            # finds subject of event
    event_from = soup.find(text="From:").findNext('p').contents[0].replace('<','')  # finds from of event
    date = soup.find(text="Date:").findNext('p').contents[0].replace('<','')         # finds date of blitz sent out

    #formats the date (NOTE: there's a bug where some events don't have +0000 but -4000, which throws an error)
    utc_dt = datetime.strptime(date.replace(' +0000',''),'%a, %d %b %Y %H:%M:%S').replace(tzinfo=pytz.utc) #
    loc_dt = utc_dt.astimezone(timezone('US/Eastern'))
    event_date = loc_dt.strftime('%A, %b %d %I:%M%p')

    #get txt by starting a new request from the link to text/plain
    for link in soup.find_all('a'):
        if (link.get('href')):
            if (link.text == 'text/plain'): #text/html, get this url and pass it in to the view.py
                url = link.get('href')
                break
    if (url != ''):
        r = requests.get('https://listserv.dartmouth.edu'+url) # makes a new request to get the text from the URL that outputs plaintext
        soup = BeautifulSoup(r.text)
        for pre in soup.find_all('pre'):
            txt = pre.text

    #return all
    data.append(txt)
    data.append(event_subject)
    data.append(event_from)
    data.append(event_date)
    return data

def get_content2(): #returns a list of recent blitzes
    # Get the month and week of month of today.
    date = datetime.now().date() 
    year = date.year
    year = year % 2000  # only the last two digits of year.
    month = date.month
    padded_month = ("%02d" % month)
    day = date.day
    week_of_month = ((day + 6)/7)
    letter_for_week = chr(ord('a') + week_of_month - 1) # first week is A, etc.

    last_year = year
    last_month = month
    last_week = week_of_month - 1
    # Get the previous week.
    if week_of_month == 1:
        last_month = month - 1
        last_week = 5
        if month == 1:
            last_month = 12
            last_year = year - 1
        if last_month == 2:
            last_week = 4
    padded_last_month = ("%02d" % last_month)
    letter_for_last_week = chr(ord('a') + last_week - 1) # first week is A, etc.

    # Scrape for this week.
    listserv_url = 'https://listserv.dartmouth.edu/scripts/wa.exe?A1=ind' + str(year) + str(padded_month) + letter_for_week + '&L=CAMPUS-EVENTS&O=D&H=0&D=1&T=1'

    # Finds the correct link for the list of this week's events, 
    # then gets the basic info for all of those events

    r = requests.get(listserv_url) # stores url response in var "r"
    soup = BeautifulSoup(r.text) # stores url response in a BeautifulSoup object for later parsing
    realEvents = []
    iterator = 0
    for link in soup.find_all('a'): # go through every link from the url
        if iterator > 0: # we only want to go through this loop once, iterator makes sure of that
            break
        href = link.get('href') # href now holds the href of the link
        if href: # if href isn't None
            if  '/scripts/wa.exe?A1=' in href: # if href contains this string, it's what we're looking for
                r = requests.get('https://listserv.dartmouth.edu'+href) # makes a new request from this link
                soup2 = BeautifulSoup(r.text) # puts it into beautifulsoup format
                for event in soup2.find_all('a'): # for all of the links on this page
                    if event.get('href'):
                        if '/scripts/wa.exe?A2=' in event.get('href'):
                            newEvent = get_event2(urllib.quote_plus(event.get('href')))
                            if newEvent:
                                realEvents.append(newEvent)
                            #TESTING - only get 10 events
                            if len(realEvents) >= 6:
                                return realEvents
                iterator = iterator + 1

    # Scrape for last week
    # NOTE: I will move this soup/link/event/iterator stuff into a separate function,
    # once I know it is okay to do that.
    # h: yeah that'd be good! also might want to get the "from" field (who the event was sent from) as well since that's part of it
    listserv_url2 = 'https://listserv.dartmouth.edu/scripts/wa.exe?A1=ind' + str(last_year) + str(padded_last_month) + letter_for_last_week + '&L=CAMPUS-EVENTS&O=D&H=0&D=1&T=1'

    #same comments as above for this loop
    r = requests.get(listserv_url2)
    soup3 = BeautifulSoup(r.text)
    iterator = 0
    for link in soup3.find_all('a'):
        if iterator > 0:
            break
        href = link.get('href')
        if href:
            if  '/scripts/wa.exe?A1=' in href:
                r = requests.get('https://listserv.dartmouth.edu'+href)
                soup4 = BeautifulSoup(r.text)
                for event in soup4.find_all('a'):
                    if event.get('href'):
                        if '/scripts/wa.exe?A2=' in event.get('href'):
                            newEvent = get_event2(urllib.quote_plus(event.get('href')))
                            if newEvent:
                                realEvents.append(newEvent)
                            # TESTING - only get 10 events
                            if len(realEvents) >= 6:
                                return realEvents
                iterator = iterator + 1
    return realEvents

def get_event2(event_url): # This method returns all the relevant information for a specific event URL given
    #initialize vars
    url = ''
    htmlurl = ''
    txt = ''
    data = []
    event_url = ''+urllib.unquote_plus(event_url)
    event_subject = ''

    #get request
    r = requests.get('https://listserv.dartmouth.edu'+event_url)
    soup = BeautifulSoup(r.text)

    #get subject, from, and date
    event_subject = soup.find(text="Subject:").findNext('a').contents[0].strip()           # finds subject of event
    event_from = soup.find(text="From:").findNext('p').contents[0].replace('<','')  # finds from of event
    date = soup.find(text="Date:").findNext('p').contents[0].replace('<','')         # finds date of blitz sent out
    
    nicknames = {
        'delta delta delta':'TriDelt',
        'kappa kappa gamma':'Kappa',
        'alpha delta':'AD',
        'sigma phi epsilon':'SigEp',
        'alpha chi alpha':'Alpha Chi',
        'beta alpha omega':'Beta',
        'chi heorot':'Heorot',
        'collis governing board':'Collis',
        'kappa kappa kappa':'Tri-Kap',
        'kappa delta':'KD',
        'epsilon kappa theta': 'EKT',
        'sigma alpha epsilon':'SAE',
        'psi upsilon': 'Psi U',
        'zeta psi': 'Zete',
        'phi Delta alpha': 'Phi Delt',
        'alpha xi delta': 'AZD',
        'dartmouth outing club':'DOC',
        '"bar.hop"':'BarHop'
        }

    categories_names = [
        'Greek',
        'Social',
        'Sports',
        'Performances',
        'Misc'
    ]

    categories = [
        ['tridelt','kappa',' ad ','sigep','alpha chi',' beta ','heorot','tri-kap','trikap',' kd ',' ekt ',' sae ',' psi u ',' psiu ',' zete ',
            'phi delt',' azd '],
        ['collis','one wheelock','collis after dark','barhop'],
        ['football','soccer','hockey','baseball','basketball','tennis','volleyball','track & field','cross country','squash'],
        ['acapella','dog day','decibelles','brovertones','cords','rockapellas','subtleties','dodecaphonics','dodecs','aires',
            'dartmouth symphony orchestra','soul scribes','casual thursday','rude mechanicals'],
    ]

    print categories

    event_from = event_from.strip()
    if event_from.lower() in nicknames.keys():
        event_from = nicknames.get(event_from.lower())
    #formats the date (NOTE: there's a bug where some events don't have +0000 but -4000, which throws an error)
    try:
    	utc_dt = datetime.strptime(date.replace(' +0000',''),'%a, %d %b %Y %H:%M:%S').replace(tzinfo=pytz.utc)
    except:
    	return None
    loc_dt = utc_dt.astimezone(timezone('US/Eastern'))
    event_date = loc_dt.strftime('%A, %b %d %I:%M%p')

    #get txt by starting a new request from the link to text/plain
    for link in soup.find_all('a'):
        if (link.get('href')):
            if (link.text == 'text/plain'):
                url = link.get('href')
            if (link.text == 'text/html'):
                htmlurl = urllib.quote_plus('https://listserv.dartmouth.edu'+ link.get('href'))
            if (url !='') and (htmlurl != ''):
                break

    if (url != ''):
        r = requests.get('https://listserv.dartmouth.edu'+url) # makes a new request to get the text from the URL that outputs plaintext
        soup = BeautifulSoup(r.text)
        for pre in soup.find_all('pre'):
            txt = pre.text

    # Day keywords
    keywords = {'today':"today",
            "tonight":"today",
            "tomorrow":"tomorrow",
            "monday":"0",
            "tuesday": "1",
            "wednesday":"2",
            "thursday":"3",
            "friday": "4",
            "saturday": "5",
            "sunday":"6"
            }

    # Go through the message day by day.
    words = txt.split()

    # Information about today and about the message.
    todayDay = datetime.now().date().day
    messageDay = loc_dt.date().day
    messageMonth = loc_dt.date().month
    daysInMessageMonth = calendar.monthrange(loc_dt.date().year, messageMonth)[1]
    thisEvent = {'from':event_from,'subject':event_subject,'blitz_date':loc_dt,'category':'Misc','time_event':'7PM','date_event':'', 'html':htmlurl}

    if event_from.lower() in categories[0] or event_subject.lower() in categories[0]:
            thisEvent['category'] = categories_names[0]
    elif event_from.lower() in categories[1] or event_subject.lower() in categories[1]:
            thisEvent['category'] = categories_names[1]
    elif event_from.lower() in categories[2] or event_subject.lower() in categories[2]:
            thisEvent['category'] = categories_names[2]
    elif event_from.lower() in categories[3] or event_subject.lower() in categories[3]:
            thisEvent['category'] = categories_names[3]
    # Loop through all the words.
    for word in words:
        # If the word is a keyword.
        if (thisEvent['category'] == 'Misc'):
            if word.lower() in categories[0]:
                thisEvent['category'] = categories_names[0]
            elif word.lower() in categories[1]:
                thisEvent['category'] = categories_names[1]
            elif word.lower() in categories[2]:
                thisEvent['category'] = categories_names[2]
            elif word.lower() in categories[3]:
                thisEvent['category'] = categories_names[3]

        if word.lower() in keywords.keys():
            print "Got here"
            classifier = keywords.get(word.lower())
            if classifier == "today":
                # check if the event message was sent today
                if messageDay == todayDay:
                    thisEvent['date_event'] = 'today'
            elif classifier == "tomorrow":
                # Check if the event message was sent today or yesterday.
                if messageDay == todayDay:
                    thisEvent['date_event'] = 'tomorrow'
                elif (messageDay == (todayDay - 1)) or (messageDay + 1 == todayDay + daysInMessageMonth):
                    thisEvent['date_event'] = 'today'
            # If the word implies a day of the week.
            elif isint(classifier) and (int("0") <= int(classifier) <= int("6")):
                # Need to deal with month overlaps
                eventDayofWeek = int(classifier)

                # Find which day the event is on based on the word and the message date.
                daysFromMessage = (eventDayofWeek - loc_dt.date().weekday()) % 7
                eventDay = messageDay + daysFromMessage

                # If the message is from last month.
                if datetime.now().date().month > messageMonth:
                    eventDay = eventDay - daysInMessageMonth

                if eventDay == todayDay:
                    thisEvent['date_event'] = 'today'
                elif eventDay == (todayDay + 1):
                    thisEvent['date_event'] = 'tomorrow'
                elif eventDay > todayDay:
                    thisEvent['date_event'] = 'upcoming'

            if (thisEvent['date_event'] != ''):
                print 'Found date. Subject: ' + thisEvent['subject'] + ' Category: ' + thisEvent['category']
                return thisEvent

    # Return the event if it contained an event date.
    # if thisEvent['date_event'] != '':
    #return all
    print thisEvent['category']
    return thisEvent
