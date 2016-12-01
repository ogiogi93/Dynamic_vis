DROP TABLE IF EXISTS location;

CREATE TABLE location(
  location_id INTEGER,
  location_name VARCHAR(20),
  location_eng VARCHAR(20)
);


INSERT INTO location(location_id, location_name, location_eng) VALUES (1, '食堂', 'Refectory');
INSERT INTO location(location_id, location_name, location_eng) VALUES (2, '生協', 'Shop');
INSERT INTO location(location_id, location_name, location_eng) VALUES (3, '大教室', 'Auditorium');
INSERT INTO location(location_id, location_name, location_eng) VALUES (4, '小教室', 'Lecture Room');
INSERT INTO location(location_id, location_name, location_eng) VALUES (5, 'メディアセンター', 'Media Centor');
