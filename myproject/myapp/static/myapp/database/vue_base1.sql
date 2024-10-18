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


