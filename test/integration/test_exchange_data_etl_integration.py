import csv
import datetime
from decimal import Decimal

import psycopg2

from bitcoinmonitor.exchange_data_etl import run
from bitcoinmonitor.utils.db import WarehouseConnection
from bitcoinmonitor.utils.sde_config import get_warehouse_creds


class TestBitcoinMonitor:
    def teardown_method(self, test_exchange_data_etl_run):
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE bitcoin.exchange;")

    def get_exchange_data(self):
        with WarehouseConnection(get_warehouse_creds()).managed_cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as curr:
            curr.execute(
                '''SELECT id,
                        name,
                        rank,
                        percenttotalvolume,
                        volumeusd,
                        tradingpairs,
                        socket,
                        exchangeurl,
                        updated_unix_millis,
                        updated_utc
                        FROM bitcoin.exchange;'''
            )
            table_data = [dict(r) for r in curr.fetchall()]
        return table_data

    def test_exchange_data_etl_run(self, mocker):
        mocker.patch(
            'bitcoinmonitor.exchange_data_etl.get_exchange_data',
            return_value=[
                r
                for r in csv.DictReader(
                    open('test/fixtures/sample_raw_exchange_data.csv')
                )
            ],
        )
        run()
        expected_result = [
            {
                'id': 'binance',
                'name': 'Binance',
                'rank': 1,
                'percenttotalvolume': Decimal('25.44443'),
                'volumeusd': Decimal('12712561147.7913049212358699'),
                'tradingpairs': 650,
                'socket': True,
                'exchangeurl': 'https://www.binance.com/',
                'updated_unix_millis': 1625787943298,
                'updated_utc': datetime.datetime(
                    2021, 7, 8, 23, 45, 43, 298000
                ),
            },
            {
                'id': 'zg',
                'name': 'ZG.com',
                'rank': 2,
                'percenttotalvolume': Decimal('13.03445'),
                'volumeusd': Decimal('6512276458.5226475820074930'),
                'tradingpairs': 133,
                'socket': False,
                'exchangeurl': 'https://api.zg.com/',
                'updated_unix_millis': 1625787941554,
                'updated_utc': datetime.datetime(
                    2021, 7, 8, 23, 45, 41, 554000
                ),
            },
            {
                'id': 'huobi',
                'name': 'Huobi',
                'rank': 3,
                'percenttotalvolume': Decimal('5.93652'),
                'volumeusd': Decimal('2966009471.8337660651992927'),
                'tradingpairs': 589,
                'socket': True,
                'exchangeurl': 'https://www.hbg.com/',
                'updated_unix_millis': 1625787943276,
                'updated_utc': datetime.datetime(
                    2021, 7, 8, 23, 45, 43, 276000
                ),
            },
            {
                'id': 'okex',
                'name': 'Okex',
                'rank': 4,
                'percenttotalvolume': Decimal('4.99990'),
                'volumeusd': Decimal('2498051785.3601278924449889'),
                'tradingpairs': 287,
                'socket': False,
                'exchangeurl': 'https://www.okex.com/',
                'updated_unix_millis': 1625787941641,
                'updated_utc': datetime.datetime(
                    2021, 7, 8, 23, 45, 41, 641000
                ),
            },
        ]
        result = self.get_exchange_data()
        assert expected_result == result
