from django.core.management.base import BaseCommand
from rimori.models import Word
import requests, re

url = 'https://qub10cxllf.execute-api.eu-central-1.amazonaws.com/prod/define/'
vowels = 'aeiouy'
vowels_acute = 'áéíóúý'
consonants = 'bcçdfghjklmnpqrstvwxz'

def is_vowel(letter):
    return letter in vowels + 'ë' + vowels_acute

def count_vowels(word):
    return sum(1 for x in word if is_vowel(x))

def find_accent_index(word, accent_index):
    vowel_count = 0
    for i, l in enumerate(reversed(word)):
        if is_vowel(l):
            vowel_count += 1
            if vowel_count == accent_index:
                index = len(word) - i - 1
                tail = word[index:]
                print(word, tail, i, l)
                Word.objects.create(word=word, tail=tail, index=i, vowel=l)

def find_accent(word):
    number_of_vowels = count_vowels(word)
    if number_of_vowels < 3:
        return find_accent_index(word, number_of_vowels)
    else:
        number_of_vowels = 2
        if re.match('.*[hk][eë]sh([ae]|(i[mnt]))$', word) or\
            re.match('.*ke[mn]i$', word) or \
            re.match('.*jeje$', word) or \
            re.match('.*[aeëiouy]ve$', word) or \
            re.match('.*([uy][aeëiouy])[^aeëiouy].*[aeëiouy].*', word):
            number_of_vowels +=1
        return find_accent_index(word, number_of_vowels)

def get_words_from_exact_match(exact_matches):
    word5 = exact_matches[0]['word5']
    the_split = word5.split('/' if '/' in word5 else ',') # sometimes the word is in this format 'fjalë/-a,-ët'
    if len(the_split) > 1:
        root = the_split[0]
        endings = the_split[1]
        if len(endings) > 1:
            endings = list(map(lambda x: x.replace('-', ''), the_split[1].split(',')))
        else:
            endings = [endings]
        return list(map(lambda x: root + x, endings))
    else:
        return [word5]

def get_word_data(word):
    r = requests.get(url + word) # get the data from fjalorthi API
    res = r.json() # get the json data
    exact_matches = res['exactMatches'] # get the exact matches
    if len(exact_matches):
        words = get_words_from_exact_match(exact_matches) # get the words from the exact matches
        for word in words:
            if any(ext in word for ext in vowels_acute): # if the word has an accent
                vowels_count = 0
                for letter in reversed(word): # iterate over the word backwards
                    if is_vowel(letter):
                        vowels_count += 1
                        if letter in vowels_acute: # if the letter is the accented vowel
                            vowel = vowels[vowels_acute.index(letter)]
                            unaccented_word = word.replace(letter, vowel)
                            find_accent_index(unaccented_word, vowels_count) # get the necessary data
                            break
            else:
                find_accent(word)
                break
    else:
        find_accent(word)

class Command(BaseCommand):
    help = 'Populates the database with accented words'

    def handle(self, *args, **options):
        file = open('data/sq.dic', 'rb').read()
        words = list(map(lambda x: x.split('/')[0], file.decode('latin1').split('\n')))
        for i in range(156778, len(words)):
            get_word_data(words[i])