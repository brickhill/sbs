from django.core.management.base import BaseCommand
from pgfinance.models import Company, Price
import pickle
from django.db.models import Q
import pytz
import datetime as dt
from dateutil.relativedelta import relativedelta
import yfinance as yf

class Command(BaseCommand):
    help = "Add Prices to database"

    def add_arguments(self, parser):
        parser.add_argument("-c",
                            "--count",
                            required=False,
                            type=int,
                            default=10,
                            help='Index')

    def handle(self, *args, **options):
        print(f"Prices: Count:({options['count']})")
        bound = options['count'] - 1
        print(f"Bound:{bound}")
        historical_companies = Company.objects.all().filter \
        ((Q(prices_updated__lt=pytz.utc.localize(dt.datetime.now())- relativedelta(years=0)) \
        | Q(prices_updated__isnull=True)) & Q(status=Company.ACTIVE)).        \
        order_by("prices_updated")[:options['count']]
        ticker_list = []
        for h in historical_companies:
            ticker_list.append(f"{h.symbol}.L")

        historical_data = yf.download(ticker_list, period='max',auto_adjust=True)
        pickle_file = open("pickle2.txt", "ab")
        pickle.dump(historical_data, pickle_file)

        # Live
        # company = Company.objects.filter(symbol="III")[0]
        # historical_data = ticker.history(period="max")  # the last month
        # pickle_file = open("pickle.txt", "ab")
        # pickle.dump(historical_data, pickle_file)

        # Test
        # pickle_file = open("pickle.txt", "rb")
        # historical_data = pickle.load(pickle_file)
        # print(type(historical_data))
        # for h in historical_data:
        #     print(h)

        # for index, row in historical_data.iterrows():
        #     obj, created = Price.objects. \
        #         update_or_create(
        #                         company=company,
        #                         price_time=index.
        #                         to_pydatetime(),
        #                         open=row['Open'],
        #                         high=row['High'],
        #                         low=row['Low'],
        #                         close=row['Close'],
        #                         volume=row['Volume'],
        #                         dividends=row['Dividends'],
        #                         stock_splits=row['Stock Splits']
        #                         )

        # print(dat.info)
        # print(dat.calendar)
        # print(dat.analyst_price_targets)
        # print(dat.quarterly_income_stmt)
        # print(dat.history(period='1mo'))
        # print(dat.option_chain(dat.options[0]).calls)
        print("Prices END")
        
        