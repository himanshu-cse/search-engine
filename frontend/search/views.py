import requests
from django.shortcuts import render

# Create your views here.

def search_view(request):
    query = request.GET.get("q", "")

    results = []

    if query:
        response = requests.get("http://127.0.0.1:8000/search", params={"q": query})
        results = response.json()

    return render(request, "search/search.html", {"query": query, "results": results})

def analytics_view(request):
    response = requests.get("http://127.0.0.1:8000/analytics")
    analytics = response.json()

    return render(request, "search/analytics.html", {"analytics": analytics})