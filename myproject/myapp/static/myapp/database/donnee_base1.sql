insert into myapp_genre (genre) values ('homme');
insert into myapp_genre (genre) values ('femme');

insert into myapp_SIT_MATRIM (Situation) values ('marié(e)');
insert into myapp_SIT_MATRIM (Situation) values ('célibataire');
insert into myapp_SIT_MATRIM (Situation) values ('divorcé(e)');
insert into myapp_SIT_MATRIM (Situation) values ('veuf(ve)');

INSERT INTO myapp_country (country_name, country_name_f, country_name_s, country_code, capital) 
VALUES ('Madagascar', 'Madagascar', 'Madagasikara', 'MG', 'Antananarivo');

INSERT INTO myapp_parish (id, parish_name, parish_name_f, parish_name_s, parish_code)
VALUES 
((SELECT id FROM myapp_country WHERE country_code = 'MG'), 'Analamanga', 'Analamanga', '', 'ANL'),
((SELECT id FROM myapp_country WHERE country_code = 'MG'), 'Vakinankaratra', 'Vakinankaratra', '', 'VAK');

INSERT INTO myapp_city (id, city_name, city_name_f, city_name_s, city_code, city_name_extra)
VALUES 
((SELECT id FROM myapp_parish WHERE parish_code = 'ANL'), 'Antananarivo', 'Antananarivo', '', 'TNR', 'La capitale'),
((SELECT id FROM myapp_parish WHERE parish_code = 'VAK'), 'Antsirabe', 'Antsirabe', '', 'ASB', 'Ville thermale');


INSERT INTO myapp_locality (id, locality_desc, locality_desc_f, locality_desc_s, locality_code)
VALUES 
((SELECT id FROM myapp_city WHERE city_code = 'TNR'), 'Andohalo', 'Andohalo', '', 'AL01'),
((SELECT id FROM myapp_city WHERE city_code = 'ASB'), 'Mahazoarivo', 'Mahazoarivo', '', 'MR01');

INSERT INTO myapp_wereda (id, wereda_desc, wereda_code)
VALUES 
((SELECT id FROM myapp_locality WHERE locality_code = 'AL01'), 'Commune Urbaine Antananarivo', 101),
((SELECT id FROM myapp_locality WHERE locality_code = 'MR01'), 'Commune Urbaine Antsirabe', 201);

INSERT INTO myapp_fokontany (id, fkt_desc)
VALUES 
((SELECT id FROM myapp_wereda WHERE wereda_code = 101), 'Ambanidia'),
((SELECT id FROM myapp_wereda WHERE wereda_code = 201), 'Ambohimena');