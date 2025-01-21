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


INSERT INTO myapp_country (country_name, country_name_f, country_name_s, country_code, capital)
VALUES
('Madagascar', 'Madagasikara', 'Madagasikara', 'MG', 'Antananarivo');

-- Insérer les paroisses pour la province d'Antananarivo
INSERT INTO myapp_parish (country_id, parish_name, parish_name_f, parish_name_s, parish_code)
VALUES
(1, 'Antananarivo', 'Antananarivo', 'Antananarivo', '001'),
(1, 'Itasy', 'Itasy', 'Itasy', '002');

-- Insérer les paroisses pour la province de Toamasina
INSERT INTO myapp_parish (country_id, parish_name, parish_name_f, parish_name_s, parish_code)
VALUES
(1, 'Toamasina', 'Toamasina', 'Toamasina', '003'),
(1, 'Atsinanana', 'Atsinanana', 'Atsinanana', '004');


-- Insérer des villes pour la paroisse d'Antananarivo
INSERT INTO myapp_city (parish_id, city_name_f, city_code, city_name_extra, city_name_s, city_name)
VALUES
(1, 'Antananarivo', '001', 'Antananarivo Ville', 'Antananarivo', 'Antananarivo City'),
(1, 'Ambohijatovo', '002', 'Ambohijatovo City', 'Ambohijatovo', 'Ambohijatovo');

-- Insérer des villes pour la paroisse de Toamasina
INSERT INTO myapp_city (parish_id, city_name_f, city_code, city_name_extra, city_name_s, city_name)
VALUES
(3, 'Toamasina', '003', 'Toamasina Ville', 'Toamasina', 'Toamasina City'),
(3, 'Foulpointe', '004', 'Foulpointe City', 'Foulpointe', 'Foulpointe');

-- Insérer des localités pour la ville d'Antananarivo
INSERT INTO myapp_locality (city_id, locality_desc, locality_desc_f, locality_desc_s, locality_code)
VALUES
(1, 'Centre Ville', 'Centre Ville', 'Centre Ville', '0001'),
(1, 'Ankorondrano', 'Ankorondrano', 'Ankorondrano', '0002');

-- Insérer des localités pour la ville de Toamasina
INSERT INTO myapp_locality (city_id, locality_desc, locality_desc_f, locality_desc_s, locality_code)
VALUES
(3, 'Centre Ville', 'Centre Ville', 'Centre Ville', '0003'),
(3, 'Foulpointe', 'Foulpointe', 'Foulpointe', '0004');


-- Insérer des weredas pour Antananarivo
INSERT INTO myapp_wereda (wereda_code, locality_id, wereda_desc)
VALUES
(1, 1, 'Antananarivo District'),
(2, 2, 'Ankorondrano District');

-- Insérer des weredas pour Toamasina
INSERT INTO myapp_wereda (wereda_code, locality_id, wereda_desc)
VALUES
(3, 3, 'Toamasina District'),
(4, 4, 'Foulpointe District');

INSERT INTO myapp_fokontany (wereda_id, fkt_desc)
VALUES
(1, 'Fokontany d''Antananarivo Ville'),
(1, 'Fokontany de Soavimasoandro'),
(2, 'Fokontany d''Ambohijatovo'),
(2, 'Fokontany de Antsirabe II'),
(2, 'Fokontany de Ankadifotsy');


INSERT INTO myapp_fokontany (wereda_id, fkt_desc)
VALUES
(3, 'Fokontany de Toamasina Ville'),
(3, 'Fokontany de Mahavoky'),
(4, 'Fokontany de Foulpointe'),
(4, 'Fokontany de Mahatsara'),
(4, 'Fokontany de Ambodiriana');





INSERT INTO myapp_centralrecette (id_contribuable_id,id_centre_recette,regisseur,logiciel_id,ref_trans,ref_reglement,daty,
    mouvement,moyen_paiement,rib,raison_sociale,nimp_id,libelle,flag,date_debut,date_fin,periode,periode2,mnt_ap,base,imp_detail,da,
    banque,annee_recouvrement,code_bureau,libelle_bureau
) VALUES (
    20,                         
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
(20, 1, 1, 'QUIT126', 35000.00, '2027-02-01'),  
(20, 1, 1, 'QUIT126', 15000.00, '2027-03-01');  






INSERT INTO myapp_videopublicite (
    titre, description, video, lien_video, date_publication, duree, categorie, langue, statut, 
    tags, nombre_vues, auteur, miniature, date_modification
)
VALUES
    (
        'Lutter Contre la Corruption', 
        'Connaissez Vos Droits, Protégez-Vous !',
        'videos/1.mp4', 
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
        'Partagez Vos Idées et Préoccupations', 
        'Visitez www.mef.gov.mg pour soumettre vos suggestions.',
        'videos/4.mp4', 
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
        'Comprendre l''IFPB et Son Importance pour Tous', 
        'Impôt Foncier sur les Propriétés Bâties (IFPB)',
        'videos/2.mp4', 
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
        'la DGI (Direction Générale des Impôts)', 
        'Votre Partenaire Fiscal au Service de la Nation',
        'videos/5.mp4', 
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
        'Après l''Obtention de Votre Carte Fiscale', 
        'Les démarches à effectuer pour bien utiliser votre carte fiscale',
        'videos/6.mp4', 
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
    ),
    (
        'Lutter Contre la Corruption', 
        'Connaissez Vos Droits, Protégez-Vous !',
        'videos/0.mp4', 
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


insert into myapp_operateurs(nom,email) values('Operateur 1','raharinirinalina@gmail.com');

insert into myapp_operateur(cin,contact) values ('123123123123','0345319718');

insert into myapp_message('love you',,default,20,1,f);



-- lina04!s