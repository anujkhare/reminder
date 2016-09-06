import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from MsgApp import app


if __name__ == '__main__':
    host = os.environ.get("HOST", '0.0.0.0')
    port = int(os.environ.get("PORT", 3000))
    app.run(host=host,
            port=port,
            debug=True)
