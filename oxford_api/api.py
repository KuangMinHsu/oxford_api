import requests
from . import exceptions
import logging
from multiprocessing.dummy import Pool as ThreadPool

logger = logging.getLogger("general")


class API:
    base = "https://od-api.oxforddictionaries.com/api/v2"
    language = "en-us"
    app_id = "47fcc00f"
    app_key = "03db3f6ad3e3c2d042afdcd9aa33a0cc"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "app_id": self.app_id,
            "app_key": self.app_key
        })

    def entries(self, word_id):
        url = f"{self.base}/entries/{self.language}/{word_id}"
        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError as e:
            raise exceptions.BaseException(url) from e
        if response.status_code != 200:
            raise exceptions.BaseException(
                f"{word_id} {response.status_code}\n{response.text}"
            )
        return (word_id, response.text)


class ParallelAPI:
    def __init__(self):
        self.api = API()

    def entries(self, word_ids):
        return self._parallel_query(self.api.entries, word_ids)

    def _parallel_query(self, task, inputs):
        pool = ThreadPool(5)
        try:
            rets = pool.map(task, inputs)
        except Exception:
            logger.exception(rets)
            raise
        finally:
            pool.close()
        rets, errors = self.filter_error(rets)
        return rets, errors

    def filter_error(self, rets):
        errors = []
        new_rets = []
        for k, v in rets:
            if isinstance(v, Exception):
                errors.append((k, v))
                continue
            new_rets.append((k, v))
        return new_rets, errors
