from datetime import datetime

from bson import ObjectId
from models.order import Order
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.serialize import Serializer
from fastapi import status
from helpers.utils import Response
from configurations.config import orders


class OrderService:
    def __init__(self, order_collection: AsyncIOMotorCollection):
        self.orders = order_collection

    async def create(self, order: Order) -> Response:
        try:
            serialize_data = Serializer(order)
            response = await self.orders.insert_one(serialize_data.serialize())
            if response.acknowledged:
                return Response(
                    status_code=status.HTTP_201_CREATED,
                    inserted_id=str(response.inserted_id),
                    message='Book created successfully'

                )

            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Book not created'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f'Error: {e}'
            )

    async def find_all(self) -> Response:
        try:
            data = await self.orders.find({}).to_list(None)
            serialize_data = Serializer(data)
            return Response(
                status_code=status.HTTP_200_OK,
                data=serialize_data.deserialize()
            )
        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def find_by_id(self, order_id: str) -> Response:
        try:
            if order := await self.orders.find_one({'_id': ObjectId(order_id)}):
                serialize_data = Serializer(order)
                return Response(
                    status_code=status.HTTP_200_OK,
                    data=serialize_data.deserialize()
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not found'
            )
        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def delete(self, order_id: str) -> Response:
        try:
            response = await self.find_by_id(order_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return response

            if await self.orders.delete_one({'_id': ObjectId(order_id)}):
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book deleted successfully'
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not found'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def update(self, order_id: str, order_updated: Order) -> Response:
        try:
            response = await self.find_by_id(order_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return response
            order_updated.updated_at = datetime.now()
            response = await self.orders.update_one({'_id': ObjectId(order_id)}, {'$set': dict(order_updated)})
            if response.acknowledged:
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book updated successfully'
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The order is not updated'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

order_service = OrderService(orders)