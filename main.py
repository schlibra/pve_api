from load_info import load_info
from pve_api import PVE

if __name__ == '__main__':
    host, username, password = load_info()
    pve: PVE = PVE(host, username, password)
    node = pve.get_nodes().query('node', 'pve')
    qemu = node.get_qemu().query('name', 'debian')
    status = qemu.get_status()
    print(status.status)

