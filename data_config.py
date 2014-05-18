


class DataConfig:
    def __init__(self, fname):
        self.config_fname = fname
        self.GetConfigStrings()
        self.GetConfigList()
        self.GetDataPacketLength()

    def GetConfigStrings(self):
        self.config_file = open(self.config_fname, "rt")
        self.lines = self.config_file.readlines()
        self.config_file.close()

    def GetConfigList(self):
        self.config = [];    # dummy for config list
        for line in self.lines:
            var_config = line.strip().split()
            if len(var_config) == 3:
                var_name = var_config[0]
                var_width = int(var_config[1]) - 1
                var_length = int(var_config[2])
                var_config = var_name, var_width, var_length
                self.config.append(var_config)
            if len(var_config) == 2:
                var_name = var_config[0]
                if var_name != "unused":
                    raise RuntimeError('Wrong name for unused bytes!')
                var_width = 1
                var_length = int(var_config[1])
                var_config = var_name, var_width, var_length
                self.config.append(var_config)
        return self.config

    def GetDataPacketLength(self):
        self.packet_length = 0
        for item in self.config:
            self.packet_length = self.packet_length + item[1] * item[2]
        return self.packet_length
