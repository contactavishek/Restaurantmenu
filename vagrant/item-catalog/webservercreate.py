# Create new restaurant link
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/restaurants/new"):
                output = ""
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output += "<html><body>"
                output+= "<h1> Make New Restaurant here: </h1>"
                output+= '''<form method= 'POST' enctype= 'multipart/form-data' action='/restaurants/new'> <input name='newrestaurantname' type="text" placeholder='New Restaurant Name'><input type='submit' value='create'></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
           
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Objective 3 Step 1 - Create a Link to create a new Restaurant
                output += "<a href= '/restaurants/new'> Make a new Restaurant here </a></br>"
                output+= "<html><body>"
                for i in restaurants:
                    output += i.name
                    # Objective 2 -- Add Edit and Delete Links
                    output += "</br><a href ='#' >Edit </a></br> "
                    output += "<a href =' #'> Delete </a></br></br> "
                    print i.name
                    print "\n"

                output += "</body></html>"
                self.wfile.write(output)
                return
     
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype,pdict= cgi.parse_header(self.headers.getheader('content-type'))
                if ctype== 'multipart/form-data':
                    fields= cgi.parse_multipart(self.rfile,pdict)
                    messagecontent= fields.get('newrestaurantname')
                
                # Create new Restaurant Object
                newrestaurant = Restaurant(name=messagecontent[0])
                session.add(newrestaurant)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except:
               pass

 
def main():
    try:
        server = HTTPServer(('',8080), webServerHandler)
        print 'Web server running...open localhost:8080/restaurants in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

