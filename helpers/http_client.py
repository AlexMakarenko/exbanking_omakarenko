import requests, logging, json


log = logging.getLogger(__name__)


class HttpClient:

    def send_post(self, url: str, headers: dict, data: dict):
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        log.info(f'POST {url} \nHEADERS: {headers} \nPAYLOAD: {data} \nRESPONSE: {r.content}')
        return r
    
    def send_get(self, url: str, headers: dict, data: dict=None):
        r = requests.get(url=url, headers=headers, data=json.dumps(data))
        log.info(f'GET {url} \nHEADERS: {headers} \nPAYLOAD: {data} \nRESPONSE: {r.content}')
        return r
