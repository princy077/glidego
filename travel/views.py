
from django.shortcuts import get_object_or_404, render, redirect
from .models import Destination, Activity, UserPreference, ActivityBooking, Review
from django.contrib.auth.decorators import login_required
from .forms import ActivityBookingForm, ReviewForm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse
from geopy.distance import geodesic
import json

def home(request):
    return render(request, 'travel/home.html')

def search_destinations(request):
    query = request.GET.get('query', '').strip()
    category = request.GET.get('category', '').strip()
    activity = request.GET.get('activity', '').strip()

    destinations = Destination.objects.none()  

    if query or category or activity:  
        destinations = Destination.objects.all()

        if query:
            destinations = destinations.filter(name__icontains=query)

        if category:
            destinations = destinations.filter(category=category)

        if activity:
            destinations = destinations.filter(activities__activity_type=activity).distinct()

    return render(request, 'travel/search_results.html', {'destinations': destinations})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')  
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def map_view(request):
    destinations = list(Destination.objects.values("name", "latitude", "longitude", "category")) 

    return render(request, 'travel/map.html', {'destinations_json': json.dumps(destinations)})

def nearby_destinations(request):
    try:
        user_lat = float(request.GET.get('lat'))
        user_lon = float(request.GET.get('lon'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid coordinates'}, status=400)

    destinations = Destination.objects.all()
    nearby_places = []

    for destination in destinations:
        dest_coords = (destination.latitude, destination.longitude)
        user_coords = (user_lat, user_lon)
        distance = geodesic(user_coords, dest_coords).km  

        if distance <= 50:  
            nearby_places.append({
                'name': destination.name,
                'category': destination.category,
                'lat': destination.latitude,
                'lon': destination.longitude,
                'distance': round(distance, 2)
            })

    return JsonResponse({'nearby_destinations': nearby_places})

def recommend_destinations(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    similar_destinations = Destination.objects.filter(category=destination.category).exclude(id=destination.id)[:5]

    return render(request, 'travel/recommendations.html', {
        'destination': destination,
        'recommended_destinations': similar_destinations
    })


def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    
    
    all_destinations = Destination.objects.exclude(id=destination.id)
    descriptions = [destination.description] + [d.description for d in all_destinations]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked_destinations = sorted(zip(all_destinations, similarity_scores), key=lambda x: x[1], reverse=True)
    recommended_destinations = [dest[0] for dest in ranked_destinations[:5]]
    recommended_activities = Activity.objects.filter(destination=destination)

    return render(request, 'travel/destination_detail.html', {
        'destination': destination,
        'recommended_destinations': recommended_destinations,
        'recommended_activities': recommended_activities
    })


def destinations_list(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    destinations = Destination.objects.all()

    if query:
        destinations = destinations.filter(name__icontains=query)

    if category:
        destinations = destinations.filter(category=category)

    return render(request, 'travel/destinations.html', {'destinations': destinations})

@login_required
def update_preferences(request):
    if request.method == 'POST':
        categories = request.POST.getlist('categories')
        activities = request.POST.getlist('activities')

        preferences, created = UserPreference.objects.get_or_create(user=request.user)
        preferences.preferred_categories = categories
        preferences.preferred_activities = activities
        preferences.save()

        first_matching_destination = Destination.objects.filter(category__in=categories).first()

        if first_matching_destination:
            return redirect('recommend_destinations', destination_id=first_matching_destination.id)
        else:
            return redirect('destinations')

    return render(request, 'travel/preferences.html')



@login_required
def book_activity(request):
    if request.method == 'POST':
        form = ActivityBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = ActivityBookingForm()

    return render(request, 'travel/book_activity.html', {'form': form})

@login_required
def booking_confirmation(request, booking_id):
    booking = ActivityBooking.objects.get(id=booking_id, user=request.user)
    return render(request, 'travel/booking_confirmation.html', {'booking': booking})

@login_required
def user_bookings(request):
    bookings = ActivityBooking.objects.filter(user=request.user)
    return render(request, 'travel/user_bookings.html', {'bookings': bookings})


@login_required
def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    paginator = Paginator(reviews, 5) 

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'travel/review_list.html', {'reviews': page_reviews})

def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()

    return render(request, 'travel/submit_review.html', {'form': form})


