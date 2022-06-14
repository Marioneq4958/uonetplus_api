import json


def status_check(status_check_code, status_check_json, fg):
    if status_check_code == 200:
        status_check_response = print(
            "\n" + fg.lightgreen + "OK " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 111:
        status_check_response = print(
            "\n" + fg.red + "Connection refused " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 307:
        status_check_response = print(
            "\n" + fg.orange + "Temporary redirect " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 308:
        status_check_response = print(
            "\n" + fg.orange + "Permanent redirect " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 310:
        status_check_response = print(
            "\n" + fg.red + "Too many redirects " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 400:
        status_check_response = print(
            "\n" + fg.red + "Bad Request " + str(status_check_code) + fg.rs
        )
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 401:
        status_check_response = print(
            "\n" + fg.red + "Unauthorized " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 403:
        status_check_response = print(
            "\n" + fg.red + "Forbidden " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 404:
        status_check_response = print(
            "\n" + fg.orange + "Not Found " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 405:
        status_check_response = print(
            "\n" + fg.orange + "Method Not Allowed " + str(status_check_code) + fg.rs
        )
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 408:
        status_check_response = print(
            "\n" + fg.orange + "Request Timeout " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 422:
        status_check_response = print(
            "\n" + fg.red + "Unprocessable Entity " + str(status_check_code) + fg.rs
        )
        try:
            print(json.dumps(status_check_json, indent=4))
        except:
            print(status_check_json)
    elif status_check_code == 429:
        status_check_response = print(
            "\n" + fg.red + "Too Many Requests " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 500:
        status_check_response = print(
            "\n" + fg.red + "Internal Server Error " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 502:
        status_check_response = print(
            "\n" + fg.orange + "Bad Gateway " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 503:
        status_check_response = print(
            "\n" + fg.orange + "Service Unavailable " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 504:
        status_check_response = print(
            "\n" + fg.orange + "Gateway Timeout " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 505:
        status_check_response = print(
            "\n"
            + fg.orange
            + "HTTP Version Not Supported "
            + str(status_check_code)
            + fg.rs
        )
    elif status_check_code == 521:
        status_check_response = print(
            "\n" + fg.red + "Web server is down " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 522:
        status_check_response = print(
            "\n" + fg.red + "Connection timed out " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 525:
        status_check_response = print(
            "\n" + fg.red + "SSL Handshake Failed " + str(status_check_code) + fg.rs
        )
    elif status_check_code == 526:
        status_check_response = print(
            "\n" + fg.red + "Invalid SSL Certificate " + str(status_check_code) + fg.rs
        )
    try:
        return status_check_response, status_check_json
    except:
        return status_check_response
