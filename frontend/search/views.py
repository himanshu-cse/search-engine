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
        pagination_pages = []

        if int(total_pages) <= 7:
            pagination_pages = range(1, int(total_pages) + 1)
        else:
            pagination_pages.append(1)

            start = max(2, page - 2)
            end = min(int(total_pages) - 1, page + 2)

            if start > 2:
                pagination_pages.append("...")

            for p in range(start, end + 1):
                pagination_pages.append(p)

            if end < total_pages - 1:
                pagination_pages.append("...")

            pagination_pages.append(int(total_pages))
        
    return render(
        request, 
        "search/search.html", 
        {
            "query": query, 
            "results": results, 
            "page": page, 
            "total_pages": total_pages,
            "pagination_pages": pagination_pages,
            "total_results": total_results
        }
    )

def analytics_view(request):
    response = requests.get("http://127.0.0.1:8000/analytics")
    analytics = response.json()

    return render(request, "search/analytics.html", {"analytics": analytics})