# -*- Mode: Python; coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Cliente, Proposta
from django.utils.html import format_html
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg

class TotalChangeList(ChangeList):
	fields_to_total = ['valor',]

	def get_total_values(self, queryset):
		total = Proposta()
		total.custom_alias_name = "Totals"
		for field in self.fields_to_total:
			setattr(total, field, queryset.aggregate(total=Sum('valor'))['total'])
		return total

	def get_results(self, request):
		super(TotalChangeList, self).get_results(request)
		total = self.get_total_values(self.queryset)
		len(self.result_list)
		self.result_list._result_cache.append(total)


class PropostaAdmin(admin.ModelAdmin):

	def get_changelist(self, request, **kwargs):
		return TotalChangeList

	
	list_display = ['cliente', 'data',  'status', 'pago', 'valor', 'imprimir']
	search_fields = ['cliente__nome']
	list_filter = ['cliente__nome', 'data', 'situacao']
	# list_editable = ['valor']
	list_per_page = 30
	save_on_top=True

	def status(self, obj):
		if obj.situacao == 'Pago':
			color = 'green'
		elif obj.situacao == 'Atrasado':
			color = 'red'
		else:
			color = 'orange'
		return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.situacao))

	status.allow_tags = True

class ClienteAdmin(admin.ModelAdmin):
	pass

admin.site.register(Proposta, PropostaAdmin)
admin.site.register(Cliente, ClienteAdmin)