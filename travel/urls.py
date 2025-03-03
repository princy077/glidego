
from django.urls import path
from .views import destination_detail, destinations_list, home, search_destinations, recommend_destinations, update_preferences, register, map_view, nearby_destinations, book_activity, booking_confirmation, user_bookings, submit_review, review_list

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_destinations, name='search_destinations'),
    path('recommendations/<int:destination_id>/', recommend_destinations, name='recommend_destinations'),
    path('preferences/', update_preferences, name='update_preferences'),
    path('register/', register, name='register'),
    path('destination/<int:destination_id>/', destination_detail, name='destination_detail'),
    path('destinations/', destinations_list, name='destinations'),
    path('map/',map_view, name='map_view'),
    path('nearby-destinations/', nearby_destinations, name='nearby_destinations'),
    path('book-activity/', book_activity, name='book_activity'),
    path('booking-confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', user_bookings, name='user_bookings'),
    path('submit-review/', submit_review, name='submit_review'),
    path('reviews/', review_list, name='review_list'),
]
