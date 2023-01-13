from common.comparators import compare_fields
from tests.generator import create_info_message
from tests.generator import generator
from tests.generator import info_message_create_dict

stream_name = "info"
create_obj = create_info_message
create_dict = info_message_create_dict


def test_read_page(log_core, log_session):
    crud = getattr(log_core, stream_name)
    for error in crud.read_page(log_session):
        assert error.id


def test_create(log_core, log_session):
    crud = getattr(log_core, stream_name)
    values = create_dict(log_session)
    obj = crud.create(log_session, values)
    compare_fields(values, obj)


class TestRead:
    @staticmethod
    @generator.custom(count=2)
    def generator(log_session):
        return create_obj(log_session)

    def test(self, log_core, log_session):
        crud = getattr(log_core, stream_name)
        for obj_id in self.generator.generated:
            obj = crud.read(log_session, obj_id)
            assert obj.id == obj_id
