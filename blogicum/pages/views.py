from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason='', template_name='pages/403csrf.html'):
    return render(request, template_name, status=403)


def server_error(request, template_name='pages/500.html'):
    return render(request, template_name, status=500)
