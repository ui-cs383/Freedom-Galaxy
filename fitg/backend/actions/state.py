import yaml
import orm
from sqlalchemy import or_

def get_object(session, name, table):
	if name is None:
		items = session.query(table).filter_by(name=name).one()
	else:
		items = session.query(table).all()
		items = [ x.__dict__ for x in items ]

	return True, { table: items }