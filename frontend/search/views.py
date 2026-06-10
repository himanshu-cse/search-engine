import requests
from django.shortcuts import render

# Create your views here.

def search_view(request):
    query = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    results = []
    total_pages = 1
    total_results = 0
    page_range = []

    if query:
        response = requests.get("http://127.0.0.1:8000/search", params={"q": query, "page": page})
        results = response.json()["results"]
        total_pages = response.json()["total_pages"]
        total_results = response.json()["total_results"]
        page_range = range(1, int(total_pages) + 1)
        
    return render(
        request, 
        "search/search.html", 
        {
            "query": query, 
            "results": results, 
            "page": page, 
            "total_pages": total_pages,
            "page_range": page_range,
            "total_results": total_results
        }
    )

def analytics_view(request):
    response = requests.get("http://127.0.0.1:8000/analytics")
    analytics = response.json()

    return render(request, "search/analytics.html", {"analytics": analytics})