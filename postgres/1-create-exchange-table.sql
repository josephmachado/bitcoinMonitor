CREATE SCHEMA bitcoin;

DROP TABLE IF EXISTS bitcoin.exchange;
CREATE TABLE bitcoin.exchange
(
    id VARCHAR(50),
    name VARCHAR(50),
    rank INT,
    percentTotalVolume NUMERIC(8, 5),
    volumeUsd NUMERIC(18, 5),
    tradingPairs INT,
    socket BOOLEAN,
    exchangeUrl VARCHAR(50),
    updated_unix_millis BIGINT,
    updated_utc TIMESTAMP
)
