from datetime import date, timedelta
import locale
import os
from typing import List

import pandas as pd

from cal.models import CalDia


def get_todays_date() -> date:
    """Return today's date or other for debugging."""
    locale.setlocale(locale.LC_TIME, 'pt_PT')
    today_s_date = date.today()
    # today_s_date = date(2023, 1, 20)
    return today_s_date


def get_first_day_of_cal() -> date:
    """Return first calendar day to be displayed."""
    today_s_date = get_todays_date()
    today_s_weekday = today_s_date.weekday()
    first_cal_day = today_s_date - timedelta(days=today_s_weekday)
    return first_cal_day


def get_last_day_of_cal(number_of_weeks:int) -> date:
    """Return last day of calendar to be displayed."""
    number_of_days = number_of_weeks * 7
    last_cal_day = get_first_day_of_cal() + timedelta(days=number_of_days)
    return last_cal_day


def prepare_calendar_cells(number_of_weeks:int) -> List:
    """Prepare a list of calendar cells to display in template.
    Return a list of these cells."""

    first_day = get_first_day_of_cal()
    last_day = get_last_day_of_cal(number_of_weeks)
    time_diff = last_day - first_day
    days_in_calendar = [first_day + timedelta(days=i) for i in range(time_diff.days)]

    cal_dias = CalDia.objects.filter(day__gte=first_day).exclude(day__gte=last_day)

    calendar_cells = []
    for i in range(len(days_in_calendar)):
        day_of_week = days_in_calendar[i].strftime("%A")[:3]
        calendar_cells.append([days_in_calendar[i], day_of_week, None, None])

    if first_day.year == 2022:    
        get_farmacias_for_2022(calendar_cells)

    if last_day.year == 2023 or first_day.year == 2023:
        get_farmacias_for_2023(calendar_cells)

    for cd in cal_dias:
        for i in range(len(calendar_cells)):
            if cd.day == calendar_cells[i][0]:
                calendar_cells[i][2] = cd

    return calendar_cells


def get_farmacias_for_2023(calendar_cells:List):
    """Get information of Farmacias de Servico for 2023."""
    
    farmacias_tables = get_excel_tables_2023()

    if len(farmacias_tables) == 12:
        for i in range(len(calendar_cells)):
            i_month = calendar_cells[i][0].month - 1
            for r in range(len(farmacias_tables[i_month])):
                if (calendar_cells[i][0].day == farmacias_tables[i_month].iloc[r, 0] 
                        and calendar_cells[i][0].year == 2023):
                    calendar_cells[i][3] = farmacias_tables[i_month].iloc[r, 4].split("|")[0].title()


def get_excel_tables_2023():
    """Go through ecxel file, retreive farmcias de servico and return a list."""
    xls_file = "farmacias_de_servico_2023.xlsx"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, xls_file)
    farmacias_tables = []
    try:
        with pd.ExcelFile(file_path) as xls:
            for i in range(len(xls.sheet_names)):
                sn = 'Sheet' + str(i + 1)
                farmacias_tables.append(pd.read_excel(xls, sheet_name=sn, usecols='A:E'))
    except IOError:
        print("Could not open file 2023")

    return farmacias_tables

def get_farmacias_for_2022(calendar_cells:List):
    """Get information of Farmacias de Serviço for 2022."""

    farmacias_tables = get_excel_tables_2022()

    if len(farmacias_tables) == 12:
        for i in range(len(calendar_cells)):
            i_month = calendar_cells[i][0].month - 1
            for x in range(len(farmacias_tables[i_month].columns)):
                for y in range(len(farmacias_tables[i_month])):
                    if (calendar_cells[i][0].day == 
                            farmacias_tables[i_month].iloc[y, x] 
                            and calendar_cells[i][0].year == 2022):
                        calendar_cells[i][3] = farmacias_tables[i_month].iloc[y, x + 1]
            

def get_excel_tables_2022() -> List:
    """Prepare Farmacia tables from 2022 from an EXCEL file.
    Return a List."""
    xls_file = "farmacias_de_servico.xlsx"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, xls_file)
    farmacias_tables = []
    try:
        with pd.ExcelFile(file_path) as xls:
            for i in range(len(xls.sheet_names)):
                sn = 'Sheet' + str(i + 1)
                farmacias_tables.append(pd.read_excel(xls, sheet_name=sn, usecols='B:O'))
    except IOError:
        print("Could not open file 2022")

    return farmacias_tables