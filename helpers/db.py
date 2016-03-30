import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.news_scraper
collection = db.news
collection.create_index("href", unique=True)


def save_entry(entry):
    return collection.insert_one(entry).inserted_id


def get_entries(*args, **kwargs):
    return collection.find(*args, **kwargs)
