import requests
from config import BASE_CURRENCY, TARGET_CURRENCIES

def get_exchange_rates(base=BASE_CURRENCY, targets=TARGET_CURRENCIES, api_key=None):

    if not api_key:
        raise Exception("EXCHANGE_API_KEY が設定されていません")

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    response = requests.get(url)
    data = response.json()

    if data.get("result") != "success":
        raise Exception(f"API取得エラー: {data}")

    rates = {t: data["conversion_rates"].get(t) for t in targets}
    return {"base": base, "rates": rates}


def calculate_jpy_to_php(rate_data):
    jpy_rate = rate_data["rates"].get("JPY")
    php_rate = rate_data["rates"].get("PHP")

    if not jpy_rate or not php_rate:
        raise Exception("JPYまたはPHPレートが取得できません")

    return php_rate / jpy_rate