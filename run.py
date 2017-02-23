import os, sys
from app import create_app

app = create_app()

if __name__ == '__main__':
    try:
        port = int(sys.argv[-1])
    except ValueError:
        port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
   
