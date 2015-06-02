from pyvirtualdisplay import Display
from selenium import webdriver
import os
import redis
import json
import pickle

def setvalue(redis, supcs, pog_id):
    redis.set(supcs, pickle.dumps(pog_id));

def getvalue(redis, supcs):
    pog_id = redis.get(supcs);
    if (pog_id is None):
        return None;
    return pickle.loads(pog_id);


r = redis.Redis(host = "127.0.0.1",port = "6379",db = 0);
try :

    display = Display(visible=0, size=(1024, 768))
    display.start()
    fromCity = raw_input("fromCity")
    departDate  = raw_input("departDate");
    toCity = raw_input("toCity")
    key = fromCity+"-"+toCity+"-"+departDate;
    t =  getvalue(r,key)
    if(t != None):
	print t;
    else:
        browser = webdriver.Firefox()
        bl = "http://www.travelyaari.com/ty2/search/?mode=oneway&hop=direct&fromCity="
        l1 = "&toCity="
        l2 = "&departDate="
        l3 = "&src=h&fcs=karnataka&h=v2&b=firefox&ver=v2"
	url = bl+fromCity.lower()+l1+toCity.lower()+l2+departDate+l3
	browser.get(url)

	#scraping
	operator = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="operator"]//h3')
	#bus_type = browser.find_elements_by_xpath('')
	departure = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="departure sorting_1"]/div[@class="time"]')
	duration = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="duration"]/div[@class="time"]')
	arrival = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="arrival"]/div[@class="time"]')
	seats = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="seats"]')
	fare = browser.find_elements_by_xpath('.//*[@id="searchResultsTable"]/tbody//tr//td[@class="fare"]/div[@class="amount"]')

	print len(operator), len(departure), len(duration), len(arrival), len(seats), len(fare)

	i = 0
	schedule = ""
	while(i < len(operator)):
	    print operator[i].text, ' ', departure[i].text, ' ',
	    print duration[i].text, ' ', arrival[i].text, ' ',
	    print seats[i].text, ' ', fare[i].get_attribute("data-fare")
	    print '\n\n'
	    schedule  = schedule+ ("schedule_"+str(i+1)+"   "+operator[i].text+' '+departure[i].text+'      '+duration[i].text+ '       ' +arrival[i].text+ '        '+seats[i].text+ '        '+ str(fare[i].get_attribute("data-fare")) + '\n'); 
	    i += 1
	setvalue(r,key,schedule);
	browser.close()
except Exception, e:
    print e

