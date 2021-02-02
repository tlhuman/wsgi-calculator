"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def responce_404():
    """not found or bad url"""
    return "404 Not Found", "404<br>NOT FOUND"

def responce_500():
    """misc errors"""
    return "500 Internal Server Error", "500<br>INTERNAL SERVER ERROR"

def responce_403():
    """forbidden data errors"""
    return "403 Forbidden", "403<br>FORBIDDEN - BAD ARGUMENTS"

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    total = float(args[0])
    for arg in args[1:]:
        try:
            total += float(arg)
        except ValueError:
            raise NameError

    return str(total)

def subtract(*args):
    """ Returns a STRING with the subtraction of the arguments """
    total = float(args[0])
    for arg in args[1:]:
        try:
            total -= float(arg)
        except ValueError:
            raise NameError

    return str(total)

def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """
    total = float(args[0])
    for arg in args[1:]:
        try:
            total *= float(arg)
        except ValueError:
            raise NameError

    return str(total)

def divide(*args):
    """ Returns a STRING with the division of the arguments """
    total = float(args[0])
    for arg in args[1:]:
        try:
            total /= float(arg)
        except ValueError:
            raise NameError

    return str(total)

def index(*args):
    return '\n'.join(["<html>",
                      "<head>",
                      "<title>A calculator</title>",
                      "<h1>Welcome to the Calculator!</h1>"
                      "</head>",
                      "<body>",
                      "<p>Use the URL to do some math.</p>",
                      "<p></p>",
                      "<p></p>",
                      "<p>Like this!</p>",
                      "<p>.../multiply/3/5   => 15</p>",
                      "<p>.../add/23/42      => 65</p>",
                      "<p>.../subtract/23/42 => -19</p>",
                      "<p>.../divide/22/11   => 2</p>",
                      "</body>",
                      "</html>",
                      ])


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    func_dict = {"add": add,
                 "subtract": subtract,
                 "multiply": multiply,
                 "divide": divide,
                 "": index}

    # delimit to segments
    path_parts = path.strip("/").split("/")

    # variable assign
    func_name = path_parts[0]
    args = path_parts[1:]

    # function test
    try:
        func = func_dict[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    try:
        request_path = environ.get('PATH_INFO', "")
        if not request_path:
            raise NameError
        func, args = resolve_path(request_path)
        status = "200 OK"
        body = func(*args)
    except NameError:
        status, body = responce_404()
    except ZeroDivisionError:
        # forbidden variable error
        status, body = responce_403()
    except Exception as e:
        status, body = responce_500()
        body += f"<br><span>{str(e)}</span>"

    response_headers = [('Content-Type', 'text/html'),
                        ]
    start_response(status, response_headers)
    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
