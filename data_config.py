
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
        _data_type = {1:'b', 2:'B', 3:'h', 4:'H', 5:'i', 6:'I', 7:'f', 9:'d', 12:'q', 13:'Q'}
        _data_size = {1:1, 2:1, 3:2, 4:2, 5:4, 6:4, 7:4, 9:8, 12:8, 13:8}
        # <: little-endian, 
        '''
        x: pad byte (no data); c:char; b:signed byte; B:unsigned byte;
        ?: _Bool (requires C99; if not available, char is used instead)
        h:short; H:unsigned short; i:int; I:unsigned int;
        l:long; L:unsigned long; f:float; d:double.
        Special case (not in native mode unless 'long long' in platform C):
        q:long long; Q:unsigned long long
        '''
        
        self.config = [];    # dummy for config list
        unused_counter = 0;
        for line in self.lines:
            var_config = line.strip().split()
            if len(var_config) == 3:
                var_name = var_config[0]
                var_type = _data_type[int(var_config[1])]
                var_width = _data_size[int(var_config[1])]
                var_length = int(var_config[2])
                var_config = var_name, var_width, var_length, var_type
                self.config.append(var_config)
            if len(var_config) == 2:
                var_name = var_config[0]
                if var_name != "unused":
                    raise RuntimeError('Wrong name for unused bytes!')
                var_width = 1
                var_length = int(var_config[1])
                var_name = '{}_{}'.format(var_name,  unused_counter)
                unused_counter = unused_counter + 1
                var_config = var_name, var_width, var_length, 'B'
                self.config.append(var_config)
        return self.config

    def GetDataPacketLength(self):
        self.packet_length = 0
        for item in self.config:
            self.packet_length = self.packet_length + item[1] * item[2]
        return self.packet_length
