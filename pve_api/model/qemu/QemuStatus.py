from enum import Enum


class QemuStatusEnum(Enum):
    STOPPED = "stopped"
    RUNNING = "running"

class QemuStatus:
    def __init__(self):
        self.mem = None
        self.netout = None
        self.vmid = None
        self.status = None
        self.disk = None
        self.ha = None
        self.proxmox_support = None
        self.nics = None
        self.cpus = None
        self.pid = None
        self.running_machine = None
        self.running_qemu = None
        self.blockstat = None
        self.ballooninfo = None
        self.freemem = None
        self.maxmem = None
        self.maxdisk = None
        self.netin = None
        self.cpu = None
        self.uptime = None
        self.diskwrite = None
        self.name = None
        self.diskread = None
        self.balloon = None
        self.qmpstatus = None

    def __str__(self):
        if 'proxmox_support' not in self.__dict__:
            self.proxmox_support = ''
        if 'nics' not in self.__dict__:
            self.nics = ''
        if 'cpus' not in self.__dict__:
            self.cpus = ''
        if 'pid' not in self.__dict__:
            self.pid = ''
        if 'running_machine' not in self.__dict__:
            self.running_machine = ''
        if 'running_qemu' not in self.__dict__:
            self.running_qemu = ''
        if 'blockstat' not in self.__dict__:
            self.blockstat = ''
        if 'ballooninfo' not in self.__dict__:
            self.ballooninfo = ''
        if 'freemem' not in self.__dict__:
            self.freemem = ''
        if'maxmem' not in self.__dict__:
            self.maxmem = ''
        if'maxdisk' not in self.__dict__:
            self.maxdisk = ''
        if 'netin' not in self.__dict__:
            self.netin = ''
        if 'cpu' not in self.__dict__:
            self.cpu = ''
        if 'uptime' not in self.__dict__:
            self.uptime = ''
        if 'diskwrite' not in self.__dict__:
            self.diskwrite = ''
        if 'name' not in self.__dict__:
            self.name = ''
        if 'diskread' not in self.__dict__:
            self.diskread = ''
        if 'balloon' not in self.__dict__:
            self.balloon = ''
        if 'qmpstatus' not in self.__dict__:
            self.qmpstatus = ''
        return f"QemuStatus [mem={self.mem}, netout={self.netout}, vmid={self.vmid}, status={self.status}, disk={self.disk}, ha={self.ha}, proxmox_support={self.proxmox_support}, nics={self.nics}, cpus={self.cpus}, pid={self.pid}, running_machine={self.running_machine}, running_qemu={self.running_qemu}, blockstat={self.blockstat}, ballooninfo={self.ballooninfo}, freemem={self.freemem}, maxmem={self.maxmem}, maxdisk={self.maxdisk}, netin={self.netin}, cpu={self.cpu}, uptime={self.uptime}, diskwrite={self.diskwrite}, name={self.name}, diskread={self.diskread}, balloon={self.balloon}, qmpstatus={self.qmpstatus}]"
