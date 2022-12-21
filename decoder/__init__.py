from decoder.descriptors import Utf8Descriptor


class Decoder:

    descriptor = Utf8Descriptor

    def __init__(self, database):
        self.database = database

    def __parse_packets(self):
        for session, packet in self.database.get_packets_for_parse():
            data = self.descriptor(packet, self.database.logger)
            if data:
                self.database.insert_parse_data(session, packet, data)

    def run(self):
        while True:
            self.__parse_packets()
