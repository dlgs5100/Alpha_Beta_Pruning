from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Post
import json

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    context = {
        'posts_list': posts
    }
    return render(request, 'homepage.html', context)

@csrf_exempt
def returnServer(request):
    json_data = request.POST.get('data')
    list_data = json.loads(json_data)
    print(list_data)
    return render(request, 'homepage.html')