# ProxmoxVE Web API
这个项目是ProxmoxVE Web API的Python库

## 安装
```
pip install pve-api
```
> 该方法暂不支持

## 示例
```python
from pve_api import PVE

# 创建PVE对象
pve = PVE('192.168.1.100', 'root', 'password')
# 获取主节点
node = pve.get_nodes().query('node', 'pve')
# 获取当前节点下的qemu虚拟机中名为Windows的虚拟机
qemu = pve.get_node_qemu(node).query('name', 'Windows')
# 输出虚拟机信息对象
print(qemu)
```
> ### 输出：
> QemuItem [cpus=1, diskwrite=0, cpu=0.0807287315007847, netin=122048440, uptime=28161, name=Router, diskread=0, vmid=201, mem=480493425, netout=138588369, disk=0, template=, maxmem=2147483648, maxdisk=34359738368, status=running]