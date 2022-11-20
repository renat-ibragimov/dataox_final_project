from datetime import date
from typing import Optional


class CommonQueryParams:
    def __init__(self,
                 price_from: int = None,
                 price_to: int = None,
                 date_from: date = None,
                 date_to: date = None,
                 hydro_available: bool = None,
                 heat_available: bool = None,
                 water_available: bool = None,
                 wifi_available: bool = None,
                 parking: int = None,
                 move_in_date_from: date = None,
                 move_in_date_to: date = None,
                 pet_friendly: bool = None,
                 size_from: int = None,
                 size_to: int = None,
                 furnished: bool = None,
                 appliances: bool = None,
                 ac: bool = None,
                 outdoor_space: bool = None,
                 smoking: bool = None
                 ):
        self.price_from = price_from
        self.price_to = price_to
        self.date_from = date_from
        self.date_to = date_to
        self.hydro_available = hydro_available
        self.heat_available = heat_available
        self.water_available = water_available
        self.wifi_available = wifi_available
        self.parking = parking
        self.move_in_date_from = move_in_date_from
        self.move_in_date_to = move_in_date_to
        self.pet_friendly = pet_friendly
        self.size_from = size_from
        self.size_to = size_to
        self.furnished = furnished
        self.appliances = appliances
        self.ac = ac
        self.outdoor_space = outdoor_space
        self.smoking = smoking
