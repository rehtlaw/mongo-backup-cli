from pymongo import MongoClient

from mongo_backup.zip import read_zip_file

# connect to db, read zip out zip file, drop all collections present in backup and restore from the backup
def restore_files(mongo_uri, db_name, file):
    '''
    @mongo_uri[string]: mongo uri string used to connect to the database
    @db_name[string]: name of the database that is supposed to be restored
    @file[filename/string]: name of the backup zip that it restores from
    '''

    # connect to database
    db = MongoClient(mongo_uri)[db_name]
    # read zip file
    input = read_zip_file(file)

    # restore backup from read zip file
    for collection, value in input.items():
        # if there's a collection with the same name already, delete it
        # otherwise the insert_many() will fail
        if collection in db.list_collection_names():
            db[collection].drop()

        # insert collection
        res = db[collection].insert_many(value)
        print('Successful: {}'.format(res.acknowledged))
