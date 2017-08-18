from bs4 import BeautifulSoup
from selenium import webdriver
import time
from decimal import *
import datetime
import os

def getB365Odds(b365Source, b365BetNo):

    soup = BeautifulSoup(b365Source, "html.parser")
    container = soup.find("div",{"id":"MarketGrid"})

    teams = []
    betodds = []
    currentbet = 1
    for bet in container:
        teamname = bet.findAll("span",{"class":"ipe-Participant_OppName"})
        odds = bet.findAll("span",{"class":"ipe-Participant_OppOdds "})
        susp = bet.findAll("div",{"class":"ipe-Participant ipe-Participant_Suspended "})
        
        if currentbet == b365BetNo and len(susp) == 0:
            anum, aden = odds[0].text.split('/')
            a1 = (float(anum)/float(aden)) + 1
            a = Decimal(str(a1)).quantize(Decimal('.01'), rounding=ROUND_DOWN)

            bnum, bden = odds[1].text.split('/')
            b1 = (float(bnum)/float(bden)) + 1
            b = Decimal(str(b1)).quantize(Decimal('.01'), rounding=ROUND_DOWN)

            betodds.append(a)
            betodds.append(b)

            teams.append(teamname[0].text)
            teams.append(teamname[1].text)

        currentbet += 1

    
    if len(betodds) == 2:
        return(float(betodds[0]), float(betodds[1]), teams[0], teams[1])
    else:
        return(None, None, teams[0], teams[1])


with open("B365Log.txt", "a") as logf:
    url = input("Paste Bet365 url: ")
    betNo = int(input("Bet number: "))

    b365D = webdriver.Chrome()
    b365D.get(url)
    time.sleep(3)

    lastodds = []
    logf.write("-----------------------------------------------------\n")
    running = True
    while running:
        try:
            
            b365S = b365D.execute_script("return document.documentElement.outerHTML") 
            b365Odds = getB365Odds(b365S, betNo)            

            if len(lastodds) == 0:
                lastodds.append(b365Odds[0])
                lastodds.append(b365Odds[1])
                logf.write("{0}: {1} {2} {3} {4}\n".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                                       b365Odds[2], b365Odds[0], b365Odds[3], b365Odds[1]))

                print(b365Odds[2], b365Odds[0], b365Odds[3], b365Odds[1])

                logf.flush()
                os.fsync()
            
            if b365Odds[0] != lastodds[0] or b365Odds[1] != lastodds[1]:
                logf.write("{0}: {1} {2} {3} {4}\n".format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                                                       b365Odds[2], b365Odds[0], b365Odds[3], b365Odds[1]))

                lastodds[0] = b365Odds[0]
                lastodds[1] = b365Odds[1]

                print(b365Odds[2], b365Odds[0], b365Odds[3], b365Odds[1])

                logf.flush()
                os.fsync()
            
        except:
            pass

        time.sleep(1)

