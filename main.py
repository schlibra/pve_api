from load_info import load_info
from pve_api import PVE, LocalDisk

if __name__ == '__main__':
    host, username, password = load_info()
    pve = PVE(host, username, password)
    node = pve.get_nodes(True).query('node', 'pve')
    disks = pve.get_node_disks_list(node, include_partitions=True)
    for disk in disks:
        disk: LocalDisk
        smart = pve.get_node_disks_smart(node, disk)
        print(smart)
