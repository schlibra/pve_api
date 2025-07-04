import requests
import urllib3

from .exception import *
from .model.PveNode import PveNode
from .model.Version import Version
from .model.MyList import MyList
from .model.QemuCPU import QemuCPU
from .model.Network import Network
from .model.QemuMachine import QemuMachine
from .model.Directory import Directory
from .model.AptPackage import AptPackage
from .model.Certificate import Certificate
from .model.LvmThin import LvmThin
from .model.LocalDisk import LocalDisk
from .model.ZfsPool import ZfsPool
from .util.SizeConvert import *


class PVE:
    login = False
    def __build_url__(self, path, api_prefix="/api2/extjs"):
        return f"https://{self.host}:8006{api_prefix}{path}"

    def __get(self, path, headers=None, verify=False, api_prefix="/api2/extjs", **kwargs):
        if self.login:
            return requests.get(self.__build_url__(path, api_prefix), verify=verify, headers=headers, cookies={
                'PVEAuthCookie': self.ticket
            }, **kwargs)
        else:
            return requests.get(self.__build_url__(path), verify=verify, headers=headers, **kwargs)

    def __delete(self, path, headers=None, verify=False, api_prefix="/api2/extjs", **kwargs):
        if self.login:
            return requests.delete(self.__build_url__(path, api_prefix), verify=verify, headers=headers, cookies={
                'PVEAuthCookie': self.ticket
            }, **kwargs)
        else:
            return requests.delete(self.__build_url__(path), verify=verify, headers=headers, **kwargs)

    def __post(self, path, data=None, headers=None, verify=False, api_prefix="/api2/extjs", **kwargs):
        if self.login:
            return requests.post(self.__build_url__(path, api_prefix), data=data, verify=verify, headers=headers, cookies={
                'PVEAuthCookie': self.ticket
            }, **kwargs)
        else:
            return requests.post(self.__build_url__(path), data=data, verify=verify, headers=headers, **kwargs)

    def __put(self, path, data=None, headers=None, verify=False, api_prefix="/api2/extjs", **kwargs):
        if self.login:
            return requests.put(self.__build_url__(path, api_prefix), data=data, verify=verify, headers=headers, cookies={
                'PVEAuthCookie': self.ticket
            }, **kwargs)
        else:
            return requests.put(self.__build_url__(path), data=data, verify=verify, headers=headers, **kwargs)

    def __init__(self, host, username, password):
        urllib3.disable_warnings()
        self.host = host
        self.username = username
        self.password = password
        res = self.__post("/access/ticket", {
            "username": self.username,
            "password": self.password,
            "realm": "pam",
            "new-format": 1
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                self.ticket = res.json()['data']['ticket']
                self.login = True
            else:
                raise AuthorizationException(res)
        else:
            raise AuthorizationException("Authorization failed")

    def version(self):
        res = self.__get("/version")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _version = Version()
                _version.__dict__ = res.json()['data']
                return _version
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_nodes(self, size_convert=False):
        res = self.__get("/nodes")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for node in res.json()['data']:
                    _node = PveNode()
                    _node.__dict__ = node
                    _node._PveNode__pve = self
                    if size_convert:
                        _node.mem = to_string_size(_node.mem)
                        _node.disk = to_string_size(_node.disk)
                        _node.maxmem = to_string_size(_node.maxmem)
                        _node.maxdisk = to_string_size(_node.maxdisk)
                    _data.append(_node)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_apt_changelog(self, node: PveNode, package: str):
        res = self.__get(f"/nodes/{node.node}/apt/changelog?name={package}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_apt_repositories(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/apt/repositories")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_apt_repository(self, node: PveNode, index: int, path: str, digest: str="", enabled: bool=True):
        res = self.__post(f'/nodes/{node.node}/apt/repositories', {
            "index": index,
            "path": path,
            "digest": digest,
            "enabled": enabled
        }, api_prefix="/api2/json")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def update_node_apt_repository(self, node: PveNode, handle: str, digest: str=""):
        res = self.__put(f'/nodes/{node.node}/apt/repositories', {
            "digest": digest,
            "handle": handle
        }, api_prefix="/api2/json")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_apt_update(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/apt/update")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _list = []
                for pkg in res.json()['data']:
                    package = AptPackage()
                    package.__dict__ = pkg
                    _list.append(package)
                return MyList(_list)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_apt_update(self, node: PveNode, notify: bool=False, quiet: bool=False):
        res = self.__post(f"/nodes/{node.node}/apt/update", {
            "notify": notify,
            "quiet": quiet
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_apt_versions(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/apt/versions")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for version in res.json()['data']:
                    _version = AptPackage()
                    _version.__dict__ = version
                    _data.append(_version)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_capabilities_qemu_cpu(self, node: PveNode, custom: bool=False, name: str="", vendor: str="", features: str=""):
        res = self.__get(f"/nodes/{node.node}/capabilities/qemu/cpu")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for cpu in res.json()['data']:
                    _cpu = QemuCPU()
                    _cpu.__dict__ = cpu
                    _data.append(_cpu)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_capabilities_qemu_machines(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/capabilities/qemu/machines")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for machine in res.json()['data']:
                    _machine = QemuMachine()
                    _machine.__dict__ = machine
                    _data.append(_machine)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_cfg_db(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/cfg/db")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_cfg_raw(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/cfg/raw")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_cfg_value(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/cfg/value")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_fs(self, node: PveNode, name: str="cephfs", add_storage: bool=False, pg_num: int=128):
        res = self.__post(f"/nodes/{node.node}/ceph/fs/{name}", {
            "add_storage": add_storage,
            "pg_num": pg_num
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_mds(self, node: PveNode, name: str="nodename", hotstandby: bool=False):
        res = self.__post(f"/nodes/{node.node}/ceph/mds/{name}", {
            "hotstandby": hotstandby
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_ceph_mds(self, node: PveNode, name: str):
        res = self.__delete(f"/nodes/{node.node}/ceph/mds/{name}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_mgr(self, node: PveNode, _id: str=""):
        res = self.__post(f"/nodes/{node.node}/ceph/mgr/{_id}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_ceph_mgr(self, node: PveNode, _id: str):
        res = self.__delete(f"/nodes/{node.node}/ceph/mgr/{_id}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_mon(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/mon")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_mon(self, node: PveNode, mon_address: str="", monid: str=""):
        res = self.__post(f"/nodes/{node.node}/ceph/mon/{monid}", {
            "mon_address": mon_address
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_ceph_mon(self, node: PveNode, monid: str):
        res = self.__delete(f"/nodes/{node.node}/ceph/mon/{monid}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_osd(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/osd")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_osd(self, node: PveNode, dev: str, crush_device_class: str="", db_dev: str="", db_dev_size: int=0, encrypted: bool=False, osds_per_device: str="", wal_dev: str="", wal_dev_size: int=0):
        res = self.__post(f"/nodes/{node.node}/ceph/osd", {
            "dev": dev,
            "crush-device-class": crush_device_class,
            "db_dev": db_dev,
            "db_dev_size": db_dev_size,
            "encrypted": encrypted,
            "osds-per-device": osds_per_device,
            "wal_dev": wal_dev,
            "wal_dev_size": wal_dev_size
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_ceph_osd(self, node: PveNode, osdid: int, cleanup: bool=False):
        res = self.__delete(f"/nodes/{node.node}/ceph/osd/{osdid}?cleanup={cleanup}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_osd_in(self, node: PveNode, osdid: int):
        res = self.__post(f"/nodes/{node.node}/ceph/osd/{osdid}/in")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_osd_lv_info(self, node: PveNode, osdid: int, _type: str=""):
        res = self.__get(f"/nodes/{node.node}/ceph/osd/{osdid}/lv_info?type={_type}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_osd_metadata(self, node: PveNode, osdid: int, devices=None, osd=None):
        if osd is None:
            osd = {}
        if devices is None:
            devices = []
        res = self.__post(f"/nodes/{node.node}/ceph/osd/{osdid}/metadata", {
            "devices": devices,
            "osd": osd
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_osd_out(self, node: PveNode, osdid: int):
        res = self.__post(f"/nodes/{node.node}/ceph/osd/{osdid}/out")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_osd_scrub(self, node: PveNode, osdid: int, deep: bool=False):
        res = self.__post(f"/nodes/{node.node}/ceph/osd/{osdid}/scrub", {
            "deep": deep
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_pool(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/pool")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_ceph_pool(self, node: PveNode, name: str, add_storages: bool=False, application: str="", crush_rule: str="", erasure_coding: str="", min_size: str="",pg_autoscale_mode: str="warn", pg_num: int=128, pg_num_min: int = 0, size: int=3, target_size: str="", targer_size_ratio: int=0):
        res = self.__post(f"/nodes/{node.node}/ceph/pool", {
            "add_storages": add_storages,
            "application": application,
            "crush_rule": crush_rule,
            "erasure_coding": erasure_coding,
            "min_size": min_size,
            "pg_autoscale_mode": pg_autoscale_mode,
            "pg_num": pg_num,
            "pg_num_min": pg_num_min,
            "size": size,
            "target_size": target_size,
            "targer_size_ratio": targer_size_ratio,
            "name": name
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def update_node_ceph(self, node: PveNode, name: str, application: str="", crush_rule: str="", min_size: str="", pg_autoscale_mode: str="warn", pg_num: int=128, pg_num_min: int = 0, size: int=3, target_size: str="", targer_size_ratio: int=0):
        res = self.__put(f"/nodes/{node.node}/ceph/pool/{name}", {
            "application": application,
            "crush_rule": crush_rule,
            "min_size": min_size,
            "pg_autoscale_mode": pg_autoscale_mode,
            "pg_num": pg_num,
            "pg_num_min": pg_num_min,
            "size": size,
            "target_size": target_size,
            "targer_size_ratio": targer_size_ratio
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_ceph_pool(self, node: PveNode, name: str, force: bool=False, remove_ecprofile: bool=True, remove_storages: bool=True):
        res = self.__delete(f"/nodes/{node.node}/ceph/pool/{name}?force={force}&remove_ecprofile={remove_ecprofile}&remove_storages={remove_storages}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_pool_status(self, node: PveNode, name: str, verbose: bool=False):
        res = self.__get(f"/nodes/{node.node}/ceph/pool/{name}/status?verbose={verbose}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_cmd_safety(self, node: PveNode, action: str, _id: str, service: str):
        res = self.__get(f"/nodes/{node.node}/ceph/cmd_safety?action={action}&id={_id}&service={service}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_crush(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/crush")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_init(self, node: PveNode, cluster_network: str="", disable_cephx: bool=False, min_size: str="", network: str="", pg_bits: int=6, size: int=3):
        res = self.__post(f"/nodes/{node.node}/ceph/init", {
            "cluster_network": cluster_network,
            "disable_cephx": disable_cephx,
            "min_size": min_size,
            "network": network,
            "pg_bits": pg_bits,
            "size": size
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_log(self, node: PveNode, limit: int=0, start: int=0):
        res = self.__get(f"/nodes/{node.node}/ceph/log?limit={limit}&start={start}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_restart(self, node: PveNode):
        res = self.__post(f"/nodes/{node.node}/ceph/restart")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_rules(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/rules")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_start(self, node: PveNode):
        res = self.__post(f"/nodes/{node.node}/ceph/start")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_ceph_status(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/ceph/status")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_ceph_stop(self, node: PveNode, service: str=""):
        res = self.__post(f"/nodes/{node.node}/ceph/stop", {
            "service": service
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_certificates(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/certificates")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_certificates_acme(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/certificates/acme")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_certificates_acme_certificate(self, node: PveNode, force: bool=False):
        res = self.__post(f"/nodes/{node.node}/certificates/acme/certificate?force={force}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_certificates_acme_certificate_renew(self, node: PveNode, force: bool=False):
        res = self.__post(f"/nodes/{node.node}/certificates/acme/certificate?force={force}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_certificates_acme_certificate(self, node: PveNode):
        res = self.__delete(f"/nodes/{node.node}/certificates/acme/certificate")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_certificates_custom(self, node: PveNode, certificates: str, key: str="", force: bool=False, restart: bool=False):
        res = self.__post(f"/nodes/{node.node}/certificates/custom", {
            "certificates": certificates,
            "ket": key,
            "force": force,
            "restart": restart
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_certificates_info(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/certificates/info")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for _certificate in res.json()['data']:
                    _certificate["public_key_bits"] = _certificate.pop("public-key-bits")
                    _certificate["public_key_type"] = _certificate.pop("public-key-type")
                    certificate = Certificate()
                    certificate.__dict__ = _certificate
                    _data.append(certificate)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_directory(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/disks/directory")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for directory in res.json()['data']:
                    _directory = Directory()
                    _directory.__dict__ = directory
                    _data.append(_directory)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_disks_directory(self, node: PveNode, name: str, device: str, add_storage: bool=False, filesystem: str="ext4"):
        res = self.__post(f"/nodes/{node.node}/disks/directory", {
            "name": name,
            "device": device,
            "add_storage": add_storage,
            "filesystem": filesystem
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_disks_directory(self, node: PveNode, name: str, cleanup_config: bool=False, cleanup_disks: bool=False):
        res = self.__delete(f"/nodes/{node.node}/disks/directory/{name}?cleanup-config={cleanup_config}&cleanup-disks={cleanup_disks}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_lvm(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/disks/lvm")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_disks_lvm(self, node: PveNode, name: str, device: str, add_storage: bool=False):
        res = self.__post(f"/nodes/{node.node}/disks/lvm", {
            "name": name,
            "device": device,
            "add_storage": add_storage
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_disks_lvm(self, node: PveNode, name: str, cleanup_config: bool=False, cleanup_disks: bool=False):
        res = self.__delete(f"/nodes/{node.node}/disks/lvm/{name}?cleanup-config={cleanup_config}&cleanup-disks={cleanup_disks}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_lvmthin(self, node: PveNode, convert_size: bool=False):
        res = self.__get(f"/nodes/{node.node}/disks/lvmthin")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for lvmthin in res.json()['data']:
                    if convert_size:
                        lvmthin["lv_size"] = to_string_size(lvmthin["lv_size"])
                        lvmthin["metadata_size"] = to_string_size(lvmthin["metadata_size"])
                        lvmthin["metadata_used"] = to_string_size(lvmthin["metadata_used"])
                        lvmthin["used"] = to_string_size(lvmthin["used"])
                    _lvmthin = LvmThin()
                    _lvmthin.__dict__ = lvmthin
                    _data.append(_lvmthin)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_disks_lvmthin(self, node: PveNode, name: str, device: str, add_storage: bool=False):
        res = self.__post(f"/nodes/{node.node}/disks/lvmthin", {
            "name": name,
            "device": device,
            "add_storage": add_storage
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_disks_lvmthin(self, node: PveNode, name: str, volume_group: str, cleanup_config: bool=False, cleanup_disks: bool=False):
        res = self.__delete(f"/nodes/{node.node}/disks/lvmthin/{name}?volume-group={volume_group}&cleanup-config={cleanup_config}&cleanup-disks={cleanup_disks}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_zfs(self, node: PveNode, convert_size: bool=False):
        res = self.__get(f"/nodes/{node.node}/disks/zfs")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for zfs in res.json()['data']:
                    if convert_size:
                        zfs["free"] = to_string_size(zfs["free"])
                        zfs["size"] = to_string_size(zfs["size"])
                    _zfs = ZfsPool()
                    _zfs.__dict__ = zfs
                    _data.append(_zfs)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def add_node_disks_zfs(self, node: PveNode, devices: str, name: str, raidlevel: str, add_storage: bool=False, ashift: int=12, compression: str="on", draid_config: str=""):
        res = self.__post(f"/nodes/{node.node}/disks/zfs", {
            "devices": devices,
            "name": name,
            "raidlevel": raidlevel,
            "add_storage": add_storage,
            "ashift": ashift,
            "compression": compression,
            "draid_config": draid_config
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_zfs_info(self, node: PveNode, name: str):
        res = self.__get(f"/nodes/{node.node}/disks/zfs/{name}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def delete_node_disks_zfs(self, node: PveNode, name: str, cleanup_config: bool=False, cleanup_disks: bool=False):
        res = self.__delete(f"/nodes/{node.node}/disks/zfs/{name}?cleanup-config={cleanup_config}&cleanup-disks={cleanup_disks}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_disks_initgpt(self, node: PveNode, disk: str, uuid: str=""):
        res = self.__post(f"/nodes/{node.node}/disks/initgpt", {
            "disk": disk,
            "uuid": uuid
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_list(self, node: PveNode, include_partitions: bool=False, skipsmart: bool=False, _type: str="journal_disks", convert_size: bool=False):
        res = self.__get(f"/nodes/{node.node}/disks/list?include-partitions={int(include_partitions)}&skipsmart={int(skipsmart)}&type={_type}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for disk in res.json()['data']:
                    if convert_size:
                        disk['size'] = to_string_size(disk['size'])
                    _disk = LocalDisk()
                    _disk.__dict__ = disk
                    _data.append(_disk)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_disks_smart(self, node: PveNode, disk: LocalDisk, healthonly: bool=False):
        res = self.__get(f"/nodes/{node.node}/disks/smart?disk={disk.devpath}&healthonly={int(healthonly)}")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def do_node_disks_wipedisk(self, node: PveNode, disk: str):
        res = self.__put(f"/nodes/{node.node}/disks/wipedisk", {
            "disk": disk
        })
        if res.status_code == 200:
            if res.json()['success'] == 1:
                return res.json()['data']
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

    def get_node_network(self, node: PveNode):
        res = self.__get(f"/nodes/{node.node}/network")
        if res.status_code == 200:
            if res.json()['success'] == 1:
                _data = []
                for network in res.json()['data']:
                    _network = Network()
                    _network.__dict__ = network
                    _data.append(_network)
                return MyList(_data)
            else:
                raise RequestException(res)
        else:
            raise RequestException(res)

