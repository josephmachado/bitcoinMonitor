import datetime
import logging
import sys
from typing import Any, Dict, List, Optional

import psycopg2.extras as p
import requests

from bitcoinmonitor.utils.db import WarehouseConnection
from bitcoinmonitor.utils.sde_config import get_warehouse_creds


def get_utc_from_unix_time(
    unix_ts: Optional[Any], second: int = 1000
) -> Optional[datetime.datetime]:
    return (
        datetime.datetime.utcfromtimestamp(int(unix_ts) / second)
        if unix_ts
        else None
    )


def get_exchange_data() -> List[Dict[str, Any]]:
    url = 'https://api.coincap.io/v2/exchanges'
    try:
        r = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)
    return r.json().get('data', [])


def _get_exchange_insert_query() -> str:
    return '''
    INSERT INTO bitcoin.exchange (
        id,
        name,
        rank,
        percenttotalvolume,
        volumeusd,
        tradingpairs,
        socket,
        exchangeurl,
        updated_unix_millis,
        updated_utc
    )
    VALUES (
        %(exchangeId)s,
        %(name)s,
        %(rank)s,
        %(percentTotalVolume)s,
        %(volumeUsd)s,
        %(tradingPairs)s,
        %(socket)s,
        %(exchangeUrl)s,
        %(updated)s,
        %(update_dt)s
    );
    '''


def run() -> None:
    data = get_exchange_data()
    for d in data:
        d['update_dt'] = get_utc_from_unix_time(d.get('updated'))
    with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
        p.execute_batch(curr, _get_exchange_insert_query(), data)


if __name__ == '__main__':
    run()
