
from pymongo import MongoClient

class MongoUtil:
    @staticmethod
    def getCollection(_dbName,_collName):
        return MongoClient().get_database(_dbName).get_collection(_collName)

if __name__ == '__main__':
    MongoUtil.getCollection('crawler','Job')
