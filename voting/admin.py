from django.contrib import admin
from django.utils.html import format_html
from .models import Party, Vote

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'bengali_name', 'symbol_preview', 'color', 'vote_count', 'order']
    ordering = ['order']

    def symbol_preview(self, obj):
        if obj.symbol:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:contain;" />', obj.symbol.url)
        return "No image"
    symbol_preview.short_description = 'Symbol'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'party', 'voted_at']
    list_filter = ['party']
    readonly_fields = ['voted_at']
