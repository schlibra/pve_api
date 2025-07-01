from load_info import load_info
from pve_api import PVE

if __name__ == '__main__':
    host, username, password = load_info()
    pve = PVE(host, username, password)
    node = pve.get_nodes(size_convert=True).query(key='node', value='pve')
    qemu = pve.get_node_qemu(node=node).query(key='name', value='Router')
    print(qemu)