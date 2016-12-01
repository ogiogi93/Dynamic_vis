# -*- coding: utf-8 -*-
class Score(object):
    def __init__(self, interval, location_id, situation, detail, score):
        self.interval = interval
        self.location_id = location_id
        self.situation = situation
        self.detail = detail
        self.score = score

    def interval(self):
        return self.interval

    def location_id(self):
        return self.location_id

    def situation(self):
        return self.situation

    def detail(self):
        return self.detail

    def score(self):
        return self.score
