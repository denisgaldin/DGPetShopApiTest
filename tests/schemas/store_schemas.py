STORE_INVENTORY_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "integer"
    }
}

STORE_ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "shipDate": {"type": "string", "format": "date-time"},
        "status": {"type": "string"},
        "complete": {"type": "boolean"}
    },
    "required": ["id", "petId", "quantity", "status", "complete"]
}
