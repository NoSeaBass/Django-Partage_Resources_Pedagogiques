-- Connexion à la base de données Django
\c uni_share;

-- Nettoyage des anciennes insertions pour éviter les conflits de clés uniques
TRUNCATE utilisateurs_utilisateur CASCADE;
TRUNCATE administrateur_classe CASCADE;

-- 1. Insertion dans l'Utilisateur de base (Données d'authentification + Profil)
INSERT INTO utilisateurs_utilisateur (id, username, password, is_superuser, is_staff, is_active, date_joined, email, nom, prenom, telephone, first_name, last_name) OVERRIDING SYSTEM VALUE VALUES
(1, 'admin', 'pbkdf2_sha256$password_hash_admin', TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, 'admin@unishare.sn', 'Diop', 'Ibrahima', '+221771234567', 'Ibrahima', 'Diop'),
(2, 'awa', 'pbkdf2_sha256$password_hash_awa', FALSE, FALSE, TRUE, CURRENT_TIMESTAMP, 'awa.ndiaye@unishare.sn', 'Ndiaye', 'Awa', '+221789876543', 'Awa', 'Ndiaye'),
(3, 'moussa', 'pbkdf2_sha256$password_hash_moussa', FALSE, FALSE, TRUE, CURRENT_TIMESTAMP, 'moussa.sane@unishare.sn', 'Sane', 'Moussa', '+221701112233', 'Moussa', 'Sane'),
(4, 'fatou', 'pbkdf2_sha256$password_hash_fatou', FALSE, FALSE, TRUE, CURRENT_TIMESTAMP, 'fatou.cisse@unishare.sn', 'Cisse', 'Fatou', '+221765554433', 'Fatou', 'Cisse'),
(5, 'amadou', 'pbkdf2_sha256$password_hash_amadou', FALSE, FALSE, TRUE, CURRENT_TIMESTAMP, 'amadou.fall@unishare.sn', 'Fall', 'Amadou', '+221774443322', 'Amadou', 'Fall');

-- 2. Insertion dans Administrateur (Liaison via utilisateur_id)
INSERT INTO administrateur_administrateur (utilisateur_id, niveau_ces) VALUES
(1, 3);

-- 3. Insertion dans Enseignant (Liaison via utilisateur_id vérifiée)
INSERT INTO utilisateurs_enseignant (utilisateur_id, grade, specialite) VALUES
(2, 'Professeur Titulaire', 'Génie Logiciel'),
(3, 'Maître de Conférences', 'Réseaux et Systèmes');

-- 4. Insertion dans Classe
INSERT INTO administrateur_classe (id, nom, effectif, annee) OVERRIDING SYSTEM VALUE VALUES
(1, 'Licence 3 Informatique', 2, 2026);

-- 5. Insertion dans Etudiant (Liaison via utilisateur_id et "NCE" avec guillemets doubles)
INSERT INTO utilisateurs_etudiant (utilisateur_id, "NCE", classe_id) VALUES
(4, 'ETU20260001', 1),
(5, 'ETU20260002', 1);

-- 6. Insertion dans Module (Liaison via classe_id)
INSERT INTO administrateur_module (id, intitule, classe_id) OVERRIDING SYSTEM VALUE VALUES
(1, 'Développement Web Django', 1),
(2, 'Administration Réseaux', 1);

-- 7. Insertion dans Affectation (Liaison via enseignant_id, classe_id, module_id)
INSERT INTO administrateur_affectation (id, est_responsable, date_debut, date_fin, classe_id, enseignant_id, module_id) OVERRIDING SYSTEM VALUE VALUES
(1, TRUE, '2026-01-05 08:00:00', '2026-06-30 18:00:00', 1, 2, 1),
(2, FALSE, '2026-01-05 08:00:00', '2026-06-30 18:00:00', 1, 3, 2);

-- Synchronisation finale des compteurs d'auto-incrémentation PostgreSQL
SELECT setval(pg_get_serial_sequence('"utilisateurs_utilisateur"', 'id'), COALESCE(max(id), 1)) FROM utilisateurs_utilisateur;
SELECT setval(pg_get_serial_sequence('"administrateur_classe"', 'id'), COALESCE(max(id), 1)) FROM administrateur_classe;
SELECT setval(pg_get_serial_sequence('"administrateur_module"', 'id'), COALESCE(max(id), 1)) FROM administrateur_module;
SELECT setval(pg_get_serial_sequence('"administrateur_affectation"', 'id'), COALESCE(max(id), 1)) FROM administrateur_affectation;
