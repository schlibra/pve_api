class Directory:
    def __init__(self):
        self.device = None
        self.options = None
        self.path = None
        self.type = None
        self.unifile = None

    def __str__(self):
        return f"Directory [device={self.device}, options={self.options}, path={self.path}, type={self.type}, unifile={self.unifile}]"