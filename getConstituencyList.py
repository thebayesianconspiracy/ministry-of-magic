import sys
import requests
from bs4 import BeautifulSoup
import json
import jsonpickle

class constituency:
    name = ""
    district = []
    constituencyId = -1
    population = 0

    def __init__(self, name, district, constituencyId, population):
        self.name = name
        self.district = district
        self.constituencyId = constituencyId
        self.population = population

    def __str__(self):
        toString = "name: " + self.name + " district: " + self.district + " constituencyId: " + self.constituencyId + " population: " + str(self.population)
        return toString


def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

        
state_elections_url = sys.argv[1]
full_url = "http://myneta.info/" + state_elections_url + "/"

r = requests.get(full_url)
soup = BeautifulSoup(r.text, "html.parser")
districtHTML =  soup.find_all("h5", class_="title")

districtList = []

for element in districtHTML:
    districtList.append(element.a.get_text().strip())

constituencyHTML = soup.find_all("div", class_="items")

constituencyList = []

districtId = -1
for element in constituencyHTML:
    stringList = element.get_text().strip().split(':')
    if (len(stringList) < 2):
        continue
    if (stringList[0] == '1'):
        districtId+=1
    constituencyId = find_between(str(element), "constituency_id=", '"')
    constituencyList.append(constituency(stringList[1],districtList[districtId] , constituencyId, 0))
#    constituencyList.append(element.a.get_text().strip())


#for i in range(len(constituencyList)):
#    print(constituencyList[i])
#print(districtList)

frozen = jsonpickle.encode(constituencyList)

print(frozen)
