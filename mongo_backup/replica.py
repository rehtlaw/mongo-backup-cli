from pymongo import MongoClient

# initialize a replica set (see docs, requires some database-side configuration as well)
def init_replica(replica_name, primary_node, secondary_nodes):
    '''
    @replica_name[string]: name of the replica set, which is set in the database configuration file (has to be the same on all servers)
    @primary_node[string]: domain or IP to the primary mongodb instance, where the replica set will be initiated
    @secondary_nodes[[]string]: list of other domains/IPs of other mongodb instances that will be the slaves/backup instances once the main node goes down
    '''
    # connect to main mongodb
    client = MongoClient(primary_node)

    # create list of all members
    members = [{'_id': 0, 'host': primary_node}]
    nodes = list(enumerate(secondary_nodes, start=1))
    for node in sec_nodes:
        members.append({'_id': node[0], 'host': node[1]})

    config = {'_id': replica_name, 'members': members}

    # send the list of replica servers to the main mongodb
    return client.admin.command('replSetInitiate', config)
