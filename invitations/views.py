from django.shortcuts import render


def error_404(request, exception, template_name='invitations/404.html'):
    return render(request, template_name)


def error_500(request, template_name='invitations/500.html'):
    return render(request, template_name)
