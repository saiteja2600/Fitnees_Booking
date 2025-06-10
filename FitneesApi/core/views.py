from django.shortcuts import render

def global_home(request):
    return render(request,"global/base.html")