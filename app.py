import logging
import sleuth
import b3

from flask import Flask

app = Flask("service-c2")


@app.route('/')
def service():
    logger.info(app.name + " has been called.")

    with b3.SubSpan() as headers:
        logger.info(app.name + " pretending to call a database that doesn't support B3 headers.")

    logger.info(app.name + " did a thing.")

    return "Service call succeeded (" + app.name + ")"


if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting " + app.name)

    app.before_request(b3.start_span)
    app.after_request(b3.end_span)
    app.run(
        host="0.0.0.0",
        port=int(8003),
        debug=True,
        threaded=True
    )
