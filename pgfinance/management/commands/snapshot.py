from django.core.management.base import BaseCommand
from pgfinance.models import Company, Price
from pgfinance.chart import Chart
from pgfinance.calcs import add_indicator
from django.db.models import Q
from django_pandas.io import read_frame


class Command(BaseCommand):
    help = "Produce a one year chart for a given company"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--symbol", required=True,
                            help='Company symbol')

    def handle(self, *args, **options):
        print(f"SNAPSHOT:{options['symbol']}")
        qs = Company.objects.filter(symbol=options['symbol'])
        if not qs:
            print(f"Symbol:({options['symbol']}) not found")
            exit(99)
        company = qs[0]
        print(company.name)
        qs = Price.objects.filter(
                                  Q(company=company) & Q(period="D")).values(
                                    "price_time",
                                    "high",
                                    "low",
                                    "open",
                                    "close",
                                    "volume")
        df = read_frame(qs)
        df = df.set_index('price_time', drop=True)
        # Add some indicators.
        add_indicator(df, "MA", 10)
        add_indicator(df, "MA", 30)
        add_indicator(df, "BOLL", 10)
        df.dropna(inplace=True)
        print(df.head())
        Chart(options['symbol'], df, period="year", filename="test.png")
