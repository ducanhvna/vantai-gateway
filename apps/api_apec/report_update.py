from .unity import Apec
from django.conf import settings

def export_report():
    print('this tas run every 20s')
    apec = Apec(url=settings.APEC_CONFIG['SERVER_URL'], 
                db=settings.APEC_CONFIG['SERVER_URL_DB'], 
                username=settings.APEC_CONFIG['SERVER_USERNAME'], 
                password=settings.APEC_CONFIG['SERVER_PASSWORD'])