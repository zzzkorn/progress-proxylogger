class Field:
    def __init__(self, field):
        self.field = field

    def __call__(self, query, value):

        if value is None:
            return query
        order = {
            "asc": self.field.asc,
            "desc": self.field.desc,
        }[value]()
        return query.order_by(order)
