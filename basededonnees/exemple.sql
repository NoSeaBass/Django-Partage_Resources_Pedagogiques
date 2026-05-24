INSERT INTO Personne (nom, prenom, telephone) VALUES
('Diop', 'Ibrahima', '+221771234567'),
('Ndiaye', 'Awa', '+221789876543'),
('Sane', 'Moussa', '+221701112233'),
('Cisse', 'Fatou', '+221765554433'),
('Fall', 'Amadou', '+221774443322');

INSERT INTO Utilisateur (id_utilisateur, email, mot_de_passe, actif) VALUES
(1, 'admin@unishare.sn', 'pbkdf2_sha256$password_hash_admin', TRUE),
(2, 'awa.ndiaye@unishare.sn', 'pbkdf2_sha256$password_hash_awa', TRUE),
(3, 'moussa.sane@unishare.sn', 'pbkdf2_sha256$password_hash_moussa', TRUE),
(4, 'fatou.cisse@unishare.sn', 'pbkdf2_sha256$password_hash_fatou', TRUE),
(5, 'amadou.fall@unishare.sn', 'pbkdf2_sha256$password_hash_amadou', TRUE);

INSERT INTO Administrateur (id_administrateur, niveau_ces) VALUES
(1, 3);

INSERT INTO Enseignant (id_enseignant, grade, specialite) VALUES
(2, 'Professeur Titulaire', 'Génie Logiciel'),
(3, 'Maître de Conférences', 'Réseaux et Systèmes');

INSERT INTO Classe (nom, effectif, annee) VALUES
('Licence 3 Informatique', 2, 2026);

INSERT INTO Etudiant (id_etudiant, NCE, id_classe) VALUES
(4, 'ETU20260001', 1),
(5, 'ETU20260002', 1);

INSERT INTO Module (intitule, id_classe) VALUES
('Développement Web Django', 1),
('Administration Réseaux', 1);

INSERT INTO Affectation (id_enseignant, id_classe, id_module, est_responsable, date_debut, date_fin) VALUES
(2, 1, 1, TRUE, '2026-01-05 08:00:00', '2026-06-30 18:00:00'),
(3, 1, 2, FALSE, '2026-01-05 08:00:00', '2026-06-30 18:00:00');

INSERT INTO Ressource (titre, fichier, description, id_module, id_enseignant) VALUES
('Support de Cours - Modèles Django', 'ressources/cours_models_django.pdf', 'Introduction aux ORM et relations SQL avec Django.', 1, 2),
('TP 1 - Configuration Réseau', 'ressources/tp1_reseau.pdf', 'Exercices pratiques sur l''adressage IP.', 2, 3);

INSERT INTO Annonce (titre, contenu, id_classe, id_enseignant) VALUES
('Report du cours de Django', 'Le cours prévu ce mercredi est reporté au vendredi à 14h en salle IP3.', 1, 2);

INSERT INTO Notification (titre, message, lue, id_etudiant) VALUES
('Nouvelle ressource disponible', 'Le Pr. Awa Ndiaye a ajouté : Support de Cours - Modèles Django.', FALSE, 4),
('Nouvelle Annonce', 'Un message concernant le report de cours a été publié.', FALSE, 4);

INSERT INTO Historique (action, id_etudiant) VALUES
('consultation', 5),
('telechargement', 5);
