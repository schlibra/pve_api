class QemuMachine:
    def __init__(self):
        self.version = None
        self.type = None
        self.changes = None
        self.id = None

    def __str__(self):
        if 'changes' not in self.__dict__:
            self.changes = ''
        return f"QemuMachine [id={self.id}, version={self.version}, type={self.type}, changes={self.changes}]"