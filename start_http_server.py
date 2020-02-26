from wsgiref.simple_server import make_server
 
import json
import smbus
import datetime

def get_temp():
    bus = smbus.SMBus(1)

    address = 0x48
    register = 0x00
    configration = 0x03

    bus.write_word_data(address, configration, 0x00)
    word_data = bus.read_word_data(address, register)

    print(hex(word_data))

    data = (word_data & 0xff00 ) >> 8 |(word_data & 0xff) << 8
    
    data = data >> 3
    
    return (data/16.)


def app(environ, start_response):
    status = '200 OK'
    headers = [
      ('Content-type', 'application/json; charset=utf-8'),
      ('Access-Control-Allow-Origin', '*'),
    ]
    start_response(status, headers)
    
    temp = get_temp()
    now = datetime.datetime.now().strftime("%H:%M:%S")
   
    return [json.dumps({'date': now ,'temp': temp }).encode("utf-8")]
 
 
def main():
  #with make_server('', 3000, app) as httpd:
    print("Serving on port 3000...")
    make_server('', 3000, app).serve_forever()
    
if __name__== "__main__":
  main()
