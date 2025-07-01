class AptPackage:
    def __init__(self):
        self.Section = None
        self.Package = None
        self.Origin = None
        self.Version = None
        self.Priority = None
        self.Description = None
        self.Title = None
        self.Arch = None
        self.OldVersion = None

    def __str__(self):
        if 'OldVersion' not in self.__dict__:
            self.OldVersion = ""
        return f"AptPackage [Section={self.Section}, Package={self.Package}, Origin={self.Origin}, Version={self.Version}, Priority={self.Priority}, Description={self.Description}, Title={self.Title}, Arch={self.Arch}, OldVersion={self.OldVersion}]"