import logging
from typing import List, Tuple
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
import json
logger = logging.getLogger('')


class Storage:
    def connect(self) -> MySQLConnection:
        return connect(
            host='local-mysql',
            database='vocabulary',
            user='user',
            password='5566'
        )

    def upsert_many(self, words: List[Tuple[str, str]]):
        con = self.connect()
        cur = con.cursor()
        try:
            cur.executemany(
                "INSERT INTO Entry (word_id, data) "
                "VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE data=VALUES(data)", words
            )
        except Exception:
            con.rollback()
            logger.exception("insert fail")
            raise
        else:
            con.commit()
        finally:
            con.close()

    def parameterize(self, n):
        return ",".join(["%s"] * n)

    def get(self, word_ids: set) -> dict:
        con = self.connect()
        cur = con.cursor()
        placeholders = self.parameterize(len(word_ids))
        try:
            cur.execute(f"SELECT word_id, data FROM Entry WHERE word_id IN ({placeholders})", tuple(word_ids))
            return dict((word_id, json.loads(data)) for word_id, data in cur.fetchall())
        except Exception:
            logger.exception("insert fail")
            raise
        finally:
            con.close()
