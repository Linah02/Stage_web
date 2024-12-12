    CREATE OR REPLACE VIEW v_getFokontany AS
    SELECT 
        f.id as fkt_no, 
        f.FKT_DESC, 
        w.id as wereda_no, 
        w.wereda_desc, 
        w.wereda_code, 
        l.id as locality_no, 
        l.locality_desc, 
        l.locality_desc_f, 
        l.locality_desc_s, 
        l.locality_code, 
        ct.id as city_no, 
        ct.city_name, 
        ct.city_name_f, 
        ct.city_name_s, 
        ct.city_code, 
        ct.city_name_extra, 
        p.id as parish_no, 
        p.parish_name, 
        p.parish_name_f, 
        p.parish_name_s, 
        p.parish_code, 
        cn.id as country_no, 
        cn.country_name, 
        cn.country_name_f, 
        cn.country_name_s, 
        cn.country_code, 
        cn.capital
    FROM 
        myapp_fokontany f
    JOIN 
        myapp_wereda w ON f.wereda_id = w.id
    JOIN 
        myapp_locality l ON w.locality_id = l.id
    JOIN 
        myapp_city ct ON l.city_id = ct.id
    JOIN 
        myapp_parish p ON ct.parish_id = p.id
    JOIN 
        myapp_country cn ON p.country_id = cn.id;


-- vue select all transaction group by quit 
-- (total_payee =somme mnt_ver,reste_ap=mnt_ap-total_payee),
-- n_quit,ANNEE,date_debt et fin,NIMP,imp_detail
--filtre montant

CREATE VIEW vue_transactions_par_quit_et_contribuable AS
SELECT
    c.id_contribuable_id AS contribuable,
    c.code_bureau,
    c.libelle_bureau,
    c.imp_detail,
    ni.numero,
    ni.impot,
    l.logiciel,
    p.n_quit,
    c.mnt_ap as mont_ap,
    SUM(p.montant) AS total_payee,
    c.mnt_ap - SUM(p.montant) AS reste_ap
FROM
    myapp_centralrecette c
JOIN
    myapp_paiement p ON c.id = p.central_recette_id
    join 
    myapp_NUMIMPOT ni on c.nimp_id= ni.id 
join 
    myapp_MODEPAIEMENT mp on mp.id =p.MODE_PAIEMENT_id
join 
    myapp_logiciel l on l.id = c.logiciel_id
GROUP BY
    c.id_contribuable_id,p.n_quit,c.mnt_ap, c.code_bureau,
    c.libelle_bureau,
    c.imp_detail,
    ni.numero,
    ni.impot,
    l.logiciel,
    p.n_quit
ORDER BY
    contribuable, p.n_quit;



-- filtre date date et montant
CREATE VIEW vue_detail_transactions_par_quit_et_contribuable AS
SELECT
    c.id_contribuable_id AS contribuable,
    p.n_quit,
    p.date_paiement,
    p.NUMREC,
    EXTRACT(YEAR FROM p.date_paiement) AS annee_de_paiement,
    c.annee_recouvrement,
    MIN(c.date_debut) AS date_debut,
    MAX(c.date_fin) AS date_fin,
    c.base,
    c.mnt_ap,
    c.nimp_id AS NIMP,
    c.imp_detail,
    ni.numero,
    ni.impot,
    mp.sens,
    l.logiciel,
    p.montant
FROM
    myapp_centralrecette c
JOIN
    myapp_paiement p ON c.id = p.central_recette_id
join 
    myapp_NUMIMPOT ni on c.nimp_id= ni.id 
join 
    myapp_MODEPAIEMENT mp on mp.id =p.MODE_PAIEMENT_id
join 
    myapp_logiciel l on l.id = c.logiciel_id
GROUP BY
    c.id_contribuable_id, p.n_quit, p.NUMREC,p.date_paiement, c.annee_recouvrement,c.base,c.mnt_ap, c.nimp_id, c.imp_detail, ni.numero,
    ni.impot,
    mp.sens,
    l.logiciel,p.montant
ORDER BY
    contribuable, n_quit;



-- liste centre fiscal ->detail paiement

-- chart 2
CREATE VIEW vue_recouvrements_et_paiements_par_annee AS
SELECT 
    c.id_contribuable_id AS contribuable,
    c.annee_recouvrement,
    SUM(c.mnt_ap) / NULLIF(COUNT(p.montant), 0) AS total_recouvrement_annuel,
    COALESCE(SUM(p.montant), 0) AS total_paye_annuel
FROM 
    myapp_centralrecette c
LEFT JOIN 
    myapp_paiement p ON c.id = p.central_recette_id
GROUP BY 
    c.id_contribuable_id, c.annee_recouvrement
ORDER BY 
    contribuable, c.annee_recouvrement;


-- vue: somme par ans(taona) par contribuable somme  mnt_ver par contribuable

CREATE VIEW vue_somme_par_contribuable_par_annee AS
SELECT
    c.id_contribuable_id AS contribuable,
    EXTRACT(YEAR FROM p.date_paiement) AS annee,
    SUM(p.montant) AS total_mnt_ver
FROM
    myapp_centralrecette c
JOIN
    myapp_paiement p ON c.id = p.central_recette_id
GROUP BY
    c.id_contribuable_id, EXTRACT(YEAR FROM p.date_paiement)
ORDER BY
    contribuable, annee;




SELECT table_name
FROM information_schema.views
WHERE table_schema = 'public';  -- Vous pouvez spécifier un autre schéma si nécessaire