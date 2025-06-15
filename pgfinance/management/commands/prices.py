from django.core.management.base import BaseCommand
from pgfinance.models import Company, Price, Lookup
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
            lookup = Lookup.objects.filter(Q(company=h) & Q(currency=Lookup.STERLING))[0]
            ticker_list.append(f"{lookup}")
        print(ticker_list)
        ##### Get prices from Yahoo!
        # historical_data = yf.download(ticker_list, period='max',auto_adjust=True)
        # pickle_file = open("pickle2.txt", "ab")
        # pickle.dump(historical_data, pickle_file)

        # Test
        pickle_file = open("pickle2.txt", "rb")
        i=0
        historical_data = pickle.load(pickle_file)
        historical_data = historical_data.fillna(0)
        print(type(historical_data))
        for h in historical_companies:
            lookup = Lookup.objects.filter(Q(company=h) & Q(currency=Lookup.STERLING))[0]
            print(f"LU:{lookup}")
            for index, row in historical_data.iterrows():
                # print(f"({lookup})>>>>>row:{row.get('Close')[lookup.symbol_yahoo]} <<<<<<<")
                obj, created = Price.objects. \
                update_or_create(
                                company=lookup.company,
                                price_time=index.
                                to_pydatetime(),
                                open=row.get('Open')[lookup.symbol_yahoo],
                                high=row.get('High')[lookup.symbol_yahoo],
                                low=row.get('Low')[lookup.symbol_yahoo],
                                close=row.get('Close')[lookup.symbol_yahoo],
                                volume=row.get('Volume')[lookup.symbol_yahoo],
                                lookup=lookup
                                # dividends=row['Dividends'].get(lookup),
                                # stock_splits=row['Stock Splits'].get(lookup)
                                )

        print("Prices END")
        
        