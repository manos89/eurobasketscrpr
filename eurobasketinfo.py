# -*- coding: utf-8 -*-
import json,requests
from jscraper import *
import Queue,csv
import threading,re
count=0


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def checkImages(ImageList):
	for I in ImageList:
		r=requests.get(I).text
		if not '404 - File or directory not found.' in r:
			return I
	return 'http://www.eurobasket.com/photos/Not_Available.jpg'

def get_season_stats(PlayerId,Season,PlayerDict):
	link='http://basketball.eurobasket.com/PlayerStatsAjax.asp?PlayerId={PID}&Season={S}'.replace('{PID}',PlayerId).replace('{S}',Season)
	soup=jscraper.get_soup(url=link)
	AverageStatsClass=jscraper.get_classes(soup=soup,TagName='tr',AttributeName='class',AttributeValue='my_pStats1')[0]
	Tables=jscraper.get_classes(soup=soup,TagName='table')
	PlayerDict['averageStats'][Season]=[]
	PlayerDict['fullStats'][Season]=[]
	for ind in range(1,len(Tables)/2,2):
		AverageStatsClass=jscraper.get_classes(soup=soup,TagName='tr',AttributeName='class',AttributeValue='my_pStats1')[ind]
		Averagestats=jscraper.get_text_element(soup=AverageStatsClass,TagName='td')		
		PlayerDict['averageStats'][Season].append({'teamName':Averagestats[0],'games':Averagestats[1],'minutes':Averagestats[2],'points':Averagestats[3],'fg2Average':Averagestats[4],'fg3Average':Averagestats[5],
											'ftAverage':Averagestats[6],'offRebounds':Averagestats[7],'defRebounds':Averagestats[8],'totalRebounds':Averagestats[9],'assists':Averagestats[10],'personalFouls':Averagestats[11],
											'blocks':Averagestats[12],
											'steals':Averagestats[13],'turnovers':Averagestats[14],'ranking':Averagestats[15]})
	for ind2 in range(len(Tables)/2,len(Tables)):
		GameStats1=jscraper.get_classes(soup=soup,TagName='tr',AttributeName='class',AttributeValue='my_pStats1')[ind2:]
		GameStats2=jscraper.get_classes(soup=soup,TagName='tr',AttributeName='class',AttributeValue='my_pStats2')[ind2:]
		GameStats=GameStats1+GameStats2	
		AllGames=[]
		for g in GameStats:
			Game=jscraper.get_text_element(soup=g,TagName='td')
			SingleGame={'date':Game[0],'homeTeam':Game[1],'awayTean':Game[2],'result':cleanhtml(Game[3]),'minutes':Game[4],'points':Game[5],'fg2Average':Game[6],'fg3Average':Game[7],
						'ftAverage':Game[8],'offRebounds':Game[9],'defRebounds':Game[10],'totalRebounds':Game[11],'assists':Game[12],'personalFouls':Game[13],
						'blocks':Game[14],'steals':Game[15],'turnovers':Game[16],'ranking':Game[17]}
			AllGames.append(SingleGame)
		PlayerDict['fullStats'][Season].append(AllGames)


def get_season_stats2(PlayerId,Season,PlayerDict):
	link='http://basketball.eurobasket.com/PlayerStatsAjax.asp?PlayerId={PID}&Season={S}'.replace('{PID}',PlayerId).replace('{S}',Season)
	soup=jscraper.get_soup(url=link)
	if 'no data' in str(soup).lower():
		return
	Titles=jscraper.get_text_element(soup=soup,TagName='h4')
	TableClasses=jscraper.get_classes(soup=soup,TagName='table')
	PlayerDict['fullStats'][Season]={}
	PlayerDict['averageStats'][Season]={}
	for i in range(0,len(Titles)):
		start=Titles[i].find('(')
		end=Titles[i].find(')')
		League=Titles[i][start+1:end]
		if 'AVERAGE' in str(TableClasses[i]).upper():
			AverageStatsClass=jscraper.get_classes(soup=TableClasses[i],TagName='tr',AttributeName='class',AttributeValue='my_pStats1')[0]
			Averagestats=jscraper.get_text_element(soup=AverageStatsClass,TagName='td')
			try:
				PlayerDict['averageStats'][Season][League]={'teamName':Averagestats[0],'games':Averagestats[1],'minutes':Averagestats[2],'points':Averagestats[3],'fg2Average':Averagestats[4],'fg3Average':Averagestats[5],
													'ftAverage':Averagestats[6],'offRebounds':Averagestats[7],'defRebounds':Averagestats[8],'totalRebounds':Averagestats[9],'assists':Averagestats[10],'personalFouls':Averagestats[11],
													'blocks':Averagestats[12],
													'steals':Averagestats[13],'turnovers':Averagestats[14],'ranking':Averagestats[15]}
			except:
				PlayerDict['averageStats'][Season][League]={}
				PlayerDict['averageStats'][Season][League]={'teamName':Averagestats[0],'games':Averagestats[1],'minutes':Averagestats[2],'points':Averagestats[3],'fg2Average':Averagestats[4],'fg3Average':Averagestats[5],
													'ftAverage':Averagestats[6],'offRebounds':Averagestats[7],'defRebounds':Averagestats[8],'totalRebounds':Averagestats[9],'assists':Averagestats[10],'personalFouls':Averagestats[11],
													'blocks':Averagestats[12],
													'steals':Averagestats[13],'turnovers':Averagestats[14],'ranking':Averagestats[15]}
		else:
			GameStats1=jscraper.get_classes(soup=TableClasses[i],TagName='tr',AttributeName='class',AttributeValue='my_pStats1')
			GameStats2=jscraper.get_classes(soup=TableClasses[i],TagName='tr',AttributeName='class',AttributeValue='my_pStats2')
			GameStats=GameStats1+GameStats2	
			AllGames=[]
			for g in GameStats:
				Game=jscraper.get_text_element(soup=g,TagName='td')
				SingleGame={'date':Game[0],'homeTeam':Game[1],'awayTean':Game[2],'result':cleanhtml(Game[3]),'minutes':Game[4],'points':Game[5],'fg2Average':Game[6],'fg3Average':Game[7],
							'ftAverage':Game[8],'offRebounds':Game[9],'defRebounds':Game[10],'totalRebounds':Game[11],'assists':Game[12],'personalFouls':Game[13],
							'blocks':Game[14],'steals':Game[15],'turnovers':Game[16],'ranking':Game[17]}
				AllGames.append(SingleGame)
			try:
				PlayerDict['fullStats'][Season][League]=AllGames
			except:
				PlayerDict['fullStats'][Season][League]={}
				PlayerDict['fullStats'][Season][League]=AllGames
def get_info(queue):
	global count
	queue_full = True
	while queue_full:
		try:
			d= queue.get(False)
			d['fullStats']={}
			d['averageStats']={}
			for i in range(2000,2018):
				try:
					get_season_stats2(d['playerID'],str(i),d)
				except Exception as E:
					pass
			try:
				d['imageUrl']=checkImages(d['imageUrl'])
			except:
				d['imageUrl']='http://www.eurobasket.com/photos/Not_Available.jpg'
			print 'DONE ',count
			count+=1
			q.task_done()
		except Queue.Empty:
			queue_full = False

def get_specific(SearchTest='',StartString='',EndString=''):
	if StartString in SearchTest:
		start=SearchTest.find(StartString)
		my_search=SearchTest[start+len(StartString):]
		end=my_search.find(EndString)
		my_search=my_search[:end]
	else:
		return ' '
	return my_search

def get_dict():
	reader = csv.DictReader(open('countries.csv', 'rb'))
	dict_list = []
	for line in reader:
		dict_list.append(line)
	return dict_list
dict_list=get_dict()

for d in dict_list:
	Country=d['NAME'].strip()
	Cntrabbr=d['ABBRV'].strip()
	url='http://www.eurobasket.com/basketball-players-statistics.asp?women=0&country={COUNTRY}'.replace('{COUNTRY}',Country)
	r=requests.get(url).text
	NoJsonData=get_specific(SearchTest=r,StartString="strData='",EndString="';")
	Data=json.loads(NoJsonData)
	PlayerList=[]
	for d in Data:
		Name=d['PLAYERNAME']
		try:
			Link='http://basketball.eurobasket.com/player/{NAME}/{CNTR}/{TEAM}/{ID}'.replace('{NAME}',d['PLAYERNAME'].split(' ')[1].replace('E&quote;','')+'-'+d['PLAYERNAME'].split(' ')[0].replace('E&quote;','')).replace('{TEAM}',d['TEAMNAME'].replace(' ','-')).replace('{ID}',d['PLAYERID']).replace('{CNTR}',Cntrabbr)
		except:
			Link='http://basketball.eurobasket.com/player/{NAME}/{CNTR}/{TEAM}/{ID}'.replace('{NAME}',d['PLAYERNAME'].split(' ')[0].replace('E&quote;','')).replace('{TEAM}',d['TEAMNAME'].replace(' ','-')).replace('{ID}',d['PLAYERID']).replace('{CNTR}',Cntrabbr)
		try:
			ImageUrl=['http://www.eurobasket.com/photos/{NAME}.jpg'.replace('{NAME}',d['PLAYERNAME'].split(' ')[0]+'_'+d['PLAYERNAME'].split(' ')[1]).replace('E&quote;',''),'http://www.eurobasket.com/photos/{NAME}.jpg'.replace('{NAME}',d['PLAYERNAME'].split(' ')[1]+'_'+d['PLAYERNAME'].split(' ')[0]).replace('E&quote;','')].replace('{CNTR}',Cntrabbr)
		except:
			ImageUrl=['http://www.eurobasket.com/photos/{NAME}.jpg'.replace('{NAME}',d['PLAYERNAME'].split(' ')[0]).replace('E&quote;','')]
		# JsonPlayer={'imageUrl':None ,'playerID':d['PLAYERID'] ,'playerUrl':Link ,'age':d['AGE'] ,'birthday':None ,'gender':None ,'heightcm':d['HEIGHT'] ,'heightin':d['HEIGHTIN'] ,'leagueName':d['LEAGUENAME'] ,
		# 'nationality':d['NAT1'] ,'playerName':d['PLAYERNAME'] ,'position':d['POSITION'] ,'teamCountry':d['TEAMCOUNTRY'] ,'teamName':d['TEAMNAME'] ,'teamNo':d['TEAMNO'] ,'games':d['Games'] ,'minutes':d['MIN'] ,'points':d['PTS'] ,
		# 'fieldgoalsMade2':d['FGPM2'] ,'fieldgoalsAttempt2':d['FGPA2'] ,'fieldgoalsMade3':d['FGPM3'] ,'fg3Average':d['FGPA3'] ,'freethrowsMade':d['FTM'] ,'freethrowsAttempt':d['FTA'] ,'offensiveRebounds':d['REBO'] ,'defensiveRebounds':d['REBD'] ,'totalRebounds':d['REBT'] ,'asists':d['AS'] ,'personalFouls':d['PF'] ,'pfrv':d['PFRV'] ,'blocks':d['BS'] ,'blocksAgainst':d['BSAG'] ,'steals':d['ST'] ,'turnovers':d['TO'] ,'ranking':d['MVP'] }
		JsonPlayer={'imageUrl':ImageUrl ,'playerID':d['PLAYERID'] ,'playerUrl':Link ,'age':d['AGE'] ,'birthday':None ,'gender':'Male' ,'heightcm':d['HEIGHT'] ,'heightin':d['HEIGHTIN'] ,'leagueName':d['LEAGUENAME'] ,
		'nationality':d['NAT1'] ,'playerName':d['PLAYERNAME'] ,'position':d['POSITION'] ,'teamCountry':d['TEAMCOUNTRY'] ,'teamName':d['TEAMNAME'] ,'teamNo':d['TEAMNO'] }
		PlayerList.append(JsonPlayer)
	PlayerList=PlayerList

	q = Queue.Queue()

	for d in PlayerList:
		q.put(d)



	print 'Collecting information from each link'
	thread_count = 12


	for i in range(thread_count):
		t = threading.Thread(target=get_info, args = (q,))
		t.start()

	q.join()


	with open(Country+'Men.json', 'w') as outfile:
		json.dump(PlayerList, outfile, sort_keys = True, indent = 4, ensure_ascii = False)


	print 'DONE ',Country