import requests


class Client:
    """
    Thin wrapper around Monobank Open API.
    https://api.monobank.ua/docs/
    """

    base_url = 'https://api.monobank.ua/personal/'

    def __init__(self, token):
        self.token = token

    def request(self, url, method='get', **kwargs):
        response = requests.request(method, f'{self.base_url}{url}',
                                    headers={'X-Token': self.token}, **kwargs)
        try:
            data = response.json()
        except ValueError:
            data = response.text
        return {
            'status_code': response.status_code,
            'data': data,
        }

    def set_webhook(self, webhook_url):
        return self.request('webhook', 'post', data={'webHookUrl': webhook_url})

    def get_client_info(self):
        return self.request('client-info')

    def get_statement(self, from_time, to_time=None, account='0'):
        url = f'statement/{account}/{from_time}'
        if to_time:
            url += f'/{to_time}'
        return self.request(url)
