from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def petitions_index(request):
    petitions = Petition.objects.all().order_by('-created_at')
    template_data = {'title': 'Petitions', 'petitions': petitions}
    return render(request, 'movies/petitions_index.html', {'template_data': template_data})

@login_required
def petition_create(request):
    if request.method == 'GET':
        template_data = {'title': 'New Petition'}
        return render(request, 'movies/petition_create.html', {'template_data': template_data})

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    if title == '':
        template_data = {'title': 'New Petition', 'error': 'Title is required'}
        return render(request,'movies/petition_create.html', {'template_data': template_data})

    petition = Petition(title=title, description=description, proposer=request.user)
    petition.save()
    return redirect('movies.petitions_index')

def petition_detail(request, id):
    petition = get_object_or_404(Petition, id=id)
    user_voted = False
    if request.user.is_authenticated:
        user_voted = PetitionVote.objects.filter(petition=petition, user=request.user).exists()
    
    template_data = {'title': petition.title, 'petition': petition, 'user_voted': user_voted}
    return render(request,'movies/petition_detail.html', {'template_data': template_data})

@login_required
def petition_vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    try:
        vote = PetitionVote(petition=petition, user=request.user)
        vote.save()
    except IntegrityError:
        pass
    
    return redirect('movies.petition_detail', id=id)

@login_required
def petition_unvote(request, id):
    petition = get_object_or_404(Petition, id=id)
    PetitionVote.objects.filter(petition=petition, user=request.user).delete()
    return redirect('movies.petition_detail', id=id)