from django.shortcuts import render,HttpResponse
from .models import TodoItem

# Create your views here.
def home(request):
    # return HttpResponse('Hello World!')
    return render(request, 'home.html')

def todos(request):
    todos = TodoItem.objects.all()
    return render(request, 'todos.html', {"todos":todos})

