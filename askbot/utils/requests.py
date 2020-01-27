def get_request_method_arg(request):
    if request.method == 'POST':
        return request.POST

    return request.GET

