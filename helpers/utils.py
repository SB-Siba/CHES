from .decorators import *
import base64
from django.core.paginator import Paginator
import uuid
from urllib.parse import parse_qs

def generate_unique_id(digit):
    return str(int(str(uuid.uuid4().int)[:digit]))


def encoding_string(string_data):
    encoded_bytes = base64.b64encode(string_data.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_string(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string



def paginate(request,data_list,number=25, query_page=1):

    paginator = Paginator(data_list, number)
    page_number = request.GET.get('page',query_page)
    page_obj = paginator.get_page(page_number)
    return page_obj


def query_string_to_dict(query_string):
    query_parameters = parse_qs(query_string)
    query_parameters = {key: value[0] for key, value in query_parameters.items()}
    return query_parameters