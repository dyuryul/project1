from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Review
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings


def index(request):
    reviews = Review.objects.all()
    context = { 'reviews': reviews}
    return render(request, 'reviews/index.html', context)
    
def detail(request, review_id):
    review = Review.objects.get(id=review_id)
    context = { 'review': review }
    return render(request, 'reviews/detail.html', context)
    
@login_required
def new(request):
    return render(request, 'reviews/new.html')
    
@login_required
def create(request):
    user = request.user
    body = request.POST['body']
    image = None
    if 'image' in request.FILES:
        image = request.FILES['image']
    review = Review(user=user, body=body, image=image, created_at=timezone.now())
    review.save()
    return redirect('reviews:detail', review_id=review.id)
    
@login_required
def edit(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except review.DoesNotExist:
        return redirect('reviews:index')
    context = { 'review': review }
    return render(request, 'reviews/edit.html', context)
   
@login_required
def update(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except review.DoesNotExist:
        return redirect('reviews:index')
    review.body = request.POST['body']
    if'image' in request.FILES:
       review.image = request.FILES['image']
    
    review.save()
    return redirect('reviews:detail', review_id=review.id)
    
@login_required
def delete(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except review.DoesNotExist:
        return redirect('reviews:index')
    review.delete()
    return redirect('reviews:index')
    
@login_required
def like(request, review_id):
    
    if request.method == 'POST':
        try:
            review = Review.objects.get(id=review_id)
            
            if request.user in review.liked_users.all():
                review.liked_users.remove(request.user)
            else:
                review.liked_users.add(request.user)
            return redirect('reviews:detail', review.id)
        except review.DoesNotExist:
            pass
    
    return redirect('reviews:index')
    

def youtube(request):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'maxResults': '10',
        'q': '민아',
    }
    
    response = requests.get(url, params)
    
    response_dict = response.json()
    

    context = {
        'youtube_items': response_dict['items']
    }
    
    return render(request, 'reviews/youtube.html', context)