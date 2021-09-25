from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from rimori.models import Word
from django.db.models import Q
import re

consonants = 'bcdfghjklmnpqrstvwxz'

consonants_dict = {
    'b': '',
    'c': 'c',
    'ç': 'd',
    'd': 'd',
    'dh': 'dh',
    'f': 'f',
    'g': 'g',
    'gj': 'gj',
    'h': 'h',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'll': 'll',
    'm': 'm',
    'n': 'n',
    'nj': 'nj',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    'rr': 'rr',
    's': 's',
    'sh': 'sh',
    't': 't',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'xh': 'xh',
    'y': 'y',
    'z': 'z',
    'zh': 'zh'
}

def browse(request):
    search = request.GET.get('search', '')
    search = re.sub(r'[eë]', '[eë]', search)
    search = re.sub(r'[cç]', '[cç]', search)
    words = Word.objects.filter(word__regex=search)[:10]
    data = serialize('json', words)
    return HttpResponse(data, content_type='application/json')

def rhymes(request):
    word = request.GET.get('word', '')
    tail = request.GET.get('tail', '')

    asonance_regex = '^' + re.sub(r'([bcçdfghjklmnpqrstvwxz]|dh|gj|ll|nj|rr|sh|th|xh|zh)+', '([bcçdfghjklmnpqrstvwxz]|dh|gj|ll|nj|rr|sh|th|xh|zh)+', tail) + '$'
    consonance_regex = '^' + '[aeëiouy]' + re.sub(r'[aeëiouy]', '[aeëiouy]+', tail[1:]) + '$'

    q = Q(tail=tail) | Q(tail__regex=asonance_regex) | Q(tail__regex=consonance_regex)
    words = Word.objects.filter(q).exclude(word=word)

    a = []
    for word in words:
        d = {}
        d['word'] = word.word
        d['index'] = word.index
        if word.tail == tail:
            d['type'] = 'r'
        elif re.match(asonance_regex, word.tail):
            d['type'] = 'a'
        elif re.match(consonance_regex, word.tail):
            d['type'] = 'c'
        a.append(d)
    return JsonResponse(a, safe=False)