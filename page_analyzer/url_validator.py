from urllib.parse import urlparse


def normalize_url(url):
    '''
    :param url:
    :return: normalized URL including only the scheme and host.
    example: normalize_url("https://ru.hexlet.io/projects/83/members/44838")
    will return "https://ru.hexlet.io"
    '''
    p = urlparse(url)
    result = p.scheme + '://' + p.hostname
    return result


def validate_url(url):
    errors = []
    if not validators.url(url) or len(url) > 255:
        errors.append(('Некорректный URL', 'danger'))
    return errors