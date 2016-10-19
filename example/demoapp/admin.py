from django.contrib import admin

from unitology.forms import UnitsFieldFormMixin

from .models import Person


class PersonChangeForm(UnitsFieldFormMixin):

    class Meta:
        model = Person
        fields = ['name', 'units', 'weight', 'height']


class PersonAdmin(admin.ModelAdmin):
    form = PersonChangeForm


admin.site.register(Person, PersonAdmin)
