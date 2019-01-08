import os
import bson
from zipfile import ZipFile

from mongo_backup.const import DATE_NOW

# create a zip file with all collections and a date-stamp
def create_zip_file(files, db_name):
    '''
    @files[[]file/string]: list of files that belong to the backup
    @db_name[string]: name of the database so one knows which database has been backed up
    '''
    # create zip file with date and db_name
    with ZipFile('backup-{}-{}.zip'.format(DATE_NOW, db_name), 'w') as zip:
        # write all files from files list to the zip
        for file in files:
            zip.write(file)


# open zip file, get collections from the file names, read json files and return a dict with each collection and it's contents
def read_zip_file(file):
    '''
    @file[file/string]: name of the zip file that is supposed to be read
    '''
    from_archive = {}
    # open zip file
    with ZipFile(file, 'r') as zip:
        # get collections
        collections = zip.namelist()
        # read out collections
        for name in collections:
            with zip.open(name) as myfile:
                content = bson.json_util.loads(myfile.read())
                # add the collection to returned dict
                from_archive[os.path.splitext(myfile.name)[0]] = content

    return from_archive
