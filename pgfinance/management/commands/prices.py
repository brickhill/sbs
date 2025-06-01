from django.core.management.base import BaseCommand
from pytickersymbols import PyTickerSymbols
from pgfinance.models import Index, Company, Country, Industry, Lookup, Price
import yfinance as yf
import pickle


class Command(BaseCommand):
    help = "Add Prices to database"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--count", required=False, type=int, default=10,
                            help='Index')

    def handle(self, *args, **options):
        print(f"Prices: Count:({options['count']})")

        # Live
        ticker = yf.Ticker('III')
        company = Company.objects.filter(symbol="III")[0]
        # historical_data = ticker.history(period="max")  # data for the last month
        # pickle_file = open("pickle.txt", "ab")
        # pickle.dump(historical_data, pickle_file)

        # Test
        pickle_file = open("pickle.txt", "rb")
        historical_data = pickle.load(pickle_file)
        # print(type(historical_data))
        # for h in historical_data:
        #     print(h)

        for index, row in historical_data.iterrows():
            print(type(index))
            print(index, row['Open'], row['High'], row['Low'], row['Close'], row['Volume'],
            row['Dividends'], row['Stock Splits'])
            obj, created = Price.objects.update_or_create(
                                                          company=company,
                                                          price_time=index.to_pydatetime(),
                                                          open=row['Open'],      
                                                          high=row['High'],      
                                                          low=row['Low'],      
                                                          close=row['Close'],
                                                          volume=row['Volume'],
                                                          dividends=row['Dividends'],
                                                          stock_splits=row['Stock Splits']     
                                                        )

        # print(dat.info)
        # print(dat.calendar)
        # print(dat.analyst_price_targets)
        # print(dat.quarterly_income_stmt)
        # print(dat.history(period='1mo'))
        # print(dat.option_chain(dat.options[0]).calls)
        print("Prices END")
        
        