import json
from typing import Optional


class RawDataDescriptorBase:
    def __parse(self, raw_data: bytes) -> Optional[dict]:
        try:
            data = self.parse_raw_data(raw_data)
            self.logger.info(f"Пакет обработан: {data}")
            return data
        except Exception as e:
            self.logger.error(e)

    def __init__(self, message, logger):
        self.logger = logger
        self.data = self.__parse(message.raw_data)

    def __call__(self) -> Optional[dict]:
        return self.data

    def parse_raw_data(self, raw_data) -> dict:
        raise NotImplementedError

    def to_json(self):
        return json.dumps(self.data)


class Utf8Descriptor(RawDataDescriptorBase):
    def parse_raw_data(self, raw_data: bytes):
        data = dict(message=raw_data.decode("utf-8"))
        return data
