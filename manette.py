from machine import Pin
import network
import urequests
import time

# Configuration WiFi - Mode client
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Paramètres WiFi
SSID = 'RobotVoiture'
PASSWORD = '12345678'
ROBOT_IP = '192.168.4.1'  # L'adresse IP de la voiture

# Configuration des boutons
BOUTON_AVANCER = Pin(14, Pin.IN, Pin.PULL_UP)  # Utilisez les broches correspondant à votre montage
BOUTON_RECULER = Pin(27, Pin.IN, Pin.PULL_UP)
BOUTON_GAUCHE = Pin(26, Pin.IN, Pin.PULL_UP)
BOUTON_DROITE = Pin(25        , Pin.IN, Pin.PULL_UP)

# Dictionnaire pour suivre l'état des boutons
etat_boutons = {
    'avancer': True,
    'reculer': True,
    'gauche': True,
    'droite': True
}

derniere_commande = 'stop'

def connecter_wifi():
    """Se connecte au réseau WiFi de la voiture"""
    print("Connexion au WiFi...")
    wifi.connect(SSID, PASSWORD)
    
    # Attendre la connexion
    max_attente = 20
    while max_attente > 0:
        if wifi.isconnected():
            break
        max_attente -= 1
        print("Tentative de connexion...")
        time.sleep(1)
    
    if wifi.isconnected():
        print("Connecté!")
        print("Adresse IP:", wifi.ifconfig()[0])
        return True
    else:
        print("Échec de connexion")
        return False

def envoyer_commande(commande):
    """Envoie une commande HTTP à la voiture"""
    global derniere_commande
    
    if commande != derniere_commande:
        try:
            url = f'http://{ROBOT_IP}/{commande}'
            print(f"Envoi de la commande: {commande}")
            response = urequests.get(url)
            response.close()
            derniere_commande = commande
        except Exception as e:
            print(f"Erreur: {e}")

def verifier_boutons():
    """Vérifie l'état des boutons et envoie des commandes si nécessaire"""
    global etat_boutons
    
    # Bouton Avancer (actif quand pressé = 0)
    nouvel_etat = BOUTON_AVANCER.value()
    if nouvel_etat != etat_boutons['avancer']:
        etat_boutons['avancer'] = nouvel_etat
        if nouvel_etat == 0:  # Bouton pressé
            envoyer_commande('avancer')
        else:  # Bouton relâché
            envoyer_commande('stop')
    
    # Bouton Reculer
    nouvel_etat = BOUTON_RECULER.value()
    if nouvel_etat != etat_boutons['reculer']:
        etat_boutons['reculer'] = nouvel_etat
        if nouvel_etat == 0:
            envoyer_commande('reculer')
        else:
            envoyer_commande('stop')
    
    # Bouton Gauche
    nouvel_etat = BOUTON_GAUCHE.value()
    if nouvel_etat != etat_boutons['gauche']:
        etat_boutons['gauche'] = nouvel_etat
        if nouvel_etat == 0:
            envoyer_commande('gauche')
        else:
            envoyer_commande('stop')
    
    # Bouton Droite
    nouvel_etat = BOUTON_DROITE.value()
    if nouvel_etat != etat_boutons['droite']:
        etat_boutons['droite'] = nouvel_etat
        if nouvel_etat == 0:
            envoyer_commande('droite')
        else:
            envoyer_commande('stop')

# Programme principal
print("Démarrage de la manette de contrôle")

if connecter_wifi():
    print("Appuyez sur les boutons pour contrôler la voiture")
    
    try:
        while True:
            verifier_boutons()
            time.sleep(0.05)  # Petit délai pour éviter de surcharger le processeur
            
            # Vérifier si la connexion WiFi est toujours active
            if not wifi.isconnected():
                print("Connexion WiFi perdue, tentative de reconnexion...")
                if not connecter_wifi():
                    print("Échec de reconnexion")
                    time.sleep(5)  # Attendre avant de réessayer
    
    except KeyboardInterrupt:
        print("Programme arrêté")
else:
    print("Impossible de se connecter au WiFi, vérifiez que la voiture est allumée.")
