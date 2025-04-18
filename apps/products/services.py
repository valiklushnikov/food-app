import requests
from django.core.cache import cache
from django.conf import settings


class FatsecretAPIError(Exception):
    pass


def retrieve_product_from_fatsecret_api(product_id):
    fatsecret_api = FatSecretAPI()
    response_data = fatsecret_api.get_product(product_id)

    try:
        fatsecret_id = response_data["food_id"]
        name = response_data["food_name"]
        protein = response_data["servings"]["serving"][0]["protein"]
        carbs = response_data["servings"]["serving"][0]["carbohydrate"]
        fat = response_data["servings"]["serving"][0]["fat"]
        calories = response_data["servings"]["serving"][0]["calories"]
    except KeyError as e:
        raise FatsecretAPIError(
            f"Error message: Key {e} does not exist in response data"
        )

    product_data = {
        "fatsecret_id": fatsecret_id,
        "name": name,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "calories": calories,
    }
    return product_data


def response_context(url=None, token=None, product_id=None, query=None):
    params = {
        "method": "food.get.v4" if product_id else "food.search",
        "food_id": product_id if product_id else None,
        "search_expression": query if query else None,
        "format": "json",
    }
    params = {key: value for key, value in params.items() if value is not None}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


class FatSecretAPI:
    TOKEN_URL = settings.TOKEN_URL
    CACHE_KEY = "fatsecret_access_token"

    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET
        self.token = self.get_access_token()

    def get_access_token(self):
        cached_token = cache.get(self.CACHE_KEY)
        if cached_token:
            return cached_token
        data = {"grant_type": "client_credentials", "scope": "basic"}
        auth = (self.client_id, self.client_secret)
        response = requests.post(self.TOKEN_URL, data=data, auth=auth)
        response.raise_for_status()
        token_data = response.json()
        cache.set(
            self.CACHE_KEY,
            token_data["access_token"],
            timeout=token_data["expires_in"]
        )
        return token_data["access_token"]

    def get_product(self, product_id):
        response = response_context(
            settings.BASE_URL_GET_PRODUCT,
            self.token,
            product_id=product_id
        )
        error_message = response.get("error", {})
        if error_message:
            raise FatsecretAPIError(
                f"Error message: Invalid ID: product_id '{product_id}' does not exist"
            )
        return response["food"]

    def search_products(self, query):
        response = response_context(
            settings.BASE_URL_SEARCH_PRODUCT,
            self.token,
            query=query
        )
        error_message = response.get("error", {}).get("message")
        if error_message:
            raise FatsecretAPIError(f"Error massage: {error_message}")
        is_food_exist = response.get("foods", {}).get("food")
        if not is_food_exist:
            raise FatsecretAPIError(
                "Error message: Invalid search: product does not exist"
            )
        return response["foods"]["food"]
