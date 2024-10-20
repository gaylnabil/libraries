import os
from datetime import datetime

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status

from models.order import Order
from configurations.config import orders
from schemas.order_schema import order_entity, orders_entity
from fastapi.responses import JSONResponse
from configurations.kafka import KafkaProducer

load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER", str)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", str)

order_router = APIRouter()

# get all orders
@order_router.get("/orders")
async def get_orders():
    try:
        if data := await orders.find({}).to_list(None):
            return orders_entity(data)
        else:
            raise HTTPException(status_code=404, detail="The order is not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# retrieve order
@order_router.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        if data := await orders.find_one({"_id": ObjectId(order_id)}):
            return order_entity(data)
        else:
            raise HTTPException(status_code=404, detail="The order is not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# create new order
@order_router.post("/orders")
async def create_order(order: Order):
    try:
        p = KafkaProducer(KAFKA_BROKER, group_id="order-group")
        p.send_message(KAFKA_TOPIC, message = {"key": order.book_id, "quantity": order.quantity})
        response = await orders.insert_one(dict(order))
        return JSONResponse(content={
            "status_code": status.HTTP_201_CREATED,
            "id": str(response.inserted_id)
        })
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# update order
@order_router.put("/orders/{order_id}")
async def update_order(order_id: str, order_updated: Order):
    try:
        order = await orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="The order is not found")

        order_updated.updated_at = datetime.now()
        await orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": dict(order_updated)}
        )
        return JSONResponse(content={
            "status_code": status.HTTP_200_OK,
            "Message": "Order updated successfully"
        })
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# delete order
@order_router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    order = await orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="The order is not found")
    await orders.delete_one({"_id": ObjectId(order_id)})
    return JSONResponse(content={
        "status_code": status.HTTP_200_OK,
        "Message": "Order deleted successfully"
    })
