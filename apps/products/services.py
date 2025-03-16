import requests
from django.core.cache import cache
from django.conf import settings


def response_context(url=None, token=None, product_id=None, query=None):
    params = {
        "method": "food.get.v4" if product_id else "food.search",
        "food_id": product_id if product_id else None,
        "search_expression": query if query else None,
        "format": "json"
    }
    params = {key:value for key, value in params.items() if value is not None}
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["food"] if product_id else response.json()["foods"]["food"]

class FatSecretAPI:
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
    CACHE_KEY = "fatsecret_access_token"

    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET
        self.token = self.get_access_token()

    def get_access_token(self):
        cached_token = cache.get(self.CACHE_KEY)
        if cached_token:
            return cached_token
        data = {
            "grant_type": "client_credentials",
            "scope": "basic"
        }
        auth = (self.client_id, self.client_secret)
        response = requests.post(self.TOKEN_URL, data=data, auth=auth)
        response.raise_for_status()
        token_data = response.json()
        cache.set(self.CACHE_KEY, token_data["access_token"], timeout=token_data["expires_in"])
        return token_data["access_token"]

    def get_product(self, product_id):
        BASE_URL = "https://platform.fatsecret.com/rest/food/v4"
        return response_context(BASE_URL, self.token, product_id=product_id)

    def search_products(self, query):
        BASE_URL = "https://platform.fatsecret.com/rest/foods/search/v1"
        return response_context(BASE_URL, self.token, query=query)
