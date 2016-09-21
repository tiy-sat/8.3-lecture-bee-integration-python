from bottle import route, run, template

# As if:
#  GET localhost:8080/ :
#    hello()
#  GET localhost:8080/hello/Jablonky :
#    hello("Jablonky")

@route('/')
@route('/hello/<inp_name>')
def hello(inp_name="Python"):
    return template("Hello, {{name}}!", name=inp_name)


@route('/humans/<id:int>')
def human_details(id):
    assert isinstance(id, int)

    return "Human here!"




run(host='localhost', port=8080, debug=True)
