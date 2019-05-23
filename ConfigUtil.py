import json

default_options = {
    'beta_features': False
}


# add to the server config when a bot joins a new server
def add_server(server_id, server_list):
    # Checks for duplicates
    for s_id in server_list.keys():
        if s_id == server_id:
            return

    server_list[server_id] = default_options

    # Write to file
    with open("serveropts.json", "w") as config:
        config.write(json.dumps({"servers": server_list}, indent=1))
        config.close()


# reads in the config
def get_servers():
    with open("serveropts.json", "r") as config:
        servers = json.load(config)

    return servers["servers"]
