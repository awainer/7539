import csv,sys,os
sys.path.append("..")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()
from django.conf import settings
from settings import *
from backend.models import HealthCenter
from geoposition.fields import GeopositionField
from decimal import Decimal
import os


def load_hc_from_csv(csv_file):
    with open(csv_file,'r') as csvfile:
        print csvfile
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            print row
            hc = HealthCenter(name = row['NOMBRE'],
                              address = row['CALLE'] + ' ' +  row['ALTURA'],
                              position = ','.join((row['Y'], row['X'])))
            hc.save()
if __name__ == '__main__':
    load_hc_from_csv(sys.argv[1])
