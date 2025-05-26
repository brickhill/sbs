from django.core.management.base import BaseCommand
from pytickersymbols import PyTickerSymbols
from pgfinance.models import Index, Company, Country, Industry, Lookup


class Command(BaseCommand):
    help = "Add companies to database"

    def add_arguments(self, parser):
        parser.add_argument("-i", "--index", required=True,
                            help='Index')

    def handle(self, *args, **options):
        print(f"COMPANIES:{options['index']}")
        index = Index.objects.filter(name=options['index']).first()
        if index is None:
            print(f"Index: {options['index']} not found")
            exit(99)
        
        stock_data = PyTickerSymbols()
        uk_stocks = stock_data.get_stocks_by_index(options['index'])
        for u in uk_stocks:
            country = Country.objects.filter(name=u['country'])[0]
            new_company, created = Company.objects.update_or_create(
            name=u['name'],
            symbol=u['symbol'],
            country=country
            )
            new_company.save()
            for i in u['indices']:
                new_company.index.add(Index.objects.get(name=i))
            
            for i in u['industries']:
                new_company.industry.add(Industry.objects.get(name=i))
            
            for s in u['symbols']:
                print(s)
                if s['currency'] == 'EUR':
                    currency = Lookup.EURO
                elif s['currency'] == 'USD':
                    currency = Lookup.USDOLLAR
                elif s['currency'] == 'GBP':
                    currency = Lookup.STERLING
                else:
                    print(f"Unknown Currency: {s['currency']}")
                    exit(96)
                print(f"{new_company} GOOGLE {s['google']} YAHOO {s['yahoo']} currency {s['currency']}")
                new_lookup, created = Lookup.objects.update_or_create(
                    company = new_company,
                    symbol_yahoo = s['yahoo'],
                    symbol_google = s['google'],
                    currency = currency
                )
                new_lookup.save()

        '''
        ####### Name:3i Group PLC
        ####### Country:United Kingdom
        ####### Indices:['FTSE 100']
        ####### Industries:['Banking & Investment Services', 'Investment Banking & Investment Services', 
        ####### 'Financials', 'Investment Management & Fund Operators']
        Symbols: [
        {'yahoo': 'IGQ5.F', 'google': 'FRA:IGQ5', 'currency': 'EUR'}, 
        {'yahoo': 'TGOPY', 'google': 'OTCMKTS:TGOPY', 'currency': 'USD'},
        {'yahoo': 'III.L', 'google': 'LON:III', 'currency': 'GBP'},
        {'yahoo': 'IGQ.F', 'google': 'FRA:IGQ', 'currency': 'EUR'},
        {'yahoo': 'TGOPF', 'google': 'OTCMKTS:TGOPF', 'currency': 'USD'}]
        '''


