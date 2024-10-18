-- Table demandes
CREATE TABLE CONTRIBUABLE();

CREATE TABLE DEMANDES(
    ID_DEMANDE SERIAL PRIMARY KEY, -- Gestion de la clé primaire avec SERIAL
    RJT_CODE INTEGER, -- Code de motif de rejet, se réfère à la table MOTIF_REJET
    FISCAL_REGIME_NO INTEGER, -- Numéro de régime fiscal, se réfère à la table FISCAL_REGIME
    JURIDICAL_FORM_NO INTEGER, -- Numéro de forme juridique, se réfère à la table JURIDICAL_FORM
    WEREDA_NO INTEGER, -- Numéro de wereda, se réfère à la table WEREDA
    DM_DATEDEMANDE DATE, -- Date de la demande
    DM_STADE INTEGER, -- Stade actuel de la demande
    DM_DATEVALIDATION DATE, -- Date de validation de la demande
    DM_MOTIF_REJET VARCHAR(200), -- Motif du rejet de la demande
    DM_RAISONSOCIALE VARCHAR(100), -- Raison sociale de l'entreprise
    DM_CIN VARCHAR(15), -- Numéro de carte d'identité nationale (CIN)
    DM_RESIDENT INTEGER, -- Indique si le demandeur est résident (1 pour oui, 0 pour non)
    CAP_SOCIETE NUMERIC, -- Capital social de l'entreprise
    COM_REG_NO VARCHAR(20), -- Numéro d'enregistrement commercial
    DM_REF VARCHAR(15), -- Référence de la demande
    ID_VALID_USER INTEGER, -- Identifiant de l'utilisateur ayant validé la demande, se réfère à la table USERS_NIF
    MAILING_ADDRESS VARCHAR(200), -- Adresse postale
    ACTIVITY VARCHAR(800), -- Activité principale de l'entreprise
    AGREE_DATE DATE, -- Date d'acceptation de la demande
    BANK_ACCT_NO VARCHAR(250), -- Numéro de compte bancaire de l'entreprise
    NOM_COMMERCIAL VARCHAR(200), -- Nom commercial de l'entreprise
    ACRONYME VARCHAR(40), -- Acronyme de l'entreprise
    CF_VALID INTEGER, -- Identifiant du centre fiscal validant, se réfère à la table CENTRE_FISCAL
    CF_MANAGE VARCHAR(9), -- Identifiant du centre gestionnaire, se réfère à la table CENTRE_GESTIONNAIRE
    AUTH_PUBLIE INTEGER, -- Indicateur si l'autorisation est publiée (1 pour oui, 0 pour non)
    OLD_NIF VARCHAR(50), -- Ancien numéro d'identification fiscale (NIF)
    BIRTH_DATE DATE, -- Date de naissance du demandeur
    BIRTH_PLACE VARCHAR(120), -- Lieu de naissance du demandeur
    DELIVR_CIN_DATE DATE, -- Date de délivrance de la carte d'identité nationale (CIN)
    CIN_PLACE VARCHAR(120), -- Lieu de délivrance de la carte d'identité nationale (CIN)
    CREATE_DATE DATE, -- Date de création de la demande
    ENT_TYPE_NO INTEGER, -- Type d'treprise, se réfère à la table ENT_TYPE
    SEX INTEGER, -- Sexe du demandeur (1 pour homme, 2 pour femme)
    REG_DATE DATE, -- Date d'enregistrement
    PIECES VARCHAR(20), -- Pièces justificatives fournies
    IMPORTER INTEGER, -- Indique si le demandeur est un importateur (1 pour oui, 0 pour non)
    EXPORTER INTEGER, -- Indique si le demandeur est un exportateur (1 pour oui, 0 pour non)
    SIT_MATRIM INTEGER, -- Situation matrimoniale (1 pour célibataire, 2 pour marié, etc.)
    PROPRIETAIRE BOOLEAN, -- Indique si le demandeur est propriétaire (TRUE pour oui, FALSE pour non)
    PROPR_TYPE VARCHAR(20), -- Type de propriété (par exemple, individuel, société, etc.)
    PROPR_NIF VARCHAR(10), -- Numéro d'identification fiscale du propriétaire
    PROPR_NAME VARCHAR(100), -- Nom du propriétaire
    PROPR_CIN VARCHAR(15), -- CIN du propriétaire
    PROPR_ADDRESS VARCHAR(200), -- Adresse du propriétaire
    STATISTIC_NO VARCHAR(21), -- Numéro statistique
    STATISTIC_DATE DATE, -- Date d'enregistrement statistique
    DEBUT_EXO VARCHAR(5), -- Date de début d'exercice
    FIN_EXO VARCHAR(5), -- Date de fin d'exercice
    INTERLOCUTOR_NAME VARCHAR(100), -- Nom de l'interlocuteur
    INTERLOCUTOR_TITLE VARCHAR(100), -- Titre de l'interlocuteur
    INTERLOCUTOR_ADDRESS VARCHAR(200), -- Adresse de l'interlocuteur
    INTERLOCUTOR_PHONE VARCHAR(14), -- Téléphone de l'interlocuteur
    INTERLOCUTOR_EMAIL VARCHAR(100), -- Email de l'interlocuteur
    ASSOCIATE_MAJORITY BOOLEAN, -- Indique si le demandeur a une majorité d'associés (TRUE pour oui, FALSE pour non)
    COMPANY_NIF VARCHAR(100), -- Numéro d'identification fiscale de l'entreprise
    NBR_EMPLOYE INTEGER, -- Nombre d'employés de l'entreprise
    PROPR_CONTACT VARCHAR(14), -- Contact du propriétaire
    DETAILS_ACTIVITY VARCHAR(500), -- Détails sur l'activité de l'entreprise
    PASSEPORT VARCHAR(20), -- Numéro de passeport du demandeur
    PERIODE_GRACE INTEGER, -- Période de grâce en jours
    FKT_NO INTEGER, -- Numéro de fokontany, se réfère à la table FOKONTANY
    DURE_EXO INTEGER -- Durée de l'exercice en mois
);

create table




