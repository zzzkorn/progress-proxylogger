class PacketBase:
    def __call__(self) -> bytes:
        return self.get_packet_bytes()

    def get_packet_bytes(self, *args, **kwargs) -> bytes:
        raise NotImplementedError
