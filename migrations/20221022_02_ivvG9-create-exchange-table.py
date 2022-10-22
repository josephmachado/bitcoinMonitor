"""
create exchange table
"""

from yoyo import step

__depends__ = {"20221022_01_pvLdZ-create-bitcoin-schema"}

steps = [
    step(
        """
        CREATE TABLE bitcoin.exchange
        (
            id VARCHAR(50),
            name VARCHAR(50),
            rank INT,
            percentTotalVolume NUMERIC(8, 5),
            volumeUsd NUMERIC,
            tradingPairs INT,
            socket BOOLEAN,
            exchangeUrl VARCHAR(50),
            updated_unix_millis BIGINT,
            updated_utc TIMESTAMP
        )
        """,
        "DROP TABLE bitcoin.exchange",
    )
]
