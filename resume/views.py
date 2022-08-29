from django.shortcuts import render

# Create your views here.
def resume_url(request):
    return render(request, 'resume/index.html')