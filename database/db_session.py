import sqlalchemy as sa
import sqlalchemy.orm as orm

from database.db_modelbase import SQLBase

con_str = 'postgresql+psycopg2://dataox:dataox@localhost:5433/dataox_db'
engine = sa.create_engine(con_str)
factory = orm.sessionmaker(bind=engine)

# noinspection PyUnresolvedReferences
from database.db_models import ApartmentInfo, ApartmentDetails, OwnerDetails
SQLBase.metadata.create_all(bind=engine)
