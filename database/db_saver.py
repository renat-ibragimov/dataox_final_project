from db_models import ApartmentInfo, ApartmentDetails, OwnerDetails
from sqlalchemy.exc import IntegrityError
import sqlalchemy.orm
from database.db_session import engine, factory


class DBSaver:
    def __enter__(self):
        self.connection = engine.connect()
        self.session: sqlalchemy.orm.Session = factory()
        return self

    def save(self, info, details, owner):
        self.session.begin()
        owner_details = OwnerDetails(
            id=owner['id'],
            name=owner['name'],
            rank=owner['rank'],
            on_kijiji_since=owner['on_kijiji_since'],
            phone=owner['phone']
        )
        self.session.add(owner_details)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

        apartment_info = ApartmentInfo(
            id=info['id'],
            title=info['title'],
            city=info['city'],
            location=info['location'],
            price=info['price'],
            currency=info['currency'],
            price_description=info['price_description'],
            date_posted=info['date_posted'],
            description=info['description'],
            owner_id=info['owner_id']
        )
        self.session.add(apartment_info)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

        self.session.begin()
        apartment_details = ApartmentDetails(
            apartment_id=details['apartment_id'],
            overview_utilities_incl_hydro=details['ut_incl_hydro'],
            overview_utilities_incl_heat=details['ut_incl_heat'],
            overview_utilities_incl_water=details['ut_incl_water'],
            overview_wi_fi=details['wi_fi'],
            overview_parking=details['parking'],
            overview_agreement_type=details['agreement_type'],
            overview_move_in_date=details['move_in_date'],
            overview_pet_friendly=details['pet_friendly'],
            unit_size=details['size'],
            unit_furnished=details['unit_furnished'],
            unit_appliances=details['appliances'],
            unit_ac=details['ac'],
            unit_outdoor_space=details['outdoor_space'],
            int_smoking=details['smoking']
        )
        self.session.add(apartment_details)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()




