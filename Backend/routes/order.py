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
from configurations.logger import logger
from services.order import order_service

load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER", str)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", str)

order_router = APIRouter()

# get all orders
@order_router.get("/orders")
async def get_orders() -> JSONResponse:
    try:
        response = await order_service.find_all()
        if response.status_code == status.HTTP_200_OK:
            logger.info("find all orders successfully", func_name=get_orders.__name__)
            return response.data

        logger.error("The orders are not found", func_name=get_orders.__name__)
        raise HTTPException(status_code=404, detail="The orders are not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# retrieve order
@order_router.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        response = await order_service.find_by_id(order_id)
        if response.status_code == status.HTTP_200_OK:
            logger.info("find order successfully", func_name=get_order.__name__)
            return response.data
        else:
            logger.error("The order is not found", func_name=get_order.__name__)
            raise HTTPException(status_code=404, detail="The order is not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# create new order
@order_router.post("/orders")
async def create_order(order: Order):
    try:
        p = KafkaProducer(KAFKA_BROKER)
        p.send_message(KAFKA_TOPIC, message = {"key": order.book_id, "quantity": order.quantity})
        response = await order_service.create(order)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info("Order created successfully", func_name=create_order.__name__)
            return response

        logger.error("Order not created", func_name=create_order.__name__)
        raise HTTPException(status_code=404, detail="Order not created")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# update order
@order_router.put("/orders/{order_id}")
async def update_order(order_id: str, order_updated: Order):
    try:
        response = await order_service.update(order_id, order_updated)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Order updated successfully", func_name=update_order.__name__)
            return response
        else:
            logger.error("The order is not found", func_name=update_order.__name__)
            raise HTTPException(status_code=404, detail="The order is not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

# delete order
@order_router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    response = await order_service.delete(order_id)
    if response.status_code == status.HTTP_204_NO_CONTENT:
        logger.info("Order deleted successfully", func_name=delete_order.__name__)
        return response

    logger.error("The order is not found", func_name=delete_order.__name__)
    raise HTTPException(status_code=404, detail="The order is not found")