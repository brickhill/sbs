from django.core.management.base import BaseCommand
from pytickersymbols import PyTickerSymbols
from pgfinance.models import Country, Index, Industry


class Command(BaseCommand):
    help = "Refresh small tables"

    def add_arguments(self, parser):
        actions = ['C', 'I', 'D']
        parser.add_argument("-a", "--action", choices=actions,
                            help='''
        C - Countries
        I - Indices
        D - Industries
        ''')
        parser.add_argument("-u", "--update", type=int)

    def handle(self, *args, **options):
        if options['action'] == "C":
            self.countries(options)
        elif options['action'] == "I":
            self.indices(options)
        elif options['action'] == "D":
            self.industries(options)
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Invalid Action: {options['action']}")
            )

    def countries(self, options):
        print("COUNTRIES REFRESH")
        added = 0
        updated = 0
        stock_data = PyTickerSymbols()
        countries = stock_data.get_all_countries()
        for c in countries:
            if options['update'] == 1:
                obj, created = Country.objects.update_or_create(
                                                                name=c,
                                                                defaults={
                                                                    'name': c
                                                                         }
                                                                )
                if created is True:
                    added += 1
                else:
                    updated += 1
        print(f"Finished.  Retrieved {len(countries)}, "
              "Created: {added}, Updated:{updated}")

    def indices(self, options):
        print("INDICES REFRESH")
        added = 0
        updated = 0
        stock_data = PyTickerSymbols()
        indicies = stock_data.get_all_indices()
        for i in indicies:
            if options['update'] == 1:
                obj, created = Index.objects.update_or_create(
                                                              name=i,
                                                              defaults={
                                                                'name': i
                                                                       }
                                                              )
                if created is True:
                    added += 1
                else:
                    updated += 1
        print(f"Finished.  Retrieved {len(indicies)}, "
              "Created: {added}, Updated:{updated}")

    def industries(self, options):
        print("INDUSTRIES REFRESH")
        added = 0
        updated = 0
        stock_data = PyTickerSymbols()
        industries = stock_data.get_all_industries()
        for i in industries:
            if options['update'] == 1:
                obj, created = Industry.objects.update_or_create(
                                                                 name=i,
                                                                 defaults={
                                                                    'name': i
                                                                    }
                                                                 )
                if created is True:
                    added += 1
                else:
                    updated += 1
        print(f"Finished.  Retrieved {len(industries)},"
              "Created: {added}, Updated:{updated}")
