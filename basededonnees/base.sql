-- UniShare — base de données PostgreSQL
-- Généré pour correspondre exactement aux modèles Django (utilisateurs/models.py)
-- Ne pas utiliser pour créer la base à la place des migrations Django.
-- Utiliser uniquement comme documentation ou pour inspection.

CREATE DATABASE uni_share;

-- Extension recommandée pour PostgreSQL
-- \c uni_share

-- Table principale des utilisateurs (correspond à Utilisateur extends AbstractUser)
-- Django crée aussi les colonnes héritées de AbstractUser :
-- password, last_login, is_superuser, username, first_name, last_name,
-- is_staff, is_active, date_joined — elles ne sont pas répétées ici
CREATE TABLE utilisateurs_utilisateur (
    id           SERIAL PRIMARY KEY,
    email        VARCHAR(254) UNIQUE NOT NULL,
    nom          VARCHAR(100) NOT NULL,
    prenom       VARCHAR(100) NOT NULL,
    telephone    VARCHAR(20),
    role         VARCHAR(20) NOT NULL DEFAULT 'ETUDIANT',
    -- Colonnes AbstractUser (gérées par Django)
    password     VARCHAR(128) NOT NULL,
    username     VARCHAR(150) UNIQUE NOT NULL,
    is_staff     BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login   TIMESTAMP,
    CONSTRAINT check_role CHECK (role IN ('ADMIN', 'ENSEIGNANT', 'RESPONSABLE', 'ETUDIANT'))
);

CREATE TABLE utilisateurs_administrateur (
    utilisateur_id INT PRIMARY KEY,
    CONSTRAINT fk_admin_utilisateur
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateurs_utilisateur(id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_enseignant (
    utilisateur_id INT PRIMARY KEY,
    grade          VARCHAR(50),
    specialite     VARCHAR(100),
    CONSTRAINT fk_enseignant_utilisateur
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateurs_utilisateur(id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_classe (
    id       SERIAL PRIMARY KEY,
    nom      VARCHAR(50) NOT NULL,
    effectif INT NOT NULL DEFAULT 0,
    annee    INT NOT NULL
);

CREATE TABLE utilisateurs_etudiant (
    utilisateur_id INT PRIMARY KEY,
    NCE            VARCHAR(50) UNIQUE NOT NULL,
    classe_id      INT,
    CONSTRAINT fk_etudiant_utilisateur
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateurs_utilisateur(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_etudiant_classe
        FOREIGN KEY (classe_id)
        REFERENCES utilisateurs_classe(id)
        ON DELETE SET NULL
);

CREATE TABLE utilisateurs_module (
    id        SERIAL PRIMARY KEY,
    intitule  VARCHAR(150) NOT NULL,
    classe_id INT NOT NULL,
    CONSTRAINT fk_module_classe
        FOREIGN KEY (classe_id)
        REFERENCES utilisateurs_classe(id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_affectation (
    id              SERIAL PRIMARY KEY,
    enseignant_id   INT NOT NULL,
    classe_id       INT NOT NULL,
    module_id       INT NOT NULL,
    est_responsable BOOLEAN NOT NULL DEFAULT FALSE,
    date_debut      TIMESTAMP NOT NULL,
    date_fin        TIMESTAMP NOT NULL,
    CONSTRAINT fk_affectation_enseignant
        FOREIGN KEY (enseignant_id)
        REFERENCES utilisateurs_enseignant(utilisateur_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_affectation_classe
        FOREIGN KEY (classe_id)
        REFERENCES utilisateurs_classe(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_affectation_module
        FOREIGN KEY (module_id)
        REFERENCES utilisateurs_module(id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_ressource (
    id            SERIAL PRIMARY KEY,
    titre         VARCHAR(150) NOT NULL,
    fichier       VARCHAR(100) NOT NULL,
    description   TEXT,
    date_ajout    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    module_id     INT NOT NULL,
    enseignant_id INT NOT NULL,
    CONSTRAINT fk_ressource_module
        FOREIGN KEY (module_id)
        REFERENCES utilisateurs_module(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ressource_enseignant
        FOREIGN KEY (enseignant_id)
        REFERENCES utilisateurs_enseignant(utilisateur_id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_annonce (
    id            SERIAL PRIMARY KEY,
    titre         VARCHAR(150) NOT NULL,
    contenu       TEXT NOT NULL,
    date_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    classe_id     INT NOT NULL,
    enseignant_id INT NOT NULL,
    CONSTRAINT fk_annonce_classe
        FOREIGN KEY (classe_id)
        REFERENCES utilisateurs_classe(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_annonce_enseignant
        FOREIGN KEY (enseignant_id)
        REFERENCES utilisateurs_enseignant(utilisateur_id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_notification (
    id            SERIAL PRIMARY KEY,
    titre         VARCHAR(150) NOT NULL,
    message       TEXT NOT NULL,
    lue           BOOLEAN NOT NULL DEFAULT FALSE,
    date_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    etudiant_id   INT NOT NULL,
    CONSTRAINT fk_notification_etudiant
        FOREIGN KEY (etudiant_id)
        REFERENCES utilisateurs_etudiant(utilisateur_id)
        ON DELETE CASCADE
);

CREATE TABLE utilisateurs_historique (
    id            SERIAL PRIMARY KEY,
    action        VARCHAR(50) NOT NULL,
    date_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    etudiant_id   INT NOT NULL,
    ressource_id  INT NOT NULL,
    CONSTRAINT check_action CHECK (action IN ('telechargement', 'consultation')),
    CONSTRAINT fk_historique_etudiant
        FOREIGN KEY (etudiant_id)
        REFERENCES utilisateurs_etudiant(utilisateur_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_historique_ressource
        FOREIGN KEY (ressource_id)
        REFERENCES utilisateurs_ressource(id)
        ON DELETE CASCADE
);