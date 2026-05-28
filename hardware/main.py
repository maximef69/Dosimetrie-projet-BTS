# ============================================================
# CARTOUCHE DU FICHIER
# ============================================================
# Fichier       : main.py
# Emplacement   : ESP32 (racine du système de fichiers MicroPython)
# Date création : 20/03/2026
# Auteur        : Maxime
# Description   : Script MicroPython embarqué sur le micro-
#                 contrôleur ESP32 de chaque dosimètre.
#                 Il réalise trois missions :
#                   1. Compter les impulsions du capteur Geiger
#                      via une interruption matérielle sur la
#                      broche GPIO 4.
#                   2. Se connecter au réseau Wi-Fi dédié du
#                      système dosimétrique.
#                   3. Publier toutes les 10 secondes la valeur
#                      convertie en CPM (coups par minute) sur
#                      le broker MQTT de la Raspberry Pi via
#                      une connexion sécurisée SSL (port 8883).
# ============================================================

from machine import Pin          
from umqtt.simple import MQTTClient
import network                   
import time                      
import sys                       

# ============================================================
# SECTION : CONFIGURATION
# ============================================================
WIFI_SSID     = 'dosimetre_natecia'   
WIFI_PASSWORD = 'admin123'            
MQTT_BROKER   = '192.168.1.101'       
CLIENT_ID     = 'dosimetre_01'        
TOPIC         = '/natecia/dosimetre_01/brut'  
# PORT_MQTT   = 1883                  
PORT_MQTT     = 8883                  

# ============================================================
# SECTION : INITIALISATION MATÉRIELLE
# ============================================================

# Broche GPIO 4 configurée en entrée numérique.
broche_signal = Pin(4, Pin.IN)

# Variable globale incrémentée par l'interruption matérielle.
compteur_impulsions = 0

def compter_clic(pin):
    global compteur_impulsions   # On déclare global pour modifier la variable externe
    compteur_impulsions += 1     # On incrémente à chaque impulsion détectée


broche_signal.irq(trigger=Pin.IRQ_FALLING, handler=compter_clic)

# ============================================================
# SECTION : CONNEXION WI-FI
# ============================================================
wlan = network.WLAN(network.STA_IF)  # Mode STA : l'ESP32 se connecte à un routeur
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connexion WiFi...")
# Boucle bloquante : on attend 1 seconde entre chaque vérification
# jusqu'à ce que la connexion soit établie.
while not wlan.isconnected():
    time.sleep(1)
print("WiFi OK")

# ============================================================
# SECTION : CONNEXION MQTT ET BOUCLE PRINCIPALE
# ============================================================
try:
    print("Tentative de connexion MQTT")
    
    # Instanciation du client MQTT avec chiffrement SSL activé.
    # keepalive=60 : le broker considère le client déconnecté
    client = MQTTClient(
        CLIENT_ID,
        MQTT_BROKER,
        port=PORT_MQTT,
        keepalive=60,
        ssl=True,
        ssl_params={"server_hostname": MQTT_BROKER},
    )
    
    # Connexion effective au broker MQTT de la Raspberry Pi
    client.connect()
    print("Connecté en MQTT au Broker Raspberry !")

    while True:
        # On capture le compteur AVANT la pause de 10 secondes
        # pour éviter de perdre des impulsions survenues pendant
        # la conversion ou la publication.
        valeur_mesuree = compteur_impulsions
        compteur_impulsions = 0   # Remise à zéro pour la prochaine fenêtre

        # Fenêtre de mesure de 10 secondes.
        # Pendant ce temps, les interruptions continuent de
        # s'accumuler dans compteur_impulsions en arrière-plan.
        time.sleep(10)

        cpm = valeur_mesuree * 6

        try:
            client.publish(TOPIC, str(cpm))
            print("Envoyé :", cpm, "CPM")
        except Exception as e:
            print("Erreur lors de l'envoi :", e)
            client.connect()

except Exception as e:
    # Erreur fatale lors de la connexion initiale MQTT ou Wi-Fi.
    print("Erreur de connexion fatale :", e)

except KeyboardInterrupt:
    print("\nArrêt manuel du programme.")

finally:
    try:
        client.disconnect()
    except:
        pass                 # Si client n'existe pas encore, on ignore
    wlan.active(False)       # Désactivation de l'interface Wi-Fi
    print("Système arrêté.")
    sys.exit()
