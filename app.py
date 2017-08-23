import logging
import sleuth
import b3

from flask import Flask
import os

app = Flask("sleuth-c")
port = int(os.getenv("PORT", "8003"))

# Set the root logger to INFO so we can see B3 messages:
logging.getLogger().setLevel(logging.INFO)


@app.route('/')
def service():
    log = logging.getLogger(app.name)
    log.setLevel(logging.DEBUG)
    log.info(app.name + " has been called.")

    with b3.SubSpan() as headers:
        log.info(app.name + " pretending to call a database that doesn't support B3 headers.")

    log.info(app.name + " did a thing.")

    return "Service call succeeded (" + app.name + ")"


@app.before_request
def before_request():
    b3.start_span()


@app.after_request
def after_request(response):
    return b3.end_span(response)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(port),
        debug=True,
        threaded=True
    )
