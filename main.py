from companyblog import app
import os
from wsgiref import simple_server


# if __name__ == '__main__':
#     app.run(host="0.0.0.0",port=5000)
#     # app.run(debug=False)

port = int(os.getenv("PORT",5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
