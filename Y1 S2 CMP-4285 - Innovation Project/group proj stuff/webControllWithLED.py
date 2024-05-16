# https://anshu-dev.medium.com/creating-a-python-web-server-from-basic-to-advanced-449fcb38e93b

import os
import serial
import time
import random
from http.server import BaseHTTPRequestHandler, HTTPServer


serialCon = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
serialCon.reset_input_buffer()

host_name = '192.168.0.105'  # IP Address of Raspberry Pi
host_port = 8000


class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Change text to whatever necessary and can use format to display stuff like a number: {}</p>
           <form action="/" method="POST">
               Robot Commands:
               <input type="submit" name="submit" value="Forward">
               <input type="submit" name="submit" value="Backward">
               <input type="submit" name="submit" value="Spin Left">
               <input type="submit" name="submit" value="Spin Right">
               <input type="submit" name="submit" value="Obstacle Avoidance">
               <input type="submit" name="submit" value="Line Tracking">
               <input type="submit" name="submit" value="Stop">
               <input type="submit" name="submit" value="On">
               <input type="submit" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = "12784564.8765876"
        self.do_HEAD()
        #self.wfile.write(html.format(temp[5:]).encode("utf-8")) use this to change values
        self.wfile.write(html.encode("utf-8")) #use this to have it only load what is under

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1] #post_data is the same as text of button

        if post_data == 'On':
            led_number = random.randint(1,2)
            print("Sending number " + str(led_number) + " to Arduino.")
            serialCon.write(str(led_number).encode('utf-8'))
        else:
            print("Turning LED off")
            serialCon.write(str(3).encode('utf-8'))

        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
