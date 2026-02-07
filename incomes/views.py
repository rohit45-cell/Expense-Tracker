from django.shortcuts import render, redirect
from preferences.models import UserPreference
from .models import Income, Source
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
import json
from django.db.models import Q, F
from django.http import JsonResponse
import datetime
from django.utils import timezone
from datetime import timedelta


# ===============================
# LIST INCOMES
# ===============================
@login_required(login_url='login')
def incomes(request):
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = ""

    incomes_qs = Income.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(incomes_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "currency": currency,
        "page_obj": page_obj
    }
    return render(request, 'incomes/incomes.html', context)


# ===============================
# ADD INCOME
# ===============================
@method_decorator(login_required(login_url='login'), name='dispatch')
class addIncome(View):
    def get(self, request):
        sources = Source.objects.all()
        return render(
            request,
            'incomes/add-income.html',
            {'sources': sources}
        )

    def post(self, request):
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        source_name = request.POST.get('source')
        user = request.user

        sources = Source.objects.all()
        context = {
            'sources': sources,
            'values': request.POST
        }

        if not amount or not description or not date or not source_name:
            messages.error(request, 'All fields are required')
            return render(request, 'incomes/add-income.html', context)

        # ✅ FIX: sanitize amount (remove commas)
        try:
            amount = float(amount.replace(',', ''))
        except ValueError:
            messages.error(request, 'Amount must be a valid number')
            return render(request, 'incomes/add-income.html', context)

        try:
            source = Source.objects.get(name=source_name)
        except Source.DoesNotExist:
            messages.error(request, 'Invalid source selected')
            return render(request, 'incomes/add-income.html', context)

        Income.objects.create(
            user=user,
            amount=amount,
            description=description,
            date=date,
            source=source
        )

        messages.success(request, 'Income added successfully')
        return redirect('incomes')


# ===============================
# EDIT INCOME
# ===============================
@login_required(login_url='login')
def editIncome(request, id):
    try:
        income = Income.objects.get(pk=id, user=request.user)
    except Income.DoesNotExist:
        messages.error(request, 'Income does not exist')
        return redirect('incomes')

    sources = Source.objects.all()

    if request.method == 'GET':
        return render(
            request,
            'incomes/edit-income.html',
            {'income': income, 'sources': sources}
        )

    amount = request.POST.get('amount')
    description = request.POST.get('description')
    date = request.POST.get('date')
    source_name = request.POST.get('source')

    if not amount or not description or not date or not source_name:
        messages.error(request, 'All fields are required')
        return redirect('edit-income', id=id)

    # ✅ FIX: sanitize amount
    try:
        amount = float(amount.replace(',', ''))
    except ValueError:
        messages.error(request, 'Amount must be a valid number')
        return redirect('edit-income', id=id)

    try:
        source = Source.objects.get(name=source_name)
    except Source.DoesNotExist:
        messages.error(request, 'Invalid source selected')
        return redirect('edit-income', id=id)

    income.amount = amount
    income.description = description
    income.date = date
    income.source = source
    income.save()

    messages.success(request, 'Income updated successfully')
    return redirect('incomes')


# ===============================
# DELETE INCOME
# ===============================
@login_required(login_url='login')
def deleteIncome(request, id):
    try:
        income = Income.objects.get(pk=id, user=request.user)
    except Income.DoesNotExist:
        messages.error(request, 'Income does not exist')
        return redirect('incomes')

    income.delete()
    messages.success(request, 'Income deleted successfully')
    return redirect('incomes')


# ===============================
# SEARCH INCOME (AJAX)
# ===============================
@login_required(login_url='login')
def searchIncome(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search', '')

        incomes = Income.objects.filter(
            Q(amount__icontains=search, user=request.user) |
            Q(description__icontains=search, user=request.user) |
            Q(source__name__icontains=search, user=request.user) |
            Q(date__icontains=search, user=request.user)
        ).annotate(
            source=F('source__name')
        ).values('amount', 'description', 'date', 'source')

        return JsonResponse(list(incomes), safe=False)

    return redirect('home')


# ===============================
# INCOME SUMMARY (CHART DATA)
# ===============================
@login_required(login_url='login')
def incomes_summary(request):
    today = timezone.now().date()
    month_ago = today - timedelta(days=30)
    val = request.GET.get('value', 'all')

    if val == "all":
        incomes = Income.objects.filter(user=request.user)
    elif val == "last_30_days":
        incomes = Income.objects.filter(
            user=request.user,
            date__gte=month_ago,
            date__lte=today
        )
    else:
        first_day_current_month = today.replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)

        incomes = Income.objects.filter(
            user=request.user,
            date__gte=first_day_last_month,
            date__lte=last_day_last_month
        )

    result = {}

    for income in incomes:
        source = income.source.name
        result[source] = result.get(source, 0) + income.amount

    return JsonResponse({'income_source_data': result})


# ===============================
# STATS PAGE
# ===============================
@login_required(login_url='login')
def stats(request):
    today = timezone.now().date()
    first_day_current_month = today.replace(day=1)
    last_day_last_month = first_day_current_month - timedelta(days=1)
    last_month_name = last_day_last_month.strftime('%B')

    return render(
        request,
        'incomes/stats.html',
        {'month': last_month_name}
    )
