DROP TABLE IF EXISTS semantic;

CREATE TABLE semantic(
    id SERIAL PRIMARY KEY,
    situation varchar(120),
    detail varchar(255),
    num_of_people float,
    stay_time_avg float,
    firstvisit_rate float,
    foreign_rate float
);

INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Complex', '訪日外国人などの慣れていない人々が多く長時間滞在している状況', 1, 1, 1, 1);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Event', '初めて訪問した人々が多くいる状況', 1, 0, 1, 0);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('First Coming', '訪日外国人などの慣れていない人々が多く滞在している状況', 0, 0, 1, 1);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Congestion', '人々が多く滞在している状況', 1, 0, 0, 0);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Stable', '平常状態', -1, -1, -1, -1);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Stable', '平常状態', -1, 0, -1, 0);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Stable', '平常状態', 0, 0, -1, -1);
INSERT INTO semantic(situation,detail,num_of_people,stay_time_avg,firstvisit_rate,foreign_rate) VALUES
('Stable', '平常状態', -1, 0, 0, 0);
