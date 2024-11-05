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

INSERT INTO myapp_centralrecette (
    id_contribuable_id,
    id_centre_recette,
    regisseur,
    logiciel_id,
    ref_trans,
    ref_reglement,
    daty,
    mouvement,
    moyen_paiement,
    rib,
    raison_sociale,
    nimp_id,
    numrec,
    libelle,
    flag,
    date_debut,
    date_fin,
    periode,
    periode2,
    mnt_ap,
    base,
    imp_detail,
    da,
    banque,
    annee_recouvrement,
    code_bureau,
    libelle_bureau
) VALUES (
    6,                         -- id_contribuable_id
    'NIF123QUITCENTRE',        -- id_centre_recette
    'Regisseur 1',             -- regisseur
    1,                         -- logiciel_id
    'TRANS123',                -- ref_trans
    'REG123',                  -- ref_reglement
    '2024-01-01',              -- daty
    '1',                       -- mouvement
    '01',                      -- moyen_paiement
    'RIB123456789',            -- rib
    'Raison Sociale 1',        -- raison_sociale
    1,                         -- nimp_id
    100,                       -- numrec
    'Libelle 1',               -- libelle
    'Y',                       -- flag
    '2024-01-01',              -- date_debut
    '2024-12-31',              -- date_fin
    1,                         -- periode
    '01-2024',                 -- periode2
    50000.00,                  -- mnt_ap
    100000.00,                 -- base
    'Taxation d''office',     -- imp_detail
    1,                         -- da
    'Banque 1',                -- banque
    2024,                      -- annee_recouvrement
    'Code Bureau 123',         -- code_bureau
    'Centre Fiscal 1'          -- libelle_bureau
);



INSERT INTO myapp_centralrecette (
    id_contribuable_id,
    id_centre_recette,
    regisseur,
    logiciel_id,
    ref_trans,
    ref_reglement,
    daty,
    mouvement,
    moyen_paiement,
    rib,
    raison_sociale,
    nimp_id,
    numrec,
    libelle,
    flag,
    date_debut,
    date_fin,
    periode,
    periode2,
    mnt_ap,
    base,
    imp_detail,
    da,
    banque,
    annee_recouvrement,
    code_bureau,
    libelle_bureau
) VALUES (
    6,                         -- id_contribuable_id
    'NIF123QUITCENTRE',        -- id_centre_recette
    'Regisseur 1',             -- regisseur
    1,                         -- logiciel_id
    'TRANS123',                -- ref_trans
    'REG123',                  -- ref_reglement
    '2024-01-01',              -- daty
    '1',                       -- mouvement
    '01',                      -- moyen_paiement
    'RIB123456789',            -- rib
    'Raison Sociale 1',        -- raison_sociale
    1,                         -- nimp_id
    100,                       -- numrec
    'Libelle 1',               -- libelle
    'Y',                       -- flag
    '2024-01-01',              -- date_debut
    '2024-12-31',              -- date_fin
    1,                         -- periode
    '01-2024',                 -- periode2
    90000.00,                  -- mnt_ap
    100000.00,                 -- base
    'Taxation d''office',     -- imp_detail
    1,                         -- da
    'Banque 1',                -- banque
    2027,                      -- annee_recouvrement
    'Code Bureau 123',         -- code_bureau
    'Centre Fiscal 1'          -- libelle_bureau
);


INSERT INTO myapp_paiement (
    id_contribuable_id,
    central_recette_id,
    mode_paiement_id,
    n_quit,
    montant,
    date_paiement
) VALUES
(6, 5, 1, 'QUIT126', 50000.00, '2027-02-01'),  -- Paiement 1
(6, 5, 1, 'QUIT126', 15000.00, '2027-03-01');  -- Paiement 2
