class LvmThin:
    def __init__(self):
        self.lv = None
        self.lv_size = None
        self.vg = None
        self.metadata_size = None
        self.metadata_used = None
        self.used = None

    def __str__(self):
        return f"LvmThin [lv={self.lv}, lv_size={self.lv_size}, vg={self.vg}, metadata_size={self.metadata_size}, metadata_used={self.metadata_used}, used={self.used}]"