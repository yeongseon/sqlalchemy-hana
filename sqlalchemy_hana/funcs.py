
from sqlalchemy.sql.functions import GenericFunction


class first_value(GenericFunction):
    """The HANA 'first_value' aggregate function."""

    def __init__(self, *clauses, order_by=None, **kwargs):

        self.order_by = order_by
        super().__init__(*clauses, **kwargs)


@compile(first_value)
def compile_first_value(element, compiler, **_):
    """Compiler for first value function."""
    clauses = element.clauses
    order_by = element.order_by
    order_by_clause = "ORDER BY"
    if order_by is None:
        order_by_clause = ""
    elif isinstance(order_by, (list, tuple)):
        order_by_clause += ", ".join("%s" % compler.process(column) for column in order_by)
    else:
        order_by_clause += compiler.process(order_by)

    return "first_value(%s %s)" % (compiler.process(clauses), order_by_clause)