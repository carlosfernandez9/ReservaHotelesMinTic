from typing import Dict
from pydantic import BaseModel

class Rooms(BaseModel):
    hotelName: str
    city: str
    roomNumber: int
    isDeluxe: bool
    PriceCOP: int
    isAvailable: int
  
database_rooms = Dict[str, Rooms]
database_rooms = {"Habitacion1": Rooms(**{"hotelName":"BaqHotel",
                  "city": "Barranquilla",
                  "roomNumber":105,
                  "PriceCOP": 500000,
                  "isDeluxe":True,
                  "isAvailable": True}),

                  "Habitacion2": Rooms(**{"hotelName":"BogHotel",
                  "city": "Bogota",
                  "roomNumber":110,
                  "PriceCOP": 150000,
                  "isDeluxe":False,
                  "isAvailable": True}),

                  "Habitacion3": Rooms(**{"hotelName":"BaqHotel",
                  "city": "Barranquilla",
                  "roomNumber":209,
                  "PriceCOP": 1000000,
                  "isDeluxe":True,
                  "isAvailable": False}),
                }

def get_rooms(RoomIn):
    availableRooms = []
    for room in database_rooms.keys():
        if (database_rooms[room].isAvailable == True and 
            database_rooms[room].city == RoomIn.city and
            database_rooms[room].isDeluxe == RoomIn.isDeluxe and
            database_rooms[room].PriceCOP <= RoomIn.maxPrice):
            availableRooms.append(room)
    return availableRooms

def print_rooms(roomList):
    lista = []
    for room in roomList:
        lista.append(database_rooms[room])
        
    return lista
