from os import remove

from bson import json_util
from pymongo import MongoClient

from mongo_backup.zip import create_zip_file

# read mongodb collections, dump them into json files, zip them up and remove any remaining files
def backup_files(mongo_uri, db_name, input_collections):
    '''
    @mongo_uri[string]: mongo uri string used to connect to the database
    @db_name[string]: name of the database that is supposed to be backed up
    @input_collections[[]string]: list off collections that are supposed to be backed up (can also be an empty string)
    '''
    # connect to mongodb
    db = MongoClient(mongo_uri)[db_name]
    collections = input_collections

    # checks for an empty string as the collection input
    if not input_collections:
        # get all collections that are available
        collections = db.list_collection_names()

    files = []

    # read all collections and write them to their own json files
    for col in collections:
        data_set = []
        # read collection because pymongo wants it this way
        for grid_out in db[col].find():
            data_set.append(grid_out)

            # create file name
            file_name = '{}.json'.format(col)

        # write file with content
        with open(file_name, 'w') as f:
            f.write(json_util.dumps(data_set))

        # add file names to files list
        files.append(file_name)

    # zip 'em up
    create_zip_file(files, db_name)

    # remove remaining files
    for file in files:
        remove(file)
