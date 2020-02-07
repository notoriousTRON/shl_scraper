import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import re, itertools

def get_data(soup):
    teams = []
    tbl = []

    for i in soup.find_all('h3',"STHSGame_PlayerStatTitle"):
        teams.append(i.getText().replace('Players Stats for ',''))
    for j in soup.find_all('div',"STHSGame_PlayerStatTable"):
        tbl.append(j.getText())
    for t in range(0,2):
        hr_enter = 'T'
        team = teams[t]
        team_tbl = tbl[t]
        for ln in team_tbl.splitlines():
            if hr_enter == 'T':
                header = ln.split()
                #header = re.split(r"\t",ln)
                hr = ["Team"]
                for h in header:
                    if h == "Player":
                        hr.append("Name")
                    elif h == "Name":
                        None
                    elif h == "PP":
                        hr.append("PP_MP")
                    elif h == "MP":
                        None
                    elif h == "PK":
                        hr.append("PK_MP")
                    else:
                        hr.append(h)
                #print(hr)
                hr_enter = 'F'
            elif '------------------' in ln:
                None
            else:
                row_out = [team]
                nm = ''
                row = ln.split()

                for i in row:
                    try:
                        tst = int(i)
                    except:
                        tst = i
                    if type(tst) == int:
                        if len(nm) >0:
                            row_out.append(nm)
                            nm = ''
                        row_out.append(tst)
                    elif ":" in i:
                        row_out.append(tst)
                    else:
                        if len(nm)==0:
                            nm = nm + tst
                        else:
                            nm = nm + ' ' + tst
                        #row_out.append(str)
                print(dict(zip(hr,row_out)))


season = 'S51'
game = '3'
url = 'https://simulationhockey.com/games/smjhl/{0}/Season/SMJHL-{1}.html'.format(season,game)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
get_data(soup)