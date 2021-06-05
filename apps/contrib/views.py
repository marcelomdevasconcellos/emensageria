import os
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json

# Create your views here.

def dashboard_json(request):
    dashboars_data = {
        'reinf_quant_cadastrados': 8,
        'reinf_quant_importados': 9,
        'reinf_quant_erros_validacao': 10,
        'reinf_quant_validados': 11,
        'reinf_quant_erros_envio': 12,
        'reinf_quant_enviados': 13,
        'reinf_quant_processados': 14,
    }
    return HttpResponse(json.dumps(dashboars_data, indent=4))
