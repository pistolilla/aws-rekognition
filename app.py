from flask import Flask, request, make_response
from http import HTTPStatus

import botocore.exceptions

from processing import rekognition, s3

app = Flask(__name__)

@app.route("/")
def main():
    response = make_response({"Message": f"Hello! Documentation for this API is available here: https://documenter.getpostman.com/view/12164167/U16ks5sm"})
    return response

@app.route("/url")
def url():
    try:
        args = dict(request.args)
        res = s3.presigned_post(args.get("filename", None))
        response = make_response(res)
    except botocore.exceptions.ClientError as e:
        response = make_response({"S3Error": str(e)})
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        response = make_response({"Error": str(e)})
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    finally: pass
    return response

@app.route("/labels")
def labels():
    args = dict(request.args)
    try:
        res = rekognition.detect_labels(args["filename"])
        response = make_response({
            "labels": res
        })
    except KeyError as e:
        response = make_response({"Error": f"Incomplete parameters ({str(e)})"})
        response.status_code = HTTPStatus.BAD_REQUEST
    except Exception as e:
        response = make_response({"Error": str(e)})
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    finally: pass
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)