import json
import asyncio
import requests
#from django.views.generic.base import View
#from django.shortcuts import render
from .models import User




BINANCE_P2P_API = "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

async def get_price(trade_type, fiat, token, cantidad, page,pais):
    best_prices = []

    request_body = {
        "page": page,
        "rows": 10,
        "payTypes": [],
        "asset": token,
        "tradeType": trade_type,
        "fiat": fiat,
        "publisherType": None,
        "merchantCheck": False,
        "shieldMerchantAds":False,
        "proMerchantAds":False,
        "transAmount ": cantidad,
        "countries": pais
    }

    response = requests.post(BINANCE_P2P_API, json=request_body).json()
    data = response["data"]

    if not data:
        return best_prices

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
                    "cantidad_disponible": float(adv["surplusAmount"]),
                    "price": float(adv["price"]),
                    "activo": adv["isTradable"],
                    "banks": [adv["tradeMethods"][0]["tradeMethodName"]],
                    "sell_currency": adv["asset"],
                    "buy_currency": adv["fiatUnit"],
                    "pedidos_mensual": advertiser["monthOrderCount"],
                    "id_comerciante": advertiser["userIdentity"],
                    "tiempo_de_pago": adv["payTimeLimit"],
                    "pais":pais,
                    "page": page  # Nuevo campo para almacenar la página
                })
            continue

        banks = [method["tradeMethodName"] for method in adv["tradeMethods"] if method["identifier"] != "CashInPerson"]
        all_prices.append(float(adv["price"]))
        users.append({
            "user_no": user_no,
            "nickname": nick_name,
            "min_sell_quantity": float(adv["minSingleTransAmount"]),
            "max_sell_quantity": float(adv["maxSingleTransAmount"]),
            "cantidad_disponible": float(adv["surplusAmount"]),
            "price": float(adv["price"]),
            "activo": adv["isTradable"],
            "banks": banks if banks else ["Multiple"],
            "sell_currency": adv["asset"],
            "buy_currency": adv["fiatUnit"],
            "pedidos_mensual": advertiser["monthOrderCount"],
            "id_comerciante": advertiser["userIdentity"],
            "tiempo_de_pago": adv["payTimeLimit"],
            "pais":pais,
            "page": page  # Nuevo campo para almacenar la página
        })

    best_price = min(all_prices)
    best_prices.append({"price": best_price, "token": token, "users": users})

    return best_prices

async def analyze_prices(trade_type, fiat, token, amounts,paises):
    results = []

    for amount in amounts:
        page = 1
        while True:
            prices = await get_price(trade_type, fiat, token, amount, page,paises)
            if not prices:
                break
            results.append({"amount": amount, "prices": prices})
            page += 1

    return results

async def main():
    trade_type = "SELL"
    fiat = "USD"
    token = "USDT"
    paises = (['PE'])
    amounts_to_check = [100,500]


    prices_results = await analyze_prices(trade_type, fiat, token, amounts_to_check,paises)
    output_filename = "out_prices/data"  # Nombre del archivo de salida
    output_filename=output_filename+trade_type+fiat+str(amounts_to_check)
    ext=".json"
    output_filename=output_filename+ext
    # Almacenar los resultados en un archivo JSON
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(prices_results, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
