import datetime
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db.user_db import UserInDB
from db.user_db import update_user, get_user
from db.transaction_db import TransactionInDB
from db.transaction_db import save_transaction
from db.hotel_db import get_rooms, print_rooms
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn, TransactionOut
from models.Room_model import RoomIn

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
async def root():
    return {"Mensaje": "Bienvenido a la pagina de reserva de habitaciones !"}

@api.post("/user/auth/")
async def auth_user(user_in: UserIn):
    user_in_db = get_user(user_in.username)
    if user_in_db == "guest":
        return {"No Autenticado": "Ha ingresado como guest"}
        
    else:
        if user_in_db == None:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        if user_in_db.password != user_in.password:
            return {"No Autenticado": "Ha ingresado la contraseña incorrecta"}
        return {"Autenticado": "Ha ingresado con el usuario " + user_in_db.username}

@api.get("/user/RewardPoints/{username}")
async def get_balance(username: str):
    user_in_db = get_user(username)
    if user_in_db == None:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    user_out = UserOut(**user_in_db.dict())
    
    return user_out

@api.post("/search/")
async def searchRoomsAvailable(RoomIn: RoomIn):
    habitacionesDisponibles = get_rooms(RoomIn)

    if not habitacionesDisponibles:
        raise HTTPException(status_code=404, detail="No hay habitaciones disponibles para su seleccion")
    
    else:
        listado = print_rooms(habitacionesDisponibles)
    return listado

# @api.put("/user/transaction/")
# async def make_transaction(transaction_in: TransactionIn):
#     user_in_db = get_user(transaction_in.username)
#     if user_in_db == None:
#         raise HTTPException(status_code=404, detail="El usuario no existe")
#     if user_in_db.balance < transaction_in.value:
#         raise HTTPException(status_code=400, detail="Sin fondos suficientes")
#     user_in_db.balance = user_in_db.balance - transaction_in.value
#     update_user(user_in_db)
#     transaction_in_db = TransactionInDB(**transaction_in.dict(), actual_balance = user_in_db.balance)
#     transaction_in_db = save_transaction(transaction_in_db)
#     transaction_out = TransactionOut(**transaction_in_db.dict())
#     return transaction_out

if __name__ == '__main__':
    uvicorn.run(api, port=8080, debug=True)