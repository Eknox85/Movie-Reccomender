from django.shortcuts import render, redirect
from django.db import connection
import requests

def home(request):
    return render(request, "index.html")

def page1(request):
    if request.method == "POST":
        genre = request.POST.get("genre")
        if genre:
            request.session["genre"] = genre
            return redirect("page2")
    return render(request, "page1.html")

def page2(request):
    if request.method == "POST":
        
        pacing = request.POST.get("pacing")
        print(f"Selected Answer: {pacing}")  # Debugging
        if pacing:
            request.session["pacing"] = pacing
            return redirect("page3")
    return render(request, "page2.html")

def page3(request):
    if request.method == "POST":
        global length
        length = request.POST.get("length")
        print(f"Selected Answer: {length}")  # Debugging
        if length:
            request.session["length"] = int(length)
            return redirect("page4")
    return render(request, "page3.html")


def page4(request):
    if request.method == "POST":
        global service
        service = request.POST.get("service")
        print(f"Selected Answer: {service}")  # Debugging
        if service:
            request.session["service"] = service
            return redirect("page5")
    return render(request, "page4.html")

def page5(request):
    if request.method == "POST":
        global ending
        ending = request.POST.get("ending")
        print(f"Selected Answer: {ending}")  # Debugging
        if ending:
            request.session["ending"] = ending
            return redirect("finalpage")
    return render(request, "page5.html")


TMDB_API_KEY = "ee48820e347d17722eeed0f4d09d14ca"  # Replace this with your actual key

def get_tmdb_poster(movie_title):
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    response = requests.get(search_url, params=params)
    data = response.json()
    if data.get("results"):
        poster_path = data["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


def finalpage(request):
    genre = request.session.get("genre")
    service = request.session.get("service")

    query = """
        SELECT id FROM movie_stats 
        WHERE genre LIKE %s
        AND services LIKE %s
        LIMIT 5
    """
    params = (f"%{genre}%", f"%{service}%")
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        resultsid = cursor.fetchall()

    ids = tuple(row[0] for row in resultsid) if resultsid else ()

    if not ids:
        return render(request, 'finalpage.html', {'results': None})

    query2 = "SELECT * FROM movie_db WHERE id IN %s"
    with connection.cursor() as cursor:
        cursor.execute(query2, [ids])
        results = cursor.fetchall()

    if not results:
        return render(request, 'finalpage.html', {'results': None})

    # Get only the first result from the query
    first_movie = results[0]

    # Add the poster URL if available
    poster_url = get_tmdb_poster(first_movie[1])  # first_movie[1] is the movie title

    # Add the movie data into the context for rendering
    results_with_posters = [{
        'year': first_movie[0],    # Movie Title
        'title': first_movie[1],    # Genre
        'genre': first_movie[2],     # Mood
        'des': first_movie[3],  # Setting
        'rating': first_movie[4],   # Rating
        'poster': poster_url,       # Poster URL
    }]
    print(ids)
    print(results)
    return render(request, 'finalpage.html', {'results': results_with_posters})