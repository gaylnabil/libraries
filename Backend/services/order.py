from datetime import datetime

from bson import ObjectId
from models.order import Order
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.serialize import Serializer
from fastapi import status
from helpers.utils import Response
from configurations.config import orders
from configurations.logger import logger


class OrderService:
    def __init__(self, order_collection: AsyncIOMotorCollection):
        self.orders = order_collection

    async def create(self, order: Order) -> Response:
        """Create a new order document."""
        try:
            serialize_data = Serializer(order)
            response = await self.orders.insert_one(serialize_data.serialize())
            if response.acknowledged:
                logger.info(f"Order created successfully: {response.inserted_id}", func_name=self.create.__name__)
                return Response(
                    status_code=status.HTTP_201_CREATED,
                    inserted_id=str(response.inserted_id),
                    message='Order created successfully'
                )
            logger.error("Order not created", func_name=self.create.__name__)
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Order not created'
            )
        except Exception as e:
            logger.error(f"Error creating order: {e}", func_name=self.create.__name__)
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f'Error: {e}'
            )

    async def find_all(self) -> Response:
        """Find all orders."""
        try:
            data = await self.orders.find({}).to_list(None)
            serialize_data = Serializer(data)
            logger.info(f"Fetched {len(data)} orders", func_name=self.find_all.__name__)
            return Response(
                status_code=status.HTTP_200_OK,
                data=serialize_data.deserialize()
            )
        except Exception as e:
            logger.error(f"Error fetching orders: {e}", func_name=self.find_all.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def find_by_id(self, order_id: str) -> Response:
        """Find an order by its ID."""
        try:
            if order := await self.orders.find_one({'_id': ObjectId(order_id)}):
                serialize_data = Serializer(order)
                logger.info(f"Order found: {order_id}", func_name=self.find_by_id.__name__)
                return Response(
                    status_code=status.HTTP_200_OK,
                    data=serialize_data.deserialize()
                )
            logger.warning(f"Order not found: {order_id}", func_name=self.find_by_id.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not found'
            )
        except Exception as e:
            logger.error(f"Error finding order: {e}", func_name=self.find_by_id.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def delete(self, order_id: str) -> Response:
        """Delete an order by its ID."""
        try:
            response = await self.find_by_id(order_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                logger.warning(f"Delete failed, order not found: {order_id}", func_name=self.delete.__name__)
                return response
            delete_result = await self.orders.delete_one({'_id': ObjectId(order_id)})
            if delete_result.deleted_count == 1:
                logger.info(f"Order deleted: {order_id}", func_name=self.delete.__name__)
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Order deleted successfully'
                )
            logger.error(f"Order not deleted: {order_id}", func_name=self.delete.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not found'
            )
        except Exception as e:
            logger.error(f"Error deleting order: {e}", func_name=self.delete.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def update(self, order_id: str, order_updated: Order) -> Response:
        """Update an order by its ID."""
        try:
            response: Response = await self.find_by_id(order_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                logger.warning(f"Update failed, order not found: {order_id}", func_name=self.update.__name__)
                return response
            order_updated.updated_at = datetime.now()
            update_result = await self.orders.update_one({'_id': ObjectId(order_id)}, {'$set': dict(order_updated)})
            if update_result.modified_count == 1:
                logger.info(f"Order updated: {order_id}", func_name=self.update.__name__)
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Order updated successfully'
                )
            logger.error(f"Order not updated: {order_id}", func_name=self.update.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not updated'
            )
        except Exception as e:
            logger.error(f"Error updating order: {e}", func_name=self.update.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

order_service = OrderService(orders)