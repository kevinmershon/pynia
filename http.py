import base64
import json
import redis as Redis
import sys
import threading
import time
import web
import nia as NIA

urls = (
    '/', 'index',
    '/get_steps', 'get_steps'
)

# global scope stuff
nia = None
nia_data = None
redis = None

class index:
    def GET(self):
        render = web.template.render("templates/")
        return render.index()

class get_steps:
    def GET(self):
        web.header("Content-Type", "application/json")
        data = {
            "brain_fingers": web.brain_fingers
        }
        return json.dumps(data)

class Updater:
    def update(self):
        while True:
            # kick-off processing data from the NIA
            data_thread = threading.Thread(target=nia_data.get_data)
            data_thread.start()

            # get the fourier data from the NIA
            data, steps = nia_data.fourier(nia_data)
            web.brain_fingers = steps

            now = time.time()
            redis.zadd("brainfingers", now, steps)

            # wait for the next batch of data to come in
            data_thread.join()

            # exit if we cannot read data from the device
            if nia_data.AccessDeniedError:
                sys.exit(1)

if __name__ == "__main__":
    app = web.application(urls, globals())

    # start up redis
    redis = Redis.StrictRedis(host='localhost', port=6379, db=0)

    # open the NIA, or exit with a failure code
    nia = NIA.NIA()
    if not nia.open():
        sys.exit(1)

    # start collecting data
    milliseconds = 50
    nia_data = NIA.NiaData(nia, milliseconds)

    # kick-off processing data from the NIA
    updater = Updater()
    update_thread = threading.Thread(target=updater.update)
    update_thread.start()

    # run the app
    app.run()

    # when web.py exits, close out the NIA and exit gracefully
    nia.close()
    redis.disconnect()
    sys.exit(0)
