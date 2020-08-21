from django.contrib import admin
from bookinventery import models

admin.site.register(models.BookCategories)
admin.site.register(models.BookDetail)
admin.site.register(models.Transaction)
