import csv,sys
from pymongo import MongoClient



class constituency:
    parliamentary_constituency = ""
    name = ""
    total_population = 0
    sc_population = 0
    st_population = 0
    district = ""
    constituency_id = -1

    def __init__(self, name, district, constituencyId, total_population,sc_population, st_population, parliamentary_constituency):
        self.name = name
        self.district = district
        self.constituencyId = constituencyId
        self.total_population = total_population
        self.sc_population = sc_population
        self.st_population = st_population
        self.parliamentary_constituency = parliamentary_constituency

    def __str__(self):
        toString = "name: " + self.name + " district: " + self.district + " constituencyId: " + str(self.constituencyId) + " population: " + str(self.total_population)
        return toString
    

db_interaction = sys.argv[1]

if (db_interaction == "true"):
    connection = MongoClient("ds135916.mlab.com", 35916)
    db = connection["ministryofmagic"]
    db.authenticate("soumyadeep", sys.argv[2])
    #print(db.collection_names())

    if ("constituencies" in db.collection_names()):
        pass
    else:
        db.create_collection("constituencies")

    constituency_collection = db.constituencies


with open('karnataka-constituencies.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            parliamentary_constituency = row[0].split('-')[1]
            name = row[1].split('.')[1].strip()
            total_population = int(row[2])
            sc_population = int(row[3])
            st_population = int(row[4])
            district = row[5]
            single_constituency = constituency(name, district, -1, total_population, sc_population, st_population, parliamentary_constituency)
            if (db_interaction == "true"):
                constituency_collection.insert_one(single_constituency.__dict__)

            print(single_constituency)
        except(IndexError):
            print("Header")

