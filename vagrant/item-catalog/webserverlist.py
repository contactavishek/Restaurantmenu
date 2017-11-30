# List all the restaurant names in the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()


class webServerHandler(BaseHTTPRequestHandler):
      def do_GET(self):
          try:
              if self.path.endswith("/restaurants"):
                 restaurant= session.query(Restaurant).all()
                 self.send_response(200)
                 self.send_header('Content-type','text/html')
                 self.end_headers()
                 output= " "
                 output+= "<html><body>" 
                 for i in restaurant:
                     output+= i.name
                     output+= "</br>"
                     print i.name
                     print "\n"
                 
                 output+= "</body></html>"
                 self.wfile.write(output)
                 return
          
          except IOError:
                   self.send_error(404,"Restaurant not found: %s" %self.path)


def main():
    try:
        port=8080
        server=HTTPServer(('',port),webServerHandler)
        print "Restaurant server running on port %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
            print "^C entered, stopping web server"
            server.socket.close()

if __name__=='__main__':
     main()


