from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,    get_list_or_404


def index(request):
    return render(request, 'index.html')
