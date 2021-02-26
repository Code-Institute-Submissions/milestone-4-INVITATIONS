from django.shortcuts import render


def handler500(request,  *args, **argv):
    return render(request, '500.html', status=500)
