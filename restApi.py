from flask import Flask, jsonify,request

app = Flask(__name__)
def pickAndDrop(fromFloor, toFloor):
    current_floor = 8
    time_drop = 0
    state = 'DropOff'
    if (state == 'DropOff'):
        time_drop=4
    come2nd_person = abs((fromFloor - current_floor) * 3)   # after drop a person lift start next journey from current floor to user from floor
    totalTime = come2nd_person + time_drop

    return totalTime

@app.route('/smartkent/liftsimulation/') #default get method
def api():
    fromfl = int(request.args.get('fromFloor'))
    tofl = int(request.args.get('toFloor'))

    eta = pickAndDrop(fromfl, tofl)
    return jsonify({'ETA': eta})

if __name__ == '__main__':
    app.run(port=8090,debug=True)

# the log statement that prints the lifts state
# 20200511091223.123 {"liftId":1, "state":"DROPOFF", "direction":"NAN", "person": "1", "floor" : 8}
# 20200511091223.123 {"liftId":2, "state":"PICKUP", "direction":"UP", "person": "0", "floor" : 4}