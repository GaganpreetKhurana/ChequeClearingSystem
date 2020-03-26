from django.contrib import admin

# Register your models here.
from ChequeClearingSystem.models import payeeBank, bearerBank, payeeBankCheque, bearerBankCheque

admin.site.register(payeeBank)
admin.site.register(bearerBank)
admin.site.register(payeeBankCheque)
admin.site.register(bearerBankCheque)
