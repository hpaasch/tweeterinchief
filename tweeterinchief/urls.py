
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import url
from django.contrib import admin

from chief_app.views import TrumpTweetListView, Trump2017ListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TrumpTweetListView.as_view(), name='index_view'),
    url(r'^2017/$', Trump2017ListView.as_view(), name='2017_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
