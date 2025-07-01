class Certificate:
    def __init__(self):
        self.filename = None
        self.fingerprint = None
        self.issuer = None
        self.notafter = None
        self.pem = None
        self.public_key_bits = None
        self.public_key_type = None
        self.san = None
        self.subject = None

    def __str__(self):
        return f"Certificate [filename={self.filename}, fingerprint={self.fingerprint}, issuer={self.issuer}, notafter={self.notafter}, subject={self.subject}, san={self.san}, pem={self.pem}, public-key-bits={self.public_key_bits}, public-key-type={self.public_key_type}]"