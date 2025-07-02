# ProxmoxVE Web API
这个项目是ProxmoxVE Web API的Python库

## 安装
```
pip install pve-api
```

## 示例
```python
from pve_api import PVE

# 创建PVE对象
pve = PVE('192.168.1.100', 'root', 'password')
# 获取主节点
node = pve.get_nodes().query('node', 'pve')
# 获取当前节点下的qemu虚拟机中名为debian的虚拟机
qemu = node.get_qemu().query('name', 'debian')
# 获取虚拟机当前状态
status = qemu.get_status()
# 输出虚拟机当前状态
print(status)
```
## 链式操作
```python
from pve_api import PVE

print(PVE('192.168.1.100', 'root', 'password').get_nodes().query('node', 'pve').get_qemu().query('name', 'debian').get_status().status)
```
> ### 输出：
> QemuStatusEnum.STOPPED