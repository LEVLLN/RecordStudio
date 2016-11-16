from django.conf.urls import url
from bookings import views

urlpatterns = [
    url(r'^$', views.home, name='main_page'),
    url(r'^about', views.about, name='about'),
    # url(r'^creating_booking', views.creating_booking, name='creating_booking'),
    url(r'^step_1', views.show_soundmans, name='step_1'),
    url(r'^step_2/(?P<soundman_id>[0-9]+)/$', views.show_calendar, name='step_2'),
    url(r'^step_2/(?P<soundman_id>[0-9]+)/create$', views.show_schedule, name='step_3'),
    url(r'^step_2/(?P<soundman_id>[0-9]+)/show$', views.create_booking, name='step_4'),

    url(r'^records$', views.CurrentRecordsView.get, name='current_records_of_soundman'),
    url(r'^records/(?P<booking_id>[0-9]+)/$', views.RecordView.details, name='start_record'),
    url(r'^records/(?P<booking_id>[0-9]+)/start', views.RecordView.start_record_method),
    url(r'^records/(?P<booking_id>[0-9]+)/stop', views.RecordView.stop_record_method),

]
