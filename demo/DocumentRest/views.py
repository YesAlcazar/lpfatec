from django.shortcuts import render,HttpResponse

# Create your models here.
def home(request):
    # return HttpResponse('Hello World!')
    return render(request, 'home.html')

# Create your views here.
