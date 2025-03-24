from machine import Pin, PWM
import time

# Définition des broches pour le moteur
IN1 = Pin(12, Pin.OUT)
IN2 = Pin(14, Pin.OUT)
IN3 = Pin(13, Pin.OUT)
IN4 = Pin(27, Pin.OUT)
ENA = PWM(Pin(26), freq=1000, duty_u16= 0)
ENB = PWM(Pin(25), freq=1000, duty_u16= 0)

ENA.duty_u16(65535)
ENB.duty_u16(64879)

# Paramètres de calibration (16 bits)
VITESSE_MAX = 65535
VITESSE_VIRAGE = int(VITESSE_MAX * 0.78)  # ~78% de la vitesse max pour tourner

# Valeurs mesurées
VITESSE_CM_PAR_SECONDE = 69.0
VITESSE_DEGRE_PAR_SECONDE = 690.0

# Capteur ultrason
TRIG = Pin(32, Pin.OUT)
ECHO = Pin(34, Pin.IN)
mesures = [100, 100] 

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

def cm_to_seconds(distance_cm):
    return distance_cm / VITESSE_CM_PAR_SECONDE

def degrees_to_seconds(angle_degrees):
    return abs(angle_degrees) / VITESSE_DEGRE_PAR_SECONDE

def avancer(distance_cm, vitesse=VITESSE_MAX):
    duree = cm_to_seconds(distance_cm)
    set_vitesses(vitesse, vitesse)
    IN1.on(); IN2.off(); IN3.on(); IN4.off()
    time.sleep(duree)

def tourner_gauche(angle_degrees, vitesse=VITESSE_VIRAGE):
    duree = degrees_to_seconds(angle_degrees)
    set_vitesses(vitesse, vitesse)
    IN1.off(); IN2.on(); IN3.on(); IN4.off()
    time.sleep(duree)

def tourner_droite(angle_degrees, vitesse=VITESSE_VIRAGE):
    duree = degrees_to_seconds(angle_degrees)
    set_vitesses(vitesse, vitesse)
    IN1.on(); IN2.off(); IN3.off(); IN4.on()
    time.sleep(duree)

def stop(duree=None):
    IN1.off(); IN2.off(); IN3.off(); IN4.off()
    set_vitesses(0, 0)
    if duree:
        time.sleep(duree)

def verifier_obstacle():
    distance = mesure_distance()
    if distance < 30:
        stop()
        print("Obstacle détecté à", distance, "cm")
        return True
    return False

def suivre_circuit_parcours():
    print("🚦 Début du parcours")
    stop(2)
    avancer(80)
    tourner_droite(420)
    avancer(75)
    tourner_droite(175)
    avancer(30)
    tourner_gauche(130) 
    avancer(30)
    tourner_droite(200) 
    avancer(15)
    tourner_droite(200)
    avancer(15)
    tourner_droite(200)
    avancer(40)
    tourner_gauche(200)
    avancer(15)
    tourner_gauche(200)
    avancer(15)
    tourner_gauche(200)
    avancer(40)
    tourner_droite(200) 
    avancer(15)
    tourner_droite(200)
    avancer(15)
    tourner_droite(200) 
    avancer(40)
    tourner_droite(200) 
    avancer(70)
    print("🏁 Circuit terminé")
    stop(1)

try:
    while True:
        suivre_circuit_parcours()
        stop(2)
        input("Appuyez sur Entrée pour recommencer ou Ctrl+C pour arrêter...")
except KeyboardInterrupt:
    stop()
    print("Programme arrêté.")



