from flask import Flask, jsonify,request
import time
import threading

floor = 8
estimate_time = 0
state = "DROPOFF"
direction = "NAN"
person = 0

floors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def dropoff():
    state = "DROPOFF"
    person = 0
    print(time.time(), '\t', {'state': state, "Direction": direction, "Person": person, "floor":floor})
    time.sleep(4)


def pickup():
    state= "PICKUP"
    person = 1
    print(time.time(), '\t', {'state': state, "Direction": direction, "Person": person, "floor":floor})
    time.sleep(4)
    state = "TO_DROPOFF"


def move_floor(pick):
    to = 0
    frm = 0
    if direction == "UP":
        frm = floor
        to = pick
    else:
        frm = pick
        to = floor
    for i in range(frm, to):
        if direction == "UP":
            floor += 1
        else:
            floor -= 1
            estimate_time -= 3
        print(time.time(), '\t', {'state': state, "Direction": direction, "Person": person, "floor":floor})
        time.sleep(3)


def eta_time(pick):
    between_floors = pick - floor
    direct = "NAN"
    eta_estimation = 0
    if between_floors >= 0:
        direct = "UP"
        eta_estimation = between_floors * 3
    else:
        direct = "DOWN"
        eta_estimation = -between_floors * 3
        direction = direct
        estimate_time = eta_estimation
    return eta_estimation


def lift_process(pick, drop):
    state = "TO_PICKUP"
    move_floor(pick)
    pickup()
    state = "TO_DROPOFF"
    eta_time(drop)
    move_floor(drop)
    dropoff()
    state = "IDLE"
    direction = "NAN"
    print(time.time(), '\t', {'state': state, "Direction": direction, "Person": person, "floor":floor})


app = Flask(__name__)
def pickAndDrop(fromFloor, toFloor):
    if state == "DROPOFF":
        print(time.time(), '\t', {'state': state, "Direction": direction, "Person": person, "floor":floor})
        download_thread = threading.Thread(target=lift_process, args=[fromFloor, toFloor])
        download_thread.start()
        return eta_time(fromFloor)
    else:
        return jsonify({"error": "Lift hold another person wait "})

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

