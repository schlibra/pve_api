class LocalDisk:
    def __init__(self):
        self.osdid_list = None
        self.vendor = None
        self.by_id_link = None
        self.gpt = None
        self.osdid = None
        self.health = None
        self.wwn = None
        self.serial = None
        self.size = None
        self.used = None
        self.devpath = None
        self.model = None
        self.rpm = None
        self.wearout = None
        self.type = None
        self.parent = None

    def __str__(self):
        if 'osdid_list' not in self.__dict__:
            self.osdid_list = ""
        if 'parent' not in self.__dict__:
            self.parent = ""
        if 'vendor' not in self.__dict__:
            self.vendor = ""
        if 'by_id_link' not in self.__dict__:
            self.by_id_link = ""
        if 'gpt' not in self.__dict__:
            self.gpt = ""
        if 'osdid' not in self.__dict__:
            self.osdid = ""
        if 'health' not in self.__dict__:
            self.health = ""
        if 'wwn' not in self.__dict__:
            self.wwn = ""
        if'serial' not in self.__dict__:
            self.serial = ""
        if'size' not in self.__dict__:
            self.size = ""
        if 'used' not in self.__dict__:
            self.used = ""
        if 'devpath' not in self.__dict__:
            self.devpath = ""
        if 'model' not in self.__dict__:
            self.model = ""
        if 'rpm' not in self.__dict__:
            self.rpm = ""
        if 'wearout' not in self.__dict__:
            self.wearout = ""
        return f"LocalDisk [osdid_list={self.osdid_list}, vendor={self.vendor}, by_id_link={self.by_id_link}, gpt={self.gpt}, osdid={self.osdid}, health={self.health}, wwn={self.wwn}, serial={self.serial}, size={self.size}, used={self.used}, devpath={self.devpath}, model={self.model}, rpm={self.rpm}, wearout={self.wearout}, type={self.type}, parent={self.parent}]"