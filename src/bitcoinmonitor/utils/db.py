from contextlib import contextmanager

import psycopg2


class WarehouseConnection(object):
    def __init__(
        self, db: str, user: str, password: str, host: str, port: int
    ):
        self.conn_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()
