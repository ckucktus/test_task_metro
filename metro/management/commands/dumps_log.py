from django.core.management.base import BaseCommand, CommandError
from metro.models import stderr
from drf_api_logger.models import APILogsModel
from ast import literal_eval
import json




def get_data_for_log(raw):
    response = json.loads(raw.response)
    error = response.get('error', None)
    data = {
        'service':'metro',
        'message': raw.status_code,
        'error': error,
        'endpoint': raw.api }
    return json.dumps(data)


def dump_log():
    bulk_list = []
    queryset = APILogsModel.objects.all().order_by('-pk') #сначала старые записи
    for raw in queryset:
        try:
            bulk_list.append(stderr(log=get_data_for_log(raw))) #сохраняем экземляр класса в список
        except:
            print('что то не то с циклом')
            raise Exception
    stderr.objects.bulk_create(bulk_list)#разом сохраняем весь список
    queryset.delete() #удаляем записи из общей таблицы 

       

class Command(BaseCommand):
    help = 'dump_log'

    def handle(self, *args, **kwargs):
        try:
           dump_log()
           
        except:
            raise CommandError('Dump failed')