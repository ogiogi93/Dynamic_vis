# -*- coding: utf-8 -*-
import pandas as pd
from django.db import connection
from main.score import Score


class Result(object):
    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def normalize(self, df):
        """
        正規化する
        :param df:
        :return:
        """
        return df.set_index(['interval', 'location_id'])[
            ['stay_time_avg', 'firstvisit_rate', 'num_of_people', 'foreign_rate']].apply(
            lambda x: (x - x.mean()) / x.std(), axis=0).fillna(0).reset_index()

    def cal_score(self, features, semantic):
        """
        距離計算をする
        :param features:
        :param semantic:
        :return:
        """
        # DataFrame型は遅いので、list型に変換する
        features_indexes, features_num_of_people, features_stay_time_avg, features_firstvisit_rate, features_foreign_rate, features_interval, features_location_id = \
            list(features.index), list(features['num_of_people']), list(features['stay_time_avg']), list(
                features['firstvisit_rate']), list(features['foreign_rate']), list(features['interval']), list(
                features['location_id'])
        semantic_indexes, semantic_num_of_people, semantic_stay_time_avg, semantic_firstvisit_rate, semantic_foreign_rate, semantic_situation, semantic_detail = \
            list(semantic.index), list(semantic['num_of_people']), list(semantic['stay_time_avg']), list(
                semantic['firstvisit_rate']), list(semantic['foreign_rate']), list(semantic['situation']), list(
                semantic['detail'])

        score_list = []
        # 定義された状況テーブルと距離計算する
        for features_index in features_indexes:
            for semantic_index in semantic_indexes:
                score = features_num_of_people[features_index] * semantic_num_of_people[semantic_index] + \
                        features_stay_time_avg[features_index] * features_stay_time_avg[semantic_index] + \
                        features_firstvisit_rate[features_index] * semantic_firstvisit_rate[semantic_index] + \
                        features_foreign_rate[features_index] * semantic_foreign_rate[semantic_index]
                score_list.append(Score(features_interval[features_index], features_location_id[features_index],
                                        semantic_situation[semantic_index], semantic_detail[semantic_index], score))
        return score_list

    def get_sensor_data(self):
        """
        DBから特徴量を取得する
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM features WHERE interval::time >= '9:00:00' AND interval::time <= '21:00:00'")
        return pd.DataFrame(list(self.dictfetchall(cursor)))

    def get_data(self, db_table=None):
        """
        DBから特徴量を取得する
        :param db_table:
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + db_table + "")
        return pd.DataFrame(list(self.dictfetchall(cursor)))

    def main(self):
        """
        分析結果を返す
        :return:
        """
        features = self.get_sensor_data()
        semantic = self.get_data(db_table='semantic')
        location = self.get_data(db_table='location')
        features_normed = self.normalize(features)
        score_list = self.cal_score(features=features_normed, semantic=semantic)
        df_semantic_score = pd.DataFrame({'interval': [a.interval for a in score_list],
                                          'location_id': [a.location_id for a in score_list],
                                          'situation': [a.situation for a in score_list],
                                          'detail': [a.detail for a in score_list],
                                          'score': [a.score for a in score_list]})
        # スコアが最も高いものを選択する
        df_semantic_score2 = df_semantic_score.sort_values('score', ascending=False).groupby(
            ['interval', 'location_id'], as_index=False).first()
        final_features = pd.merge(features, df_semantic_score2, on=['interval', 'location_id'])
        final_features = pd.merge(final_features, location, on=['location_id'])

        # str型にしないとjsonにした時におかしな値になる
        final_features['interval'] = final_features['interval'].astype(str)
        return final_features.to_json(orient='records')
