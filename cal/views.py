from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from datetime import date

from .models import CalDia
from .forms import CalForm
from . import utils


def cal(request):
    """Calendar page"""
    today_s_date = utils.get_todays_date()
    calendar_cells = utils.prepare_calendar_cells(2)
    
    current_month_str = today_s_date.strftime("%B")
    context = {'calendar_cells': calendar_cells,
               'today_s_date': today_s_date,
               'current_month_str': current_month_str}
    return render(request, 'cal/calendar.html', context)


@login_required
def edit_cal(request, calday_id):
    """Edit and existing entry."""
    day = CalDia.objects.get(id=calday_id)
    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = CalForm(instance=day)
    else:
        # POST data submitted; process data.
        form = CalForm(instance=day, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:cal')
    
    context = {'day': day, 'form': form}
    return render(request, 'cal/edit_cal.html', context)


@login_required
def new_cal(request, cal_year, cal_month, cal_day):
    """Edit and existing entry."""
    some_day = date(cal_year, cal_month, cal_day)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        caldia = CalDia.objects.create(day=some_day)
        form = CalForm(instance=caldia)
    else:
        # POST data submitted; process data.
        caldia = CalDia.objects.get(day=some_day)
        form = CalForm(instance=caldia, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('cal:cal')
    
    # Display a blank or invalid form.
    context = {'caldia': caldia, 'form': form}
    return render(request, 'cal/new_cal.html', context)
    

@login_required
def edit_all_cal(request):
    """Edit all days on screen."""
    NUMBER_OF_WEEKS = 12
    first_day = utils.get_first_day_of_cal()
    last_day = utils.get_last_day_of_cal(NUMBER_OF_WEEKS)
    CalDiaFormSet = modelformset_factory(CalDia, fields=['farmacia_de_servico', 'info'], extra=0)
    days_of_week = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
    today = utils.get_todays_date()
    
    if request.method != 'POST':
        # No data submitted.
        calendar_cells = utils.prepare_calendar_cells(NUMBER_OF_WEEKS)
        for i in range(len(calendar_cells)):
            if calendar_cells[i][2] == None:
                calendar_cells[i][2] = CalDia.objects.create(day=calendar_cells[i][0], fds_excel=calendar_cells[i][3])
                calendar_cells[i][2].save()
        formset = CalDiaFormSet(queryset=CalDia.objects
                                .filter(day__gte=first_day)
                                .exclude(day__gte=last_day)
                                .order_by('day'))
    else:
        # POST data submitted; process data.
        formset = CalDiaFormSet(request.POST, 
                                queryset=CalDia.objects
                                .filter(day__gte=first_day)
                                .exclude(day__gte=last_day)
                                .order_by('day'))
        if formset.is_valid():
            formset.save()
            return redirect('cal:cal')
        else:
            print("Not valid")
            print(formset.errors)
    
    context = {'today': today, 'days_of_week': days_of_week, 'formset': formset}
    return render(request, 'cal/edit_all_cal.html', context)
