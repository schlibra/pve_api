class QemuItem:
    def __init__(self):
        self.cpus = None
        self.diskwrite = None
        self.cpu = None
        self.netin = None
        self.uptime = None
        self.name = None
        self.diskread = None
        self.vmid = None
        self.mem = None
        self.netout = None
        self.disk = None
        self.template = None
        self.maxmem = None
        self.maxdisk = None
        self.status = None

    def __str__(self):
        if 'template' not in self.__dict__:
            self.template = ''
        return f"QemuItem [cpus={self.cpus}, diskwrite={self.diskwrite}, cpu={self.cpu}, netin={self.netin}, uptime={self.uptime}, name={self.name}, diskread={self.diskread}, vmid={self.vmid}, mem={self.mem}, netout={self.netout}, disk={self.disk}, template={self.template}, maxmem={self.maxmem}, maxdisk={self.maxdisk}, status={self.status}]"
