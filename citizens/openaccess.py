def open_access_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        response['Access-Control-Allow-Origin'] = "*"
        response['Acess-Control-Allow-Headers'] = "*"

        return response
    return middleware