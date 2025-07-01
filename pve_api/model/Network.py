class Network:
    def __init__(self):
        self.bridge_stp = None
        self.method = None
        self.families = None
        self.autostart = None
        self.iface = None
        self.priority = None
        self.method6 = None
        self.active = None
        self.bridge_ports = None
        self.cidr = None
        self.type = None
        self.netmask = None
        self.address = None
        self.bridge_fd = None

    def __str__(self):
        if 'bridge_stp' not in self.__dict__:
            self.bridge_stp = ""
        if 'bridge_ports' not in self.__dict__:
            self.bridge_ports = ""
        if 'bridge_fd' not in self.__dict__:
            self.bridge_fd = ""
        if'method' not in self.__dict__:
            self.method = ""
        if 'families' not in self.__dict__:
            self.families = ""
        if 'autostart' not in self.__dict__:
            self.autostart = ""
        if 'iface' not in self.__dict__:
            self.iface = ""
        if 'priority' not in self.__dict__:
            self.priority = ""
        if'method6' not in self.__dict__:
            self.method6 = ""
        if 'active' not in self.__dict__:
            self.active = ""
        if 'cidr' not in self.__dict__:
            self.cidr = ""
        if 'netmask' not in self.__dict__:
            self.netmask = ""
        if 'address' not in self.__dict__:
            self.address = ""
        return f"Network [bridge_stp={self.bridge_stp}, method={self.method}, families={self.families}, autostart={self.autostart}, iface={self.iface}, priority={self.priority}, method6={self.method6}, active={self.active}, bridge_ports={self.bridge_ports}, cidr={self.cidr}, type={self.type}, netmask={self.netmask}, address={self.address}, bridge_fd={self.bridge_fd}]"
