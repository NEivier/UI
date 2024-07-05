import Adafruit_DHT
import RPi.GPIO as GPIO

#设置传感器的型号和引脚
sensor = Adafruit_DHT.DHT11
pin = 19

#初始化GPIO库
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def get_tmp_hmd():
	try:
		# while True:
		#读取传感器数据
		humidity,temperature = Adafruit_DHT.read_retry(sensor,pin)
		#如果读取成功，则输出温湿度数值
		if humidity is not None and temperature is not None:
			print("湿度={0:0.1f} 温度={1:0.1f}°C".format(humidity,temperature))
		else:
			print('读取传感器数值失败')
	except KeyboardInterrupt:
		print('程序终止 ')

	finally:
		#清理GPIO资源
		GPIO.cleanup()
	return [temperature,humidity]
if __name__ == '__main__':
	tmp,hmd=get_tmp_hmd()
	print(hmd)
	print(tmp)
	
