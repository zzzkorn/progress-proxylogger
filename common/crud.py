from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from common import order_fields
from common.errors import ObjectNotFound


class CrudBase:
    default_order_field: str = "id"
    default_order_direction: str = "asc"

    def _query(self, session: Session):
        return session.query(self.model).distinct()

    def _update_from_values(self, item: object, values: dict):
        for key, value in values.items():
            setattr(item, key, value)

    def _add_filters(self, query: Query, filters: dict):
        for name, field in self.filter_fields.items():
            should_filter = name in filters or not field.optional_field
            if should_filter:
                query = field(query, filters.get(name))
        return query

    def _add_orders(self, query: Query, orders: list):
        if not orders:
            orders = [(self.default_order_field, self.default_order_direction)]
        for name, direction in orders:
            field = self.order_fields.get(name)
            if field is None:
                model_field = getattr(self.model, name)
                field = order_fields.Field(model_field)
            query = field(query, direction)
        return query

    @property
    def order_fields(self):
        return {
            "id": order_fields.Field(self.model.id),
        }

    @property
    def filter_fields(self):
        return {}

    def model(self):
        raise NotImplementedError

    def read(self, session: Session, obj_id: int):
        obj = self._query(session).filter_by(id=obj_id).first()
        if not obj:
            raise ObjectNotFound(self.model, obj_id)
        return obj

    def read_page(
        self,
        session: Session,
        filters: dict = {},
        orders: list = [],
    ):
        query = self._query(session)
        query = self._add_filters(query, filters)
        query = self._add_orders(query, orders)
        for obj in query.all():
            yield obj

    def create_obj(self, session: Session, values: dict):
        return self.model(**values)

    def create(self, session: Session, values: dict):
        obj = self.create_obj(session, values)
        session.add(obj)
        session.flush()
        return obj

    def update(self, session: Session, obj, values: dict):
        self._update_from_values(obj, values)
        session.flush()
        return obj

    def delete(self, session: Session, obj: object):
        obj.delete()
        session.flush()
