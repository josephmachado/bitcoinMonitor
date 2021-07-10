import os
from typing import Dict, Optional, Union


def get_warehouse_creds() -> Dict[str, Optional[Union[str, int]]]:
    return {
        'user': os.getenv('WAREHOUSE_USER'),
        'password': os.getenv('WAREHOUSE_PASSWORD'),
        'db': os.getenv('WAREHOUSE_DB'),
        'host': os.getenv('WAREHOUSE_HOST'),
        'port': int(os.getenv('WAREHOUSE_PORT', 5432)),
    }
