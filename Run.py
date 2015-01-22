from flask import Flask, render_template
from flask.ext.socketio import SocketIO, send, emit
import os
app = Flask(__name__)
socketio = SocketIO(app)

mission = False
admiralTaken = False
engineerTaken = False
brokenSystemList = []
admiralName = ""
engineerName = ""
brokenSystemName = ""
@socketio.on('message', namespace="/main")
def handle_message(message):
    global mission
    global admiralTaken
    global engineerTaken
    global admiralName
    global engineerName
    global brokenSystemList
    if message == "start mission":
        mission = True
        send("missionyes", broadcast=True)
        print mission
    if message.startswith("admiral name: "):
        admiralName = message[14:]
        admiralTaken = True
        send("admiraltaken: "+admiralName, broadcast=True)
        print admiralName
    if message.startswith("engineer name: "):
        engineerName = message[15:]
        engineerTaken = True
        send("engineertaken: "+engineerName, broadcast=True)
        print engineerName
    if message.startswith("brokensystem: "):
        brokenSystemName = message[14:]
        brokenSystemList.append(brokenSystemName);
        send("predamage", broadcast=True)
        for system in brokenSystemList:
            send("brokensystem: " + system, broadcast=True)
    if message.startswith("fixsystem: "):
        fixSystemName = message[11:]
        brokenSystemList.remove(fixSystemName);
        print fixSystemName
        send("predamage", broadcast=True)
        for system in brokenSystemList:
            send("brokensystem: " + system, broadcast=True)

@socketio.on('connect', namespace="/main")
def startSocket():
    global mission
    global admiralTaken
    global engineerTaken
    global admiralName
    global engineerName
    global brokenSystemList
    
    send("predamage", broadcast=True)
    if mission == True:
        send("connected")
        send("missionyes")
        print "hallelujia"
    if mission == False:
        send("connected")
        print mission
    if admiralTaken == True:
        send("admiraltaken: "+admiralName)
        print "asdfjkl;"
    if engineerTaken == True:
        send("engineertaken: "+engineerName)
        print "efvrgb"
    for system in brokenSystemList:
        send("brokensystem: " + system, broadcast=True)

@app.route('/')
def load():
    return render_template("index.html")

@app.route('/index.html')
def loadbackup():
    return render_template("index.html")

@app.route('/flight-director.html')
def loadflightdirector():
    return render_template("flight-director.html")

@app.route('/flight-director-navigations.html')
def loadflightdirectornavigations():
    return render_template("flight-director-navigations.html")

@app.route('/flight-director-operations.html')
def loadflightdirectoroperations():
    return render_template("flight-director-operations.html")

@app.route('/flight-director-tactical.html')
def loadflightdirectortactical():
    return render_template("flight-director-tactical.html")

@app.route('/flight-director-engineering.html')
def loadflightdirectorengineering():
    return render_template("flight-director-engineering.html")

@app.route('/flight-director-admiral.html')
def loadflightdirectoradmiral():
    return render_template("flight-director-admiral.html")

@app.route('/admiral.html')
def loadadmiral():
    return render_template("admiral.html")

@app.route('/admiral-self-destruct.html')
def loadadmiralselfdestruct():
    return render_template("admiral-self-destruct.html")

@app.route('/engineer.html')
def loadengineer():
    return render_template("engineer.html")

@app.route('/engineer-distribution.html')
def loadengineerdistribution():
    return render_template("engineer-distribution.html")

if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 80)