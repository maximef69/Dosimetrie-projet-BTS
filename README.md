# Dosimetrie-projet-BTS
# ☢️ Projet IoT : Dosimétrie en milieu hospitalier

![Badge MicroPython](https://img.shields.io/badge/MicroPython-ESP32-333333?style=for-the-badge&logo=python)
![Badge MQTT](https://img.shields.io/badge/MQTT-TLS_1.2-660066?style=for-the-badge&logo=mqtt)
![Badge Docker](https://img.shields.io/badge/Docker-Hardened-2496ED?style=for-the-badge&logo=docker)
![Badge Node-RED](https://img.shields.io/badge/Node--RED-Flow-8F0000?style=for-the-badge&logo=node-red)

## Contexte du projet
Ce dépôt présente le lot Matériel et Infrastructure d'un projet de conception d'un **dosimètre opérationnel** pour le bloc opératoire de l'Hôpital Privé Natécia (Lyon). L'objectif est de mesurer l'exposition aux rayonnements ionisants du personnel médical et d'alerter en cas de dépassement des seuils de sécurité, tout en respectant un environnement réseau strictement isolé.

> 👤 **Mon Rôle - (Chef de Projet | Matériel & Réseau)**
> Dans le cadre de ce projet d'équipe, j'ai été responsable de l'acquisition bas niveau des données radioactives, du transport sécurisé des flux (Cybersécurité), et de l'orchestration serveur. Ce dépôt met en valeur mes contributions spécifiques.

---

## 🛠️ Réalisations techniques & compétences

### 1. Ingénierie embarquée (ESP32 & MicroPython)
* **Acquisition zéro perte :** Implémentation d'interruptions matérielles (**IRQ**) sur front descendant pour la détection instantanée des particules captées par le tube Geiger-Müller (Gravity SEN0463).
* **Résilience Réseau :** Gestion autonome des déconnexions Wi-Fi via des blocs `try/except` et routines de reconnexion automatiques.

### 2. Cybersécurité & infrastructure (Docker / MQTT)
* **Durcissement :** Configuration stricte du conteneur Mosquitto via `docker-compose.yml` entraînant la fermeture du port MQTT standard (1883) et l'exposition exclusive du port sécurisé **MQTTS (8883)**.
* **Chiffrement des Flux :** Mise en place d'un tunnel cryptographique TLS 1.2 pour garantir la confidentialité des données médicales transmises par le microcontrôleur.
* **Réseau cloisonné :** Déploiement d'un routeur TP-Link dédié pour isoler l'infrastructure IoT du réseau informatique de l'hôpital.

### 3. Orchestration middleware (Node-RED)
* **Conversion data :** Développement de fonctions JavaScript pour convertir les données physiques brutes (Coups Par Minute - CPM) en unité légale de radioprotection (µSv/h) via le facteur d'étalonnage (153.8).
* **Formatage API :** Génération de trames JSON standardisées et interconnexion logicielle via requêtes `HTTP POST`.
* **Supervision :** Création d'un Dashboard dynamique pour la visualisation en temps réel de la dose absorbée.

---

## 📂 Architecture du Dépôt

```text
📦 Projet_Dosimetrie_Natecia
 ┣ 📂 hardware/
 ┃ ┗ 📜 main.py                # Script MicroPython ESP32
 ┣ 📂 docker/
 ┃ ┗ 📜 docker-compose.yml     # Configuration sécurisée Mosquitto & Node-RED
 ┗ 📜 README.md
