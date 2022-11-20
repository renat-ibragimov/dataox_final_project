import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from fastapi import FastAPI, Depends
from common_query import CommonQueryParams
from database.apartments_query_creator import ApartmentsQueryCreator

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/apartments')
def apartments(commons: CommonQueryParams = Depends(CommonQueryParams)):
    creator = ApartmentsQueryCreator(commons.price_from,
                                     commons.price_to,
                                     commons.date_from,
                                     commons.date_to,
                                     commons.hydro_available,
                                     commons.heat_available,
                                     commons.water_available,
                                     commons.wifi_available,
                                     commons.parking,
                                     commons.move_in_date_from,
                                     commons.move_in_date_to,
                                     commons.pet_friendly,
                                     commons.size_from,
                                     commons.size_to,
                                     commons.furnished,
                                     commons.appliances,
                                     commons.ac,
                                     commons.outdoor_space,
                                     commons.smoking)
    return creator.create_query()
