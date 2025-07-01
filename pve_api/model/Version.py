class Version:
    def __init__(self):
        self.repoid = None
        self.version = None
        self.release = None

    def __str__(self):
        return f"Version [repoid={self.repoid}, version={self.version}, release={self.release}]"