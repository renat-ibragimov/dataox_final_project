import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database import db_session
from database.db_models import ApartmentInfo, ApartmentDetails, OwnerDetails


class ApartmentsQueryCreator:
    def __init__(self, price_from, price_to, date_from, date_to,
                 hydro_available, heat_available, water_available,
                 wifi_available, parking, move_in_date_from,
                 move_in_date_to, pet_friendly, size_from, size_to, furnished,
                 appliances, ac, outdoor_space, smoking):
        self.session = db_session.factory()
        self.result = self.session.query(
            ApartmentInfo, ApartmentDetails, OwnerDetails)\
            .filter(ApartmentInfo.id == ApartmentDetails.apartment_id)\
            .filter(ApartmentInfo.owner_id == OwnerDetails.id)
        self.price_from = self.filter_price_from(price_from) \
            if price_from is not None else None
        self.price_to = self.filter_price_to(price_to) \
            if price_to is not None else None
        self.date_from = self.filter_date_from(date_from) \
            if date_from is not None else None
        self.date_to = self.filter_date_to(date_to) \
            if date_to is not None else None
        self.hydro_available = self.filter_hydro_available(hydro_available) \
            if hydro_available is not None else None
        self.heat_available = self.filter_heat_available(heat_available) \
            if heat_available is not None else None
        self.water_available = self.filter_water_available(water_available) \
            if water_available is not None else None
        self.wifi_available = self.filter_wifi_available(wifi_available) \
            if wifi_available is not None else None
        self.parking = self.filter_parking(parking) \
            if parking is not None else None
        self.move_in_date_from = self.filter_move_in_date_from(
            move_in_date_from) if move_in_date_from is not None else None
        self.move_in_date_to = self.filter_move_in_date_to(
            move_in_date_to) if move_in_date_to is not None else None
        self.pet_friendly = self.filter_pet_friendly(pet_friendly) \
            if pet_friendly is not None else None
        self.size_from = self.filter_size_from(size_from) \
            if size_from is not None else None
        self.size_to = self.filter_size_to(size_to) \
            if size_to is not None else None
        self.furnished = self.filter_furnished(furnished) \
            if furnished is not None else None
        self.appliances = self.filter_appliances(appliances) \
            if appliances is not None else None
        self.ac = self.filter_ac(ac) \
            if ac is not None else None
        self.outdoor_space = self.filter_outdoor_space(outdoor_space) \
            if outdoor_space is not None else None
        self.smoking = self.filter_smoking(smoking) \
            if smoking is not None else None

    def create_query(self):
        return self.result.all()

    def filter_price_from(self, value):
        self.result = self.result.filter(ApartmentInfo.price >= value)

    def filter_price_to(self, value):
        self.result = self.result.filter(ApartmentInfo.price <= value)

    def filter_date_from(self, value):
        self.result = self.result.filter(ApartmentInfo.date_posted >= value)

    def filter_date_to(self, value):
        self.result = self.result.filter(ApartmentInfo.date_posted <= value)

    def filter_hydro_available(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_utilities_incl_hydro == value)

    def filter_heat_available(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_utilities_incl_heat == value)

    def filter_water_available(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_utilities_incl_water == value)

    def filter_wifi_available(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_wi_fi == value)

    def filter_parking(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_parking == value)

    def filter_move_in_date_from(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_move_in_date >= value)

    def filter_move_in_date_to(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_move_in_date <= value)

    def filter_pet_friendly(self, value):
        self.result = self.result.filter(
            ApartmentDetails.overview_pet_friendly == value)

    def filter_size_from(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_size >= value)

    def filter_size_to(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_size <= value)

    def filter_furnished(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_furnished == value)

    def filter_appliances(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_appliances == value)

    def filter_ac(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_ac == value)

    def filter_outdoor_space(self, value):
        self.result = self.result.filter(
            ApartmentDetails.unit_outdoor_space == value)

    def filter_smoking(self, value):
        self.result = self.result.filter(
            ApartmentDetails.int_smoking == value)
