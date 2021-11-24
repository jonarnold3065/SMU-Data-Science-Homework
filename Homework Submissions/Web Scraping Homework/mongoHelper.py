import pymongo

class MongoHelper():
    def __init__(self):
        # Create connection variable
        self.conn = 'mongodb://localhost:27017'

        # Pass connection to the pymongo instance.
        self.client = pymongo.MongoClient(self.conn)

        # Connect to a database. Will create one if not already available.
        self.db = self.client.mars_webScrape

    def insertFacts(self, data):
        # insert into mongo
        self.db.mars_data.insert_one(data)
        return({"ok": True})

    def findLastFacts(self):
        facts = self.db.mars_data.find({}, sort=[('last_updated', pymongo.DESCENDING )], limit=1)
        return(facts[0])
