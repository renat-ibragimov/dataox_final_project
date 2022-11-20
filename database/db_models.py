import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.db_modelbase import SQLBase


class ApartmentInfo(SQLBase):
    __tablename__ = 'apartments_info'

    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    title = sa.Column(sa.String(length=128))
    city = sa.Column(sa.String(length=128), index=True)
    location = sa.Column(sa.String(length=256), index=True)
    price = sa.Column(sa.SmallInteger, index=True)
    currency = sa.Column(sa.String(length=1))
    price_description = sa.Column(sa.String(length=128))
    date_posted = sa.Column(sa.DateTime, index=True)
    description = sa.Column(sa.Text)
    details = relationship("ApartmentDetails", back_populates="info",
                           uselist=False)
    owner_id = sa.Column(sa.Integer, ForeignKey("owners_details.id"))
    owner = relationship("OwnerDetails", back_populates="apartments")


class ApartmentDetails(SQLBase):
    __tablename__ = 'apartments_details'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    apartment_id = sa.Column(sa.Integer,
                             sa.ForeignKey('apartments_info.id'), unique=True)
    info = relationship("ApartmentInfo", back_populates="details")
    overview_utilities_incl_hydro = sa.Column(sa.Boolean)
    overview_utilities_incl_heat = sa.Column(sa.Boolean)
    overview_utilities_incl_water = sa.Column(sa.Boolean)
    overview_wi_fi = sa.Column(sa.Boolean)
    overview_parking = sa.Column(sa.SmallInteger)
    overview_agreement_type = sa.Column(sa.String(length=48))
    overview_move_in_date = sa.Column(sa.DateTime)
    overview_pet_friendly = sa.Column(sa.Boolean)
    unit_size = sa.Column(sa.SmallInteger)
    unit_furnished = sa.Column(sa.Boolean)
    unit_appliances = sa.Column(sa.Boolean)
    unit_ac = sa.Column(sa.Boolean)
    unit_outdoor_space = sa.Column(sa.Boolean)
    int_smoking = sa.Column(sa.Boolean)


class OwnerDetails(SQLBase):
    __tablename__ = 'owners_details'

    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    name = sa.Column(sa.String(length=128))
    rank = sa.Column(sa.String(length=12))
    on_kijiji_since = sa.Column(sa.String(length=24))
    phone = sa.Column(sa.String(length=24))
    apartments = relationship("ApartmentInfo", back_populates="owner")
