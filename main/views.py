# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from main.get_result import Result


def main_page(request):
    """
    メインページ用
    :param request:
    :return:
    """
    if request.GET.get('date') is not None:
        date = request.GET.get('date')
        result = Result().main(date=date)
        context = {
            "result": result
        }
        return render(request, 'main/index.html', context)

    result = Result().main()
    context = {
        "result": result
    }
    return render(request, 'main/index.html', context)


def detail_page(request):
    """
    詳細ページ
    :param request:
    :return:
    """

    if request.method == 'GET':
        location_name = request.GET.get('location_name')
        date = request.GET.get('date')
        result = Result().main(location_name=location_name, date=date)
        result_rows = Result().detail(location_name=location_name, date=date)
        context = {
            "location_name": location_name,
            "date": date,
            "result": result,
            "result_rows": result_rows,
        }
        return render(request, 'main/detail.html', context)
    return HttpResponse(status=400)

