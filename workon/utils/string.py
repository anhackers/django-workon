import unicodedata, re, json
from django.utils.encoding import force_str, force_text
from django.utils.text import Truncator, slugify as django_slugify, mark_safe
from django.utils.encoding import force_text
from django.utils import six

# space_chars = re.compile(r"[\.\'\"\_\-\,\?\(\)\[\]]")

__all__ = [
    "forceunicode",
    "normalize",
    "normalize_hard",
    "slugify",
    "prepare_for_search",
    "jsonify",
    "truncatechars",
    "truncatewords"
]

def forceunicode(string):
    enc = 'utf-8'
    try: return string.decode(enc)
    except:
        enc = 'ISO-8859-1'
        try: return string.decode(enc)
        except:
            enc = 'ascii'
            try: return string.decode(enc)
            except: return string
    return string

def jsonify(obj):
    class Encoder(json.JSONEncoder):
        def default(self, obj):
            if not isinstance(obj, (dict, list, str, bytes)):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    if obj is None:
        return "{}"
    if isinstance(obj,dict):
        return json.dumps(obj, cls=Encoder)
    elif isinstance(obj,list):
        return json.dumps(obj, cls=Encoder)
    elif type(obj) == type({}.keys()):
        return json.dumps(list(obj), cls=Encoder)
    elif isinstance(obj, six.string_types):
        obj = re.sub(r'([\w\d_]+)\:', '"\\1":', obj)
        obj = re.sub(r'\'', '"', obj)
        obj = re.sub(r'\/\/\s*[\w\s\d]+', '', obj)
        obj = re.sub(r'Date\.UTC\(.+\)', '""', obj)

        try:
            return json.dumps(json.loads(obj), cls=Encoder)
        except:
            return json.loads(json.dumps(obj, cls=Encoder))
    else:
        return obj

def strip_accents(string, accents=('COMBINING ACUTE ACCENT', 'COMBINING GRAVE ACCENT', 'COMBINING TILDE')):
    accents = set(map(unicodedata.lookup, accents))
    chars = [c for c in unicodedata.normalize('NFD', string) if c not in accents]
    return unicodedata.normalize('NFC', ''.join(chars))

def slugify(string, allow_unicode=False):
    return django_slugify(string)

def normalize(value):
    return slugify(value)

def normalize_hard(value):
    value = normalize(value)
    return value

def prepare_for_search(string, default=""):
    if not string: return default
    if not isinstance(string, six.string_types): string = forceunicode(string)
    string = string.replace(u'“', ' ')
    string = string.replace(u'”', ' ')
    string = string.replace(u'"', ' ')
    string = string.replace(u"'", ' ')
    string = string.replace(u'’', " ")
    string = string.replace(u'–', " ")
    string = string.replace(u'_', " ")
    return slugify(string).replace('-', ' ').lower().strip()


def truncatechars(value, length=100, truncate=' ...', html=True):
    return Truncator(str(value)).chars(length, truncate=truncate, html=html)

def truncatewords(value, length=100, truncate=' ...', html=True):
    return Truncator(str(value)).words(length, truncate=truncate, html=html)