class StreamConfig:
    def __init__(self, config):
        self.protocol = config.get("protocol")
        self.ip = config.get("ip")
        self.port = config.get("port")

    def get_stream_url(self):
        return f"{self.protocol}://{self.ip}:{self.port}?pkt_size=1316"