def order_entity(order):
    return {
        "id": str(order["_id"]),
        "fist_name": order["fist_name"],
        "last_name": order["last_name"],
        "email": order["email"],
        "book_id": order["book_id"],
        "quantity": order["quantity"],
        "created_at": order["created_at"],
        "updated_at": order["updated_at"]
    }


def orders_entity(orders):
    return [order_entity(d) for d in orders]