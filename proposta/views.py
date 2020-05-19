# -*- Mode: Python; coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from proposta.core.models import Cliente, Proposta


# Proposta
@login_required(redirect_field_name='redirect_to')
def proposta(request, id=None, *args, **kwargs):
	contexto = {}
	contexto['proposta_base'] = Proposta.objects.get(id=id)

	return render(request, "proposta.html", contexto)