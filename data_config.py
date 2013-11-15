
config_fname = "config_2.txt"     # name of configuration file

# get config strings
config_file = open(config_fname, "rt")
lines = config_file.readlines()
config_file.close()

#get config list
config = [];    # dummy for config list
for line in lines:
    var_config = line.strip().split()
    if len(var_config) == 3:
        var_name = var_config[0]
        var_width = int(var_config[1]) - 1
        var_length = int(var_config[2])
        var_config = var_name, var_width, var_length
        config.append(var_config)
    if len(var_config) == 2:
        var_name = var_config[0]
        if var_name != "unused":
            raise RuntimeError('Wrong name for unused bytes!')
        var_width = 1
        var_length = int(var_config[1])
        var_config = var_name, var_width, var_length
        config.append(var_config)

#get data packet length
packet_length = 0
for item in config:
    packet_length = packet_length + item[1] * item[2]

#print("%dd %xh" % (packet_length, packet_length))



