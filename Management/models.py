# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Market.models import *
from django.db import models
import datetime
from datetime import timedelta
# Create your models here.
# class User_info(User):
#     def get_total(self):
#         return len()

#     def get_query_set(self):
#         return models.query.QuerySet(self.model, using=self._db)

#     def get_this_day(self):
#         start = datetime.datetime.now().date()
#         end = start + timedelta(days=1)
#         return self.objects.filter(createtime__range=(start, end))

# class SellInfo_info(SellInfo):

#     def get_query_set(self):
#         return models.query.QuerySet(self.model, using=self._db)

#     def get_this_day(self):
#         start = now().date()
#         end = start + timedelta(days=1)
#         return self.get_query_set().filter(createtime__range=(start, end))
#
