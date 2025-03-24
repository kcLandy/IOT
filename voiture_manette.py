from machine import Pin, PWM
import network
import socket
import time

# Configuration WiFi - Mode Point d'Accès
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='RobotVoiture', password='12345678', authmode=network.AUTH_WPA_WPA2_PSK)
print("Point d'accès WiFi créé: RobotVoiture")
print("Adresse IP:", ap.ifconfig()[0])

# Définition des broches pour le moteur
IN1 = Pin(12, Pin.OUT)
IN2 = Pin(14, Pin.OUT)
IN3 = Pin(13, Pin.OUT)
IN4 = Pin(27, Pin.OUT)
ENA = PWM(Pin(26), freq=1000, duty_u16=0)
ENB = PWM(Pin(25), freq=1000, duty_u16=0)
ENA.duty_u16(65535)
ENB.duty_u16(64879)

# Paramètres de calibration (16 bits)
VITESSE_MAX = 65535
VITESSE_VIRAGE = int(VITESSE_MAX * 0.78)  # ~78% de la vitesse max pour tourner

# Capteur ultrason
TRIG = Pin(32, Pin.OUT)
ECHO = Pin(34, Pin.IN)
mesures = [100, 100]

# Variable pour suivre l'état actuel
etat_mouvement = "stop"
obstacle_detecte = False

def set_vitesses(vitesse_gauche, vitesse_droite):
    ENA.duty_u16(vitesse_gauche)
    ENB.duty_u16(vitesse_droite)

def mesure_distance():
    TRIG.off()
    time.sleep_us(2)
    TRIG.on()
    time.sleep_us(10)
    TRIG.off()
    debut, fin = 0, 0
    while ECHO.value() == 0:
        debut = time.ticks_us()
    while ECHO.value() == 1:
        fin = time.ticks_us()
    distance = ((fin - debut) * 0.0343) / 2 if debut and fin else 100
    mesures.pop(0)
    mesures.append(distance)
    return sum(mesures) / len(mesures)

def verifier_obstacle():
    global obstacle_detecte
    distance = mesure_distance()
    if distance < 30:
        if not obstacle_detecte:
            stop()
            obstacle_detecte = True
            print("Obstacle détecté à", distance, "cm")
        return True
    
    # Si l'obstacle a été retiré
    if obstacle_detecte:
        obstacle_detecte = False
        print("Obstacle retiré")
        # On reprend le mouvement précédent
        if etat_mouvement == "avancer":
            avancer()
        elif etat_mouvement == "reculer":
            reculer()
        elif etat_mouvement == "gauche":
            tourner_gauche()
        elif etat_mouvement == "droite":
            tourner_droite()
    
    return False

# Fonctions de contrôle du robot
def avancer():
    global etat_mouvement
    if not obstacle_detecte:
        set_vitesses(VITESSE_MAX, VITESSE_MAX)
        IN1.on(); IN2.off(); IN3.on(); IN4.off()
        etat_mouvement = "avancer"
        print("Avancer")

def reculer():
    global etat_mouvement
    set_vitesses(VITESSE_MAX, VITESSE_MAX)
    IN1.off(); IN2.on(); IN3.off(); IN4.on()
    etat_mouvement = "reculer"
    print("Reculer")

def tourner_gauche():
    global etat_mouvement
    if not obstacle_detecte:
        set_vitesses(VITESSE_VIRAGE, VITESSE_VIRAGE)
        IN1.off(); IN2.on(); IN3.on(); IN4.off()
        etat_mouvement = "gauche"
        print("Tourner à gauche")

def tourner_droite():
    global etat_mouvement
    if not obstacle_detecte:
        set_vitesses(VITESSE_VIRAGE, VITESSE_VIRAGE)
        IN1.on(); IN2.off(); IN3.off(); IN4.on()
        etat_mouvement = "droite"
        print("Tourner à droite")

def stop():
    global etat_mouvement
    IN1.off(); IN2.off(); IN3.off(); IN4.off()
    set_vitesses(0, 0)
    etat_mouvement = "stop"
    print("Stop")

# Configuration du serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("Serveur web démarré")

# Pour vérifier régulièrement les obstacles
last_obstacle_check = time.time()

try:
    while True:
        # Vérifier les obstacles toutes les 200ms
        current_time = time.time()
        if current_time - last_obstacle_check > 0.2:
            verifier_obstacle()
            last_obstacle_check = current_time
            
        # Gestion des connexions au serveur web
        try:
            conn, addr = s.accept()
            request = conn.recv(1024)
            request = str(request)
            
            # Analyse de la requête
            if '/avancer' in request:
                avancer()
            elif '/reculer' in request:
                reculer()
            elif '/gauche' in request:
                tourner_gauche()
            elif '/droite' in request:
                tourner_droite()
            elif '/stop' in request:
                stop()

            # Envoi d'une réponse simple
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/plain\n')
            conn.send('Connection: close\n\n')
            conn.sendall('OK')
            conn.close()
        except OSError as e:
            pass
            
except KeyboardInterrupt:
    stop()
    s.close()
    ap.active(False)
    print("Programme arrêté.")
