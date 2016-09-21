from bottle import get, post, route, run, template, request, static_file, error, \
    redirect

import sqlite3

conn = sqlite3.connect('human_data')

# As if:
#  GET localhost:8080/ :
#    hello()
#  GET localhost:8080/hello/Jablonky :
#    hello("Jablonky")

STATIC_FILE_ROOT = "./"

@get('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root=STATIC_FILE_ROOT)

#from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'

@route('/')
@route('/hello/<inp_name>')
def hello(inp_name="Python"):
    return template("Hello, {{name}}!", name=inp_name)

@route('/human')
def a_human():
    # FIXME: Replace 'humans' with SQL
    human_id = int(request.query.id)
    human = humans[human_id]

    return template("<div>Name: {{name}}, color: {{color}}",
        name=human['name'], color=human['color'])

@route('/humans/<id:int>')
def human_details(id):
    # FIXME: Replace 'humans' with SQL
    assert isinstance(id, int)

    human = humans[id]

    return template("<div>Name: {{name}}, color: {{color}}",
        name=human['name'], color=human['color'])


@get('/humans') # or @route('/login')
def show_humans():
    human_list = ""

    c = conn.cursor()
    c.execute("SELECT * FROM humans")

    humans = c.fetchall()
    conn.commit()

    for human in humans:
        human_list = human_list + template("<div>Name: {{name}}, color: {{color}}",
            name=human[1], color=human[2])

    return human_list + '''
    <form action="/humans" method="post">
            Human name: <input name="name" type="text" />
            Human's favorite color: <input name="color" type="text" />
            <input value="Add Human" type="submit" />
        </form>
    '''

@post('/humans') # or @route('/login', method='POST')
def add_human():
    name = request.forms.get('name')
    color = request.forms.get('color')

    c = conn.cursor()
    c.execute("INSERT INTO humans (name, color) VALUES (?, ?)", (name, color))

    conn.commit()

#    humans.append( { "name": name, "color": color } )

    return redirect("/humans")
#    return template("Added {{name}}", name=name)

@get('/humans.json')
def humans_json():
    # FIXME: Replace 'humans' with SQL

    return { "humans": humans }


run(host='localhost', port=8080, debug=True)
