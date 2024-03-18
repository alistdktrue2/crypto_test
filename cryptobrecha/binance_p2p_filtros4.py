import asyncio
import json
import requests
import sys

BINANCE_P2P_API = "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

async def get_price(trade_type, fiat, token, cantidad):
    best_prices = []
    page = 1

    while True:
        request_body = {
            "page": page,
            "rows": 10,
            "payTypes": [],
            "asset": token,
            "tradeType": trade_type,
            "fiat": fiat,
            "publisherType": None,
            "merchantCheck": False,
            "transAmount ": cantidad
        }

        response = requests.post(BINANCE_P2P_API, json=request_body).json()
        data = response["data"]

        if not data:
            break

        all_prices = []
        users = []

        for order in data:
            adv = order["adv"]
            advertiser = order["advertiser"]

            user_no = advertiser["userNo"]
            real_name = advertiser["realName"]
            nick_name = advertiser["nickName"] if real_name is None else advertiser["realName"]

            if len(adv["tradeMethods"]) == 1:
                if adv["tradeMethods"][0]["identifier"] != "CashInPerson":
                    all_prices.append(float(adv["price"]))
                    users.append({
                        "user_no": user_no,
                        "nickname": nick_name,
                        "min_sell_quantity": float(adv["minSingleTransAmount"]),
                        "max_sell_quantity": float(adv["maxSingleTransAmount"]),
                        "available_quantity": float(adv["surplusAmount"]),
                        "price": float(adv["price"]),
                        "banks": [adv["tradeMethods"][0]["tradeMethodName"]],
                        "sell_currency": adv["asset"],
                        "buy_currency": adv["fiatUnit"],
                    })
                continue

            banks = [method["tradeMethodName"] for method in adv["tradeMethods"] if method["identifier"] != "CashInPerson"]
            all_prices.append(float(adv["price"]))
            users.append({
                "user_no": user_no,
                "nickname": nick_name,
                "min_sell_quantity": float(adv["minSingleTransAmount"]),
                "max_sell_quantity": float(adv["maxSingleTransAmount"]),
                "available_quantity": float(adv["surplusAmount"]),
                "price": float(adv["price"]),
                "banks": banks if banks else ["Multiple"],
                "sell_currency": adv["asset"],
                "buy_currency": adv["fiatUnit"]
            })

        best_price = min(all_prices)
        best_prices.append({"price": best_price, "token": token, "users": users})

        page += 1

    return best_prices

async def analyze_prices(trade_type, fiat, token, amounts):
    results = []

    for amount in amounts:
        prices = await get_price(trade_type, fiat, token, amount)
        results.append({"amount": amount, "prices": prices})

    return results

def analyze_banks(prices_results):
    bank_counts = {}

    for result in prices_results:
        for price_info in result["prices"]:
            for user_info in price_info["users"]:
                for bank in user_info["banks"]:
                    if bank in bank_counts:
                        bank_counts[bank] += 1
                    else:
                        bank_counts[bank] = 1

    return bank_counts

async def get_prices(amount):
    await asyncio.sleep(1)  # Simula una operación asíncrona, reemplaza con llamadas reales
    return {"amount": amount, "prices": [{"price": 1.0, "users": [{"nickname": "User1", "banks": ["Bank1"]}] }]}

async def main():
    trade_type = "BUY"
    fiat = "USD"
    token = "USDT"
    amounts_to_check = [100, 500]

    prices_results = await analyze_prices(trade_type, fiat, token, amounts_to_check)

    # Almacenar los resultados en un archivo JSON
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(prices_results, json_file, indent=4, ensure_ascii=False)

    bank_counts = analyze_banks(prices_results)
    
    # Agregar los resultados de los bancos al mismo archivo JSON
    with open('output.json', 'a', encoding='utf-8') as json_file:
        json.dump({"Bank Counts": bank_counts}, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
