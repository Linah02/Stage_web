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

cd 