from django.shortcuts import render
from django.utils.safestring import mark_safe
#import json
import uuid

def index(request):
    return render(request, 'chatbot/index.html', {
        'room_name_json': uuid.uuid4()
    })
