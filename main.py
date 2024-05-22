from flask import Flask, render_template, request

from expert import Light, RobotCrossStreet

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    response = None

    if request.method == 'POST':
        light_color = request.form.get('light_color')
        # Instantiate the system
        system = RobotCrossStreet()

        # Feed the facts to the system and run it
        system.reset()
        system.declare(Light(color=light_color))
        system.run()
        response = system.response
        print(response)
        

    return render_template('index.html', response=response)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)