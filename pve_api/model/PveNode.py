from pve_api.model.qemu.QemuItem import QemuItem
from pve_api.model.MyList import MyList
from pve_api.exception import RequestException
from pve_api.util import to_string_size


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
        self.__pve = None

    def __str__(self):
        return f"PveNode: [id={self.id}, status={self.status}, type={self.type}, level={self.level}, node={self.node}, mem={self.mem}, cpu={self.cpu}, disk={self.disk}, maxdisk={self.maxdisk}, maxmem={self.maxmem}, uptime={self.uptime}, ssl_fingerprint={self.ssl_fingerprint}]"

    def get_qemu(self, convert_size: bool = False):
        res = self.__pve._PVE__get(f"/nodes/{self.node}/qemu")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for qemu in res.json()['data']:
                    if convert_size:
                        qemu["netin"] = to_string_size(qemu["netin"])
                        qemu["netout"] = to_string_size(qemu["netout"])
                        qemu["mem"] = to_string_size(qemu["mem"])
                        qemu["maxmem"] = to_string_size(qemu["maxmem"])
                        qemu["maxdisk"] = to_string_size(qemu["maxdisk"])
                    _qemu = QemuItem()
                    _qemu.__dict__ = qemu
                    _qemu._QemuItem__pve = self.__pve
                    _qemu._QemuItem__node = self.node
                    _data.append(_qemu)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

