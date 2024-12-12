insert into myapp_genre (genre) values ('homme');
insert into myapp_genre (genre) values ('femme');

insert into myapp_SIT_MATRIM (Situation) values ('marie(e)');
insert into myapp_SIT_MATRIM (Situation) values ('célibataire');
insert into myapp_SIT_MATRIM (Situation) values ('divorcé(e)');
insert into myapp_SIT_MATRIM (Situation) values ('veuf(ve)');

INSERT INTO myapp_logiciel (logiciel) VALUES
('SURF'),
('SIGTAS'),
('HETRAONLINE');


INSERT INTO myapp_modepaiement (sens) VALUES
('Depot'),
('Declaration'),
('Espece'),
('Virement');


INSERT INTO myapp_numimpot (impot, numero) VALUES
('IRSA', 5),
('IR', 10),
('IS', 15),
('AMENDE', 43),
('PENALITE', 44);


INSERT INTO myapp_fokontany (wereda_id,fkt_desc) values();
INSERT INTO myapp_wereda (wereda_code,locality_id,wereda_desc)values();
INSERT INTO myapp_locality (city_id,locality_desc,locality_desc_f,locality_desc_s,locality_code) VALUES();
INSERT INTO myapp_city(parish_id,city_name_f,city_code,city_name_extra,city_name_s,city_name) values();
INSERT INTO myapp_parish (id, parish_name, parish_name_f, parish_name_s, parish_code)
VALUES 
((SELECT id FROM myapp_country WHERE country_code = 'MG'), 'Analamanga', 'Analamanga', '', 'ANL'),
((SELECT id FROM myapp_country WHERE country_code = 'MG'), 'Vakinankaratra', 'Vakinankaratra', '', 'VAK');
INSERT INTO myapp_country (country_name, country_name_f, country_name_s, country_code, capital) 
VALUES ('Madagascar', 'Madagascar', 'Madagasikara', 'MG', 'Antananarivo');





INSERT INTO myapp_centralrecette (id_contribuable_id,id_centre_recette,regisseur,logiciel_id,ref_trans,ref_reglement,daty,
    mouvement,moyen_paiement,rib,raison_sociale,nimp_id,libelle,flag,date_debut,date_fin,periode,periode2,mnt_ap,base,imp_detail,da,
    banque,annee_recouvrement,code_bureau,libelle_bureau
) VALUES (
    6,                         
    'NIF123QUITCENTRE',        
    'Regisseur 1',             
    1,                        
    'TRANS123',               
    'REG123',                 
    '2024-01-01',              
    '1',                      
    '01',                     
    'RIB123456789',          
    'Raison Sociale 1',       
    1,                                              
    'Libelle 1',              
    'Y',                       
    '2024-01-01',              
    '2024-12-31',             
    1,                        
    '01-2024',                
    50000.00,                  
    100000.00,                
    'Taxation d''office',   
    1,                         
    'Banque 1',               
    2024,                      
    'Code Bureau 123',        
    'Centre Fiscal 1'          
);


INSERT INTO myapp_paiement (id_contribuable_id,central_recette_id,mode_paiement_id,n_quit,montant,date_paiement) VALUES
(6, 5, 1, 'QUIT126', 50000.00, '2027-02-01'),  
(6, 5, 1, 'QUIT126', 15000.00, '2027-03-01');  






INSERT INTO myapp_videopublicite (
    titre, description, video, lien_video, date_publication, duree, categorie, langue, statut, 
    tags, nombre_vues, auteur, miniature, date_modification
)
VALUES
    (
        'Video Publicitaire 1', 
        'Decouvrez notre premiere video promotionnelle.',
        'videos/facebook-video-y2downloots (1).mp4', 
        NULL, 
        '2024-12-01', 
        '00:02:30', 
        'Promotion', 
        'fr', 
        'publie', 
        'promotion,fonctionnalites,nouvelle', 
        123, 
        'Auteur 1', 
        'images/miniature1.png', 
        '2024-12-03'
    ),
    (
        'Video Publicitaire 2', 
        'Une autre video mettant en avant nos produits.',
        'videos/facebook-video-y2downloots (2).mp4', 
        NULL, 
        '2024-12-02', 
        '00:03:15', 
        'Produit', 
        'fr', 
        'publie', 
        'produit,marketing,visibilite', 
        456, 
        'Auteur 2', 
        'images/miniature2.png', 
        '2024-12-03'
    ),
    (
        'Video Publicitaire 3', 
        'Video speciale pour un evenement a venir.',
        'videos/facebook-video-y2downloots.mp4', 
        NULL, 
        '2024-12-03', 
        '00:01:45', 
        'evenement', 
        'fr', 
        'publie', 
        'evenement,annonce,publicite', 
        789, 
        'Auteur 3', 
        'images/miniature3.png', 
        '2024-12-03'
);


INSERT INTO myapp_brochure (titre, description, fichier_pdf, date_publication)
VALUES
    ('Brochure 1', 'energie-renouvelable_447', '/brochurespdfs/energie-renouvelable_447.pdf', '2024-12-01'),
    ('Brochure 2', 'industrie_448', '/brochurespdfs/industrie_448.pdf', '2024-12-02'),
    ('Brochure 3', 'industrie_449', '/brochurespdfs/industrie_449.pdf', '2024-12-03'),
    ('Brochure 4', 'TRANSPORT_450', '/brochurespdfs/TRANSPORT_450.pdf', '2024-12-04'),
    ('Brochure 5', 'energie-renouvelable_447', '/brochurespdfs/energie-renouvelable_447.pdf', '2024-12-05'),
    ('Brochure 6', 'industrie_448', '/brochurespdfs/industrie_448.pdf', '2024-12-06'),
    ('Brochure 7', 'industrie_449', '/brochurespdfs/industrie_449.pdf', '2024-12-07'),
    ('Brochure 8', 'TRANSPORT_450', '/brochurespdfs/TRANSPORT_450.pdf', '2024-12-08'),
    ('Brochure 9', 'energie-renouvelable_447', '/brochurespdfs/energie-renouvelable_447.pdf', '2024-12-09'),
    ('Brochure 10', 'industrie_44', '/brochurespdfs/industrie_448.pdf', '2024-12-10');


insert into myapp_operateurs(nom,email) values('','');

insert into myapp_operateur(cin,contact) values ('','');