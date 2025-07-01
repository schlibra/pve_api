class PveNode:
    def __init__(self):
        self.ssl_fingerprint = None
        self.maxdisk = None
        self.id = None
        self.status = None
        self.mem = None
        self.type = None
        self.cpu = None
        self.uptime = None
        self.level = None
        self.node = None
        self.disk = None
        self.maxmem = None

    def __str__(self):
        return f"PveNode: [id={self.id}, status={self.status}, type={self.type}, level={self.level}, node={self.node}, mem={self.mem}, cpu={self.cpu}, disk={self.disk}, maxdisk={self.maxdisk}, maxmem={self.maxmem}, uptime={self.uptime}, ssl_fingerprint={self.ssl_fingerprint}]"



