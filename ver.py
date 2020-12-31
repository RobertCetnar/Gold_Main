
from goldmain.models import GoldPrice, Forecast


forecast_to_verification = Forecast.objects.all()
for f in forecast_to_verification:
    print('----------------------')
    create_date = f.created
    print(f'Data utworzenia prognozy: {create_date}')
    gold_price = GoldPrice.objects.filter(day=create_date)
    for g in gold_price:
        create_gold_price = g.price
        print(f'Cena złota w dniu utworzenia prognozy: {create_gold_price}')
    forecast = f.gold_forecast
    print(f'Prognozowana cena złota: {forecast}')
    ver_date = f.verification_date
    print(f'Data weryfikacji prognozy: {ver_date}')
    gold_price_verificate = GoldPrice.objects.filter(day=ver_date)
    if len(gold_price_verificate) > 0:
        print(gold_price_verificate)
        for v in gold_price_verificate:
            verificate_gold_price = v.price
    else:
        verificate_gold_price = 0
        print(f'Cena złota w dniu weryfikacji: {verificate_gold_price}')
    if create_gold_price > 0 and forecast > 0 and verificate_gold_price > 0:
        if forecast > create_gold_price and verificate_gold_price > create_gold_price:
            result_of_verification = True
            accuracy = int((verificate_gold_price - create_gold_price) / (forecast - create_gold_price) * 100)
            print(f'Prognoza: {result_of_verification}, dokładność: {accuracy} %')
        elif forecast > create_gold_price and verificate_gold_price < create_gold_price:
            result_of_verification = False
            accuracy = 0
            print(f'Prognoza: {result_of_verification}, dokładność: {accuracy} %')
        elif forecast < create_gold_price and verificate_gold_price > create_gold_price:
            result_of_verification = False
            accuracy = 0
            print(f'Prognoza: {result_of_verification}, dokładność: {accuracy} %')
        elif forecast < create_gold_price and verificate_gold_price < create_gold_price and verificate_gold_price > 0:
            result_of_verification = True
            accuracy = int((verificate_gold_price - create_gold_price) / (forecast - create_gold_price) * 100)
            print(f'Prognoza: {result_of_verification}, dokładność: {accuracy} %')
    else:
        print(f'No data needed for verification')

