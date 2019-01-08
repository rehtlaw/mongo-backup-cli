# A command-line tool to back up your MongoDB databases

## Usage

* Installation

``` shell
pip install -U git+https://github.com/rehtlaw/mongo-backup-cli.git
```

* Backing up all collections of a database

``` shell
mongo-backup backup --uri mongodb://username:password@yourmongodbinstance.net --db-name name_of_db
```

this will put a zip in the current directory named
`backup-{year}_{month}_{day}-{db_name}.zip` which contains one json file per collection

* Backing up multiple specific collections

``` shell
mongo-backup backup --uri mongodb://username:password@yourmongodbinstance.net --db-name
name_of_db --collections col1,col2,col3
```

This will also put a zip in your current directory the same as the other command
does, but this will only have the json files of the collections your provided.
This also works when you pass it only 1 collection, but it will still end up
with a .zip file

* Restoring a backup

``` shell
mongo-backup restore backup.zip --uri mongodb://username:password@yourmongodbinstance.net
--db-name name_of_db 
```

This will upload all the .json files inside the .zip file to the MongoDB server
that is provided and delete all the data of the backed up collections that was
previously on the server.

WARNING: This also deletes any collections with the same names as the ones in
the backup, but it will leave any other collection untouched. Meaning you cannot
merge 2 collections with this tool.

* Setting up a replica set

``` shell
mongo-backup replica --set-name myRepSet --primary node1-db.com:27017 --secondary node2-db.com:27017,node3-db.com:27018
```

This will set up a replica set, using the server provided with `--primary` as
the primary node and all the servers provided with `--secondary` as secondary
nodes. 
Note: You still need to configure the servers themselves with the replSet name,
either as a start parameter or in the configuration files. (see [here](https://docs.mongodb.com/manual/tutorial/deploy-replica-set/))

