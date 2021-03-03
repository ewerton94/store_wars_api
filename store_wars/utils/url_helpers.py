'''Url helpers'''


def get_photo_url_or_null(response, photo):
    ''''Get url from photo'''
    if photo is None:
        return None
    if photo:
        request = response.wsgi_request
        return f'{request.scheme}://{request.get_host()}{photo.url}'
    return None