# -*- coding: utf-8 -*-
import pandas as pd
from django.db import connection
from main.score import Score
from main.interval_location import IntervalLocation


class Result(object):
    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def add_date(self, d):
        """
        日付を返す
        :param d:
        :return:
        """
        return d.date()

    def normalize(self, df):
        """
        地点ごとに正規化する
        :param df:
        :return:
        """
        location_ids = df['location_id'].unique().tolist()
        for i, location_id in enumerate(location_ids):
            selected = df[df['location_id'] == location_id]
            if i == 0:
                normalized = selected.set_index(['interval', 'location_id'])[
                    ['stay_time_avg', 'firstvisit_rate', 'num_of_people', 'foreign_rate']].apply(
                    lambda x: (x - x.mean()) / x.std(), axis=0).fillna(0).reset_index()
            else:
                temp = selected.set_index(['interval', 'location_id'])[
                    ['stay_time_avg', 'firstvisit_rate', 'num_of_people', 'foreign_rate']].apply(
                    lambda x: (x - x.mean()) / x.std(), axis=0).fillna(0).reset_index()
                normalized = pd.concat([normalized, temp], axis=0)
        return normalized.reset_index(drop=True)

    def country_label(self, country):
        """
        countryに関するラベル付けをする
        :param country:
        :return:
        """
        return '日本' if country == 'ja' else '日本国外'

    def first_visit_label(self, first):
        """
        first_visitに関するラベル付をする
        :param first_visit:
        :return:
        """
        return '初回訪問' if first == 1 else '複数訪問'

    def situation_label(self, situation):
        """
        situationに関するラベル付をする
        :param situation:
        :return:
        """
        if situation == 'Danger':
            return 5
        elif situation == 'Event':
            return 4
        elif situation == 'congestion':
            return 3
        elif situation == 'confuse':
            return 2
        else:
            return 1

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

    def get_sensor_data(self, db_table=None, date=None):
        """
        DBからセンサデータを取得する
        :param db_table:
        :param date:
        :return:
        """
        cursor = connection.cursor()
        if date is not None:
            cursor.execute(
                "SELECT * FROM " + db_table + " WHERE interval::time >= '9:00:00' AND interval::time <= '21:00:00' AND "
                                              "interval::date = '" + date + "'")
        else:
            cursor.execute(
                "SELECT * FROM " + db_table + " WHERE interval::time >= '9:00:00' AND interval::time <= '21:00:00'")
        return pd.DataFrame(list(self.dictfetchall(cursor)))

    def get_data(self, db_table=None):
        """
        DBからその他データを取得する
        :param db_table:
        :return:
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + db_table + "")
        return pd.DataFrame(list(self.dictfetchall(cursor)))

    def completion_feature(self, features):
        """
        欠損値を補完する
        :param features:
        :return:
        """
        intervals = features['interval'].astype(str).unique().tolist()
        # locations = features['location_id'].unique().tolist()
        locations = [1, 2, 3, 4, 5]

        interval_location_list = []
        for interval in intervals:
            for location in locations:
                interval_location_list.append(IntervalLocation(interval, location))

        df_interval_location = pd.DataFrame({'interval': [a.interval for a in interval_location_list],
                                             'location_id': [a.location for a in interval_location_list]})
        df_interval_location['interval'] = pd.to_datetime(df_interval_location['interval'])
        final_features = pd.merge(df_interval_location, features, on=['interval', 'location_id'], how='left')
        final_features['situation'] = final_features['situation'].fillna('Stable')
        final_features['detail'] = final_features['detail'].fillna('平常状態')
        final_features = final_features.fillna(0)

        return final_features

    def detail(self, location_name=None, date=None):
        """
        詳細情報を返す
        :param location_name:
        :param date:
        :return:
        """
        features_row = self.get_sensor_data(db_table='features_row', date=date)
        features = self.get_sensor_data(db_table='features')
        location = self.get_data(db_table='location')
        features_row2 = pd.merge(features_row, location, on=['location_id'])
        features_row2 = pd.merge(features_row2, features, on=['location_id', 'interval'])

        features_row2['date'] = features_row2['interval'].apply(self.add_date)
        # 地点で絞り込む
        final_features = features_row2[features_row2['location_name'] == location_name]
        # str型にしないとjsonにした時におかしな値になる
        final_features['interval'] = final_features['interval'].astype(str)
        final_features['date'] = final_features['date'].astype(str)

        # 可視化用にラベル付をする
        final_features['country'] = final_features['country'].apply(self.country_label)
        final_features['first_visit'] = final_features['first_visit'].apply(self.first_visit_label)

        return final_features.to_json(orient='records')

    def main(self, location_name=None, date='2016-11-10'):
        """
        集計結果を返す
        :param location_name:
        :param date:
        :return:
        """
        features = self.get_sensor_data(db_table='features', date=date)
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

        # 欠損値を補完する
        final_features = self.completion_feature(final_features)

        # 日付情報を付加
        final_features['date'] = final_features['interval'].apply(self.add_date)
        # str型にしないとjsonにした時におかしな値になる
        final_features['interval'] = final_features['interval'].astype(str)
        final_features['date'] = final_features['date'].astype(str)

        # 地点情報をmerge
        final_features = pd.merge(final_features, location, on=['location_id'])
        if location_name and date:
            # 日付、地点が指定されていた場合
            final_features = final_features[
                (final_features['date'] == date) & (final_features['location_name'] == location_name)].reset_index(
                drop=True)
        # 意味解析結果ラベルを抽出する
        final_features['situation_label'] = final_features['situation'].apply(self.situation_label)
        return final_features.to_json(orient='records')
