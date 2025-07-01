from load_info import load_info
from pve_api import PVE

if __name__ == '__main__':
    host, username, password = load_info()
    pve = PVE(host, username, password)
    node = pve.get_nodes(True).query('node', 'pve')
    qemu_list = pve.get_node_qemu(node, True).query_all('status', 'running')
    for qemu in qemu_list:
        print(qemu)
