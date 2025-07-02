from pve_api.model.qemu.QemuStatus import QemuStatus, QemuStatusEnum


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
        self.__pve = None
        self.__node = None

    def __str__(self):
        if 'template' not in self.__dict__:
            self.template = ''
        return f"QemuItem [cpus={self.cpus}, diskwrite={self.diskwrite}, cpu={self.cpu}, netin={self.netin}, uptime={self.uptime}, name={self.name}, diskread={self.diskread}, vmid={self.vmid}, mem={self.mem}, netout={self.netout}, disk={self.disk}, template={self.template}, maxmem={self.maxmem}, maxdisk={self.maxdisk}, status={self.status}]"

    def get_status(self):
        res = self.__pve._PVE__get(f"/nodes/{self.__node}/qemu/{self.vmid}/status/current")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _qemu_status = res.json()['data']
                if 'proxmox-support' in _qemu_status:
                    _qemu_status['proxmox_support'] = _qemu_status.pop('proxmox-support')
                if 'running-machine' in _qemu_status:
                    _qemu_status['running_machine'] = _qemu_status.pop('running-machine')
                if 'running-qemu' in _qemu_status:
                    _qemu_status['running_qemu'] = _qemu_status.pop('running-qemu')
                _qemu_status['status'] = QemuStatusEnum(_qemu_status['status'])
                qemu_status = QemuStatus()
                qemu_status.__dict__ = _qemu_status
                return qemu_status
            else:
                raise Exception(res)
        else:
            raise Exception(res)