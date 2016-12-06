# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from main.get_result import Result
from main.ranking import Rank


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


def rank_page(request):
    """
    ランキングページ
    :param request:
    :return:
    """
    if request.method == 'GET':
        situation = request.GET.get('situation')
        rank_result = Rank().get_rank(situation=situation)
        context = {
            "result": rank_result,
            "situation": situation,
            "limit": 20
        }
        return render(request, 'main/ranking.html', context)


def define_page(request):
    """
    状況の定義に関するページ
    :param request:
    :return:
    """
    define = Result().get_data(db_table='semantic')
    define['id'] = define.index
    define = define.to_json(orient='records')
    context = {
        "define": define
    }
    return render(request, 'main/define.html', context)
