from django.apps import AppConfig

class IncomesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incomes'

    def ready(self):
        from .models import Source
        sources = [
            "Salary", "Business", "Freelancing", "Part-Time Job",
            "Investments", "Interest", "Dividends", "Rental Income",
            "Online Earnings", "YouTube", "Affiliate Marketing",
            "Stock Trading", "Crypto", "Bonus", "Commission",
            "Gift", "Refund", "Pension", "Government Aid", "Other"
        ]

        for s in sources:
            Source.objects.get_or_create(name=s)
