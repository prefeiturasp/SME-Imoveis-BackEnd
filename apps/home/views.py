# -*- encoding: utf-8 -*-
import json
from django.db import connection
from django.shortcuts import HttpResponse
from django.views.generic.base import View
from sme_ofertaimoveis.config.settings.base import BASE_DIR


class CreateProcedure(View):

    fn = None

    def create_stored_procedure(self) -> str:
        result = 'Create Stored Procedure Sucefully!'
        self.fn = str(BASE_DIR.path('dbscripts', 'procedure.sql'))
        try:
            f = open(self.fn, 'r')
            with connection.cursor() as cursor:
                cursor.execute(f.read())
        except Exception as e:
            result = f'Erro ao rodar o script no banco de dados!\n  ==> {e}'
        return result

    def get(self, request, *args, **kwargs):
        data = {
            'status_code': 200,
            'message': 'Create Stored Procedure Sucefully!'
        }
        try:
            data['message'] = self.create_stored_procedure()
        except Exception as e:
            data['status_code'] = 500
            data['message'] = f'Error: Error on Create Stored Procedure\n{e}'
        data['base_dir'] = self.fn
        return HttpResponse(json.dumps(data), content_type='application/json')


class ExecuteProcedure(View):

    def execute_stored_procedure(self) -> str:
        result = 'Run Stored Procedure Sucefully!'
        try:
            with connection.cursor() as cursor:
                cursor.execute('call public.detect_bidder_duplicity();')
        except Exception as e:
            result = f'Erro ao rodar a stored procedure detect_bidder_duplicity!\n  ==> {e}'
        return result

    def get(self, request, *args, **kwargs):
        data = {
            'status_code': 200,
            'message': 'Run Stored Procedure Sucefully!'
        }
        try:
            data['message'] = self.execute_stored_procedure()
        except Exception as e:
            data['status_code'] = 500
            data['message'] = f'Error: Error on Create Stored Procedure\n{e}'
        return HttpResponse(json.dumps(data), content_type='application/json')
