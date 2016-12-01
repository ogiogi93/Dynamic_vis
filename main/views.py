# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from main.get_result import Result


def main_page(request):
    """
    メインページ用
    :param request:
    :return:
    """
    result = Result().main()
    context = {
        "result": result
    }
    return render(request, 'main/index.html', context)
