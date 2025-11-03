🚗 Projet IoT – Voiture Miniature Autonome & Télécommandée
🧩 Description du projet

Ce projet IoT a pour but de concevoir et programmer une voiture miniature connectée capable :

de réaliser un parcours autonome prédéfini ;

et d’être contrôlée à distance via une manette sans fil connectée en Wi-Fi.

L’ensemble du système repose sur deux microcontrôleurs ESP32 :

l’un embarqué dans la voiture (serveur) ;

l’autre dans la manette (client).

⚙️ Fonctionnalités principales

🕹️ Contrôle manuel via Wi-Fi (avancer, reculer, gauche, droite, stop)

🤖 Parcours automatique préprogrammé

📡 Communication HTTP entre manette et voiture

🚧 Détection d’obstacle avec capteur à ultrasons

⚡ Gestion de la vitesse et des virages via PWM

🧠 Architecture du système
┌──────────────────────────┐        ┌──────────────────────────┐
│        Manette ESP32     │  <–––> │        Voiture ESP32     │
│ - Boutons directionnels  │        │ - Moteurs DC             │
│ - Connexion WiFi client  │        │ - Serveur HTTP           │
│ - Envoi de requêtes HTTP │        │ - Capteur ultrason       │
└──────────────────────────┘        └──────────────────────────┘

📁 Structure du projet
.
├── Voiture.py           → Script de la voiture (parcours automatique)
├── voiture_manette.py   → Script voiture + serveur Wi-Fi pour contrôle manuel
└── manette.py           → Script de la manette (client Wi-Fi)

🔧 Détails des scripts
🛞 Voiture.py

Gère les moteurs (IN1–IN4, ENA, ENB) via PWM.

Implémente un parcours automatique composé de séquences d’avancée et de virages.

Utilise un capteur ultrason pour détecter les obstacles.

Peut être exécuté seul pour faire tourner la voiture sur un circuit.

📡 voiture_manette.py

Configure l’ESP32 en Point d’Accès Wi-Fi (SSID: RobotVoiture, password: 12345678).

Héberge un serveur HTTP qui reçoit les commandes de la manette.

Contrôle les moteurs selon la commande reçue.

Intègre la détection d’obstacles en temps réel : la voiture s’arrête automatiquement si un objet est trop proche.

🎮 manette.py

Configure l’ESP32 en mode client Wi-Fi et se connecte au réseau de la voiture.

Lit l’état des boutons physiques (GPIO).

Envoie des requêtes HTTP à la voiture (ex. http://192.168.4.1/avancer).

Permet un contrôle en temps réel du véhicule.

🧰 Matériel requis

2x ESP32

1x Châssis de voiture (avec 2 moteurs DC et roues)

1x Module L298N (ou équivalent) pour piloter les moteurs

1x Capteur ultrason HC-SR04

4x Boutons poussoirs (pour la manette)

Fils, alimentation et breadboard

🚀 Mise en route

Flasher les scripts :

voiture_manette.py sur la voiture (ESP32 côté robot)

manette.py sur la manette (ESP32 côté télécommande)

Alimenter les deux modules ESP32.

La voiture crée automatiquement un réseau Wi-Fi nommé RobotVoiture.
La manette s’y connecte et envoie les commandes.

Appuyez sur les boutons pour contrôler la voiture :

⬆️ Avancer

⬇️ Reculer

⬅️ Tourner à gauche

➡️ Tourner à droite

🛑 Relâcher = Stop

Pour le mode automatique, flashez Voiture.py sur l’ESP32 de la voiture.

⚠️ Sécurité et calibration

Veillez à calibrer les vitesses et durées des virages pour votre châssis.

Ne pas dépasser les tensions nominales des moteurs.

Utilisez un espace dégagé pour tester le parcours.

🧾 Auteurs

Projet réalisé dans le cadre d’un projet IoT / robotique embarquée.
Équipe : (à compléter)
Année : 2025
