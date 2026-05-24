CREATE TABLE Personne (
    id_personne INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20)
);

CREATE TABLE Utilisateur (
    id_utilisateur INT PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    actif BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_utilisateur) REFERENCES Personne(id_personne) ON DELETE CASCADE
);

CREATE TABLE Administrateur (
    id_administrateur INT PRIMARY KEY,
    niveau_ces INT NOT NULL,
    FOREIGN KEY (id_administrateur) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE
);

CREATE TABLE Enseignant (
    id_enseignant INT PRIMARY KEY,
    grade VARCHAR(50),
    specialite VARCHAR(100),
    FOREIGN KEY (id_enseignant) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE
);

CREATE TABLE Classe (
    id_classe INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    effectif INT DEFAULT 0,
    annee INT NOT NULL
);

CREATE TABLE Etudiant (
    id_etudiant INT PRIMARY KEY,
    NCE VARCHAR(50) UNIQUE NOT NULL,
    id_classe INT NULL,
    FOREIGN KEY (id_etudiant) REFERENCES Utilisateur(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_classe) REFERENCES Classe(id_classe) ON DELETE SET NULL
);
CREATE TABLE Module (
    id_module INT AUTO_INCREMENT PRIMARY KEY,
    intitule VARCHAR(150) NOT NULL,
    id_classe INT NOT NULL,
    FOREIGN KEY (id_classe) REFERENCES Classe(id_classe) ON DELETE CASCADE
);

CREATE TABLE Affectation (
    id_affectation INT AUTO_INCREMENT PRIMARY KEY,
    id_enseignant INT NOT NULL,
    id_classe INT NOT NULL,
    id_module INT NOT NULL,
    est_responsable BOOLEAN DEFAULT FALSE,
    date_debut DATETIME NOT NULL,
    date_fin DATETIME NOT NULL,
    FOREIGN KEY (id_enseignant) REFERENCES Enseignant(id_enseignant) ON DELETE CASCADE,
    FOREIGN KEY (id_classe) REFERENCES Classe(id_classe) ON DELETE CASCADE,
    FOREIGN KEY (id_module) REFERENCES Module(id_module) ON DELETE CASCADE
);

CREATE TABLE Ressource (
    id_ressource INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(150) NOT NULL,
    fichier VARCHAR(255) NOT NULL,
    description TEXT,
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_module INT NOT NULL,
    id_enseignant INT NOT NULL,
    FOREIGN KEY (id_module) REFERENCES Module(id_module) ON DELETE CASCADE,
    FOREIGN KEY (id_enseignant) REFERENCES Enseignant(id_enseignant) ON DELETE CASCADE
);

CREATE TABLE Annonce (
    id_annonce INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(150) NOT NULL,
    contenu TEXT NOT NULL,
    date_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_classe INT NOT NULL,
    id_enseignant INT NOT NULL,
    FOREIGN KEY (id_classe) REFERENCES Classe(id_classe) ON DELETE CASCADE,
    FOREIGN KEY (id_enseignant) REFERENCES Enseignant(id_enseignant) ON DELETE CASCADE
);

CREATE TABLE Notification (
    id_notification INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    lue BOOLEAN DEFAULT FALSE,
    date_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_etudiant INT NOT NULL,
    FOREIGN KEY (id_etudiant) REFERENCES Etudiant(id_etudiant) ON DELETE CASCADE
);

CREATE TABLE Historique (
    id_historique INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    date_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_etudiant INT NOT NULL,
    FOREIGN KEY (id_etudiant) REFERENCES Etudiant(id_etudiant) ON DELETE CASCADE
);
