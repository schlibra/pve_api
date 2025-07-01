class QemuCPU:
    def __init__(self):
        self.name = None
        self.custom = None
        self.vendor = None

    def __str__(self):
        return f"QemuCPU [name={self.name}, custom={self.custom}, vendor={self.vendor}]"