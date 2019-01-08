import click

from mongo_backup.backup import backup_files
from mongo_backup.restore import restore_files
from mongo_backup.replica import init_replica

echo = click.echo

# define main CLI
@click.group()
@click.version_option(version='0.1.0')
def main():
    pass


@main.command()
@click.option('--uri',
              type=str,
              help='The MongoDB URI of the server that you want to back up.')
@click.option('--db-name', 'db_name',
              type=str,
              help='The name of the MongoDB database that you want to back up')
@click.option('--collections',
              default='',
              help='All the collections that you want to back up (seperated by commas). Leave this empty if you want all collections.')
def backup(uri, db_name, collections):
    ''' backup command
    this command will grab all collections from the provided database and mongo uri and put them into their own .json files,
    which will all end up in a .zip file with the date and the database name
    '''
    if ',' in collections:
        collections = collections.strip().split(',')
    elif collections:
        collections = [collections]

    backup_files(uri, db_name, collections)


@main.command()
@click.option('--uri',
              help='The MongoDB URI of the server that you want to back up.')
@click.option('--db-name', 'db_name',
              help='The name of the MongoDB database that you want to back up')
@click.option('--file',
              type=click.File('r'),
              help='The file that is used to restore the database')
def restore(uri, db_name, file):
    ''' restore command
    this command will read all the .json files from .zip file and import them back onto the provided
    mongo server and database (only works with backups created by this tool or created in the same way)
    '''
    restore_files(uri, db_name, file.name)

@main.command()
@click.option('--set-name', 'set_name',
              help='The name the replica set will be known as.')
@click.option('--primary',
              help='The primary node in the replica set.')
@click.option('--secondary',
              help='All the secondary nodes in the replica set.')
def replica(set_name, primary, secondary):
    ''' replica command
    this command will set up a replica set for you, but you still need to configure the servers yourself
    (aka. start them with the replica set name as a parameter or in their config file)
    '''
    secondary_list = secondary.strip().split(',')
    init_replica(set_name, primary, secondary_list)
