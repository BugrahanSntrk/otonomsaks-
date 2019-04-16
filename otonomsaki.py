from darksky import forecast
from datetime import date, timedelta, datetime
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

isik_sensor = 7
toprak_nem_sensor  =16
pencere_motor_kapat=37;
IST = 41.0096,28.9652
weekday = date.today()
GPIO.setup(22,GPIO.OUT)
GPIO.setup(pencere_motor_kapat,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(toprak_nem_sensor,GPIO.IN)

while True: #sonsuz döngümüzü başlattık

    
    GPIO.output(21,GPIO.LOW) ## Pompa açık kalması durumunu engellemek için Pompa çıkış pinlerini "LOW" konuma getirdik.
    GPIO.output(23,GPIO.LOW)
    GPIO.output(29,GPIO.LOW)
    GPIO.output(31,GPIO.LOW)
    
    while(GPIO.input(toprak_nem_sensor) == GPIO.HIGH): #toprka nem sensorü "1" çıkışı verdiğinde pompamız çalışır.
        GPIO.output(21,GPIO.HIGH)
        GPIO.output(23,GPIO.LOW)
        GPIO.output(29,GPIO.LOW)
        GPIO.output(31,GPIO.HIGH)




    with forecast('1815968c5064c61c7d1a59dc17935aae', *IST,units='si') as ist: #DarkSky kütüphanesinden anlık hava durumu verisi çektik.
        temp = ist.temperature
        print(temp)
        
        
    def rc_time (isik_sensor): #ışık sensörünün çalışma kodu
        count = 0
      
        GPIO.setup(isik_sensor, GPIO.OUT)
        GPIO.output(isik_sensor, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(isik_sensor, GPIO.IN)
  
        while (GPIO.input(isik_sensor) == GPIO.LOW):
            count += 1

        return count
    
    
    
    if(rc_time(isik_sensor) >= 3500 and datetime.now().hour > 9 and datetime.now().hour < 18): #gün içinde alanın karanlık olması durumunda aydınlatma sistemi aktif duruma gelir.
        GPIO.output(22,GPIO.HIGH) 
    else:
        GPIO.output(22,GPIO.LOW)
        
    if(temp <= 20): #soğuk havalarda bitkilerin zarar görmemesi için dış ortamla bağlantı kesilir.
        GPIO.output(pencere_motor_kapat,GPIO.HIGH);
    


    print(rc_time(isik_sensor))

   
   
   
   
   
GPIO.cleanup()
    



