import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MsgApp import app


if __name__ == '__main__':
    app.run(host=os.environ.get("HOST", '127.0.0.1'),
            port=int(os.environ.get("PORT", 3000)),
            debug=True)
