from django.db import models as m
from six import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
import logging

# Create your models here.
class Metro(m.Model):
    station = m.CharField(verbose_name='Станция', max_length=23 )
    line = m.CharField(verbose_name='Линия', max_length=31 )
    admarea = m.CharField(verbose_name='Округ', max_length=70)
    district = m.CharField(verbose_name='Район', max_length=25)
    status = m.CharField(verbose_name='Статус', max_length=30)
    ID = m.IntegerField(blank=True, null=True)

    def __repr__(self) -> str:
        return self.station

LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)


@python_2_unicode_compatible
class StatusLog(m.Model):
    logger_name = m.CharField(max_length=100)
    level = m.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = m.TextField()
    trace = m.TextField(blank=True, null=True)
    create_datetime = m.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return self.msg


class stderr(m.Model):
    log = m.JSONField()
