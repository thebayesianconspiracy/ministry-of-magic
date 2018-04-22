import sys
import requests
from bs4 import BeautifulSoup
import json
import jsonpickle
from pymongo import MongoClient


class candidate:
    name = ""
    constituencyId = ""
    party = ""
    criminal_cases = 0
    education = ""
    education_scale = 0
    age = 0
    total_assets = 0
    liabilities = 0
    candidateID = -1

    '''
    Scaling eductaion to a number to draw visualizations
    Illiterate, Not Given and Others considered 0
    Class considered as is
    Post Graduate is 12 + 3 + 2
    Graduate is 12 + 3 
    Graduate Professional is 12 + 3 + 2
    '''
    
    def getEducationScale(self, education):
        #        print(education)
        if(education.find("Pass") != -1):
            return int(education.split("th")[0])
        elif(education == "Graduate"):
            return 15
        elif(education.find("Professional")):
            return 17
        elif(education.find("Post")):
            return 17
        return 0

    def __init__(self, name, constituencyId, party, criminal_cases, education, age, total_assets, liabilities, candidateId):
        self.name = name
        self.constituencyId = constituencyId
        self.party = party
        self.criminal_cases = criminal_cases
        self.education = education
        self.age = age
        self.total_assets = total_assets
        self.liabilities = liabilities
        self.education_scale = self.getEducationScale(education)
        self.candidateID = candidateId

    def __str__(self):
        toString = "name:" + self.name + " party: " + self.party + " criminal_cases:" + self.criminal_cases + " education: " + self.education + " age: " + self.age + " assets: " + str(self.total_assets) + " liabilities: " + str(self.liabilities)
        return toString
    

constituencyIDList = ['39', '40', '37', '38', '34', '36', '35', '47', '44', '41', '42', '43', '45', '46', '52', '50', '54', '48', '53', '51', '49', '31', '32', '30', '33', '29', '27', '28', '110', '111', '109', '112', '61', '60', '56', '58', '59', '55', '57', '16', '11', '24', '20', '21', '19', '10', '17', '15', '12', '22', '23', '13', '9', '26', '14', '25', '18', '163', '164', '158', '159', '161', '166', '165', '162', '160', '207', '202', '206', '205', '204', '203', '220', '219', '221', '218', '223', '217', '222', '224', '68', '69', '66', '67', '120', '121', '123', '119', '122', '137', '139', '136', '135', '138', '153', '154', '155', '157', '156', '152', '88', '83', '87', '85', '86', '84', '89', '90', '7', '4', '5', '2', '3', '8', '1', '6', '181', '183', '182', '184', '185', '180', '179', '187', '189', '188', '186', '208', '216', '212', '210', '214', '213', '215', '209', '211', '96', '92', '93', '94', '95', '97', '91', '170', '167', '169', '171', '172', '168', '81', '82', '116', '117', '115', '118', '114', '113', '192', '191', '194', '190', '193', '104', '99', '98', '101', '100', '103', '102', '77', '75', '73', '72', '76', '71', '74', '78', '70', '80', '79', '198', '199', '197', '201', '196', '195', '200', '108', '107', '105', '106', '141', '146', '144', '142', '140', '145', '143', '124', '131', '130', '127', '134', '133', '132', '125', '128', '129', '126', '147', '151', '150', '148', '149', '176', '173', '174', '175', '177', '178', '65', '63', '62', '64']

#constituencyIDList = ['102', '77', '75', '73', '72', '76', '71', '74', '78', '70', '80', '79', '198', '199', '197', '201', '196', '195', '200', '108', '107', '105', '106', '141', '146', '144', '142', '140', '145', '143', '124', '131', '130', '127', '134', '133', '132', '125', '128', '129', '126', '147', '151', '150', '148', '149', '176', '173', '174', '175', '177', '178', '65', '63', '62', '64']

def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

#constituency_id = sys.argv[1]
db_interaction = sys.argv[1]
elections = sys.argv[2]


for constituency_id in constituencyIDList:
    print("CONSTITUENCYID: "+ constituency_id)
    full_url = "http://myneta.info/" + elections + "/index.php?action=show_candidates&constituency_id=" + constituency_id
    r = requests.get(full_url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        candidateHTML = soup.findAll('table')[2].findAll('tr')
    except:
        candidateHTML = []
        pass
    candidateList = []


    if (db_interaction == "true"):
        connection = MongoClient("ds135916.mlab.com", 35916)
        db = connection["ministryofmagic"]
        db.authenticate("soumyadeep", sys.argv[3])
        #print(db.collection_names())
        if ("candidates" in db.collection_names()):
            pass
        else:
            db.create_collection("candidates")
        candidate_collection = db.candidates

    for element in candidateHTML:
        try:
            candidateData = element.find_all("td")
            name = candidateData[0].get_text().split('\xa0\xa0')[0]
            candidateId = find_between(str(candidateData[0]), "candidate_id=", '"')
            party = candidateData[1].get_text()
            criminal_cases = candidateData[2].get_text()
            age = candidateData[4].get_text()
            education = candidateData[3].get_text()
            if (candidateData[5].get_text() != "Nil"):
                total_assets = int(candidateData[5].get_text().strip("Rs").strip().split('~')[0].strip().replace(',',''))
            else:
                total_assets = 0
            liabilities = int(candidateData[6].get_text().strip("Rs").strip().split('~')[0].strip().replace(',',''))
            candidateOb = candidate(name, constituency_id, party, criminal_cases, education, age, total_assets, liabilities, candidateId)
            print(candidateOb)
            if (db_interaction == "true"):
                candidate_collection.insert_one(candidateOb.__dict__)
        #        break
        except (IndexError):
            print("Header")
            pass
    
    
    


