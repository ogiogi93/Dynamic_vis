# -*- coding: utf-8 -*-
import pandas as pd

from main.get_result import Result
from django.db import connection


class Rank(Result):
    def get_rank(self, situation, limit=300):
        """
        指定された状況のスコアトップlimitを返す
        :param situation:
        :param limit:
        :return:
        """
        limit = str(limit)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
              interval,
               location_id,
               stay_time_avg AS stay_time_avg_score,
               num_of_people AS num_of_people_score,
               firstvisit_rate AS firstvisit_rate_score,
               foreign_rate AS foreign_rate_score,
               situation,
               score
            FROM score
            WHERE situation = '""" + situation + """'AND interval::date >= '2016-11-07'
            ORDER BY score
        """)
        features_rank = pd.DataFrame(list(self.dictfetchall(cursor)))
        features = self.get_data(db_table='features')
        features_rank = pd.merge(features_rank, features, on=['interval', 'location_id'])
        # 日付情報を付加
        features_rank['date'] = features_rank['interval'].apply(self.add_date)
        # str型にしないとjsonにした時におかしな値になる
        features_rank['interval'] = features_rank['interval'].astype(str)
        features_rank['date'] = features_rank['date'].astype(str)

        location = self.get_data(db_table='location')
        # 地点情報をmerge
        features_rank = pd.merge(features_rank, location, on=['location_id'])

        return features_rank.to_json(orient='records')
