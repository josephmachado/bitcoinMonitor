import datetime

from bitcoinmonitor.exchange_data_etl import get_utc_from_unix_time


def test_get_utc_from_unix_time():
    ut: int = 1625249025588
    expected_dt = datetime.datetime(2021, 7, 2, 18, 3, 45, 588000)
    assert expected_dt == get_utc_from_unix_time(ut)
