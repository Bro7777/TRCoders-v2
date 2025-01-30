from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'try_project.settings')

# Celery uygulamasını oluştur
app = Celery('try_project')

# Django'nun ayarlarından Celery yapılandırmasını yükle
app.config_from_object('django.conf:settings', namespace='CELERY')

# Görevleri otomatik olarak bul
app.autodiscover_tasks()
