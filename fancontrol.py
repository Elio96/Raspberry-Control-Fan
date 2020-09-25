import subprocess
import time
from gpiozero import OutputDevice

GRADI_ON = 55
GRADI_OFF = 45
SLEEP_INTERVAL = 5
GPIO_PIN = 17


def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_string = output.stdout.decode()
    try:
        return float(temp_string.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Non posso fare parsing della temperatura')


if __name__ == '__main__':
    if GRADI_OFF >= GRADI_ON:
        raise RuntimeError('La temperatura dei gradi per lo spegnimento deve essere minore rispetto all\'accensione')

    fan = OutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()
        if temp > GRADI_ON and not fan.value:
            fan.on()
        elif fan.value and temp < GRADI_OFF:
            fan.off()
        time.sleep(SLEEP_INTERVAL)
