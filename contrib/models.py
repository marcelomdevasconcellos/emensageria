import jsonfield
from django.apps import apps
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from django.contrib.postgres.fields import JSONField

from config.mixins import BaseModelEsocial, BaseModelSerializer

from .choices import *

get_model = apps.get_model
