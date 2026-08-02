from flask_socketio import emit, join_room, leave_room


def register_socket_events(socketio):

    @socketio.on("join")

    def join(data):

        room = data["room"]

        join_room(room)

        emit(

            "status",

            {

                "message":

                    "A user joined the room."

            },

            room=room

        )

    @socketio.on("leave")

    def leave(data):

        room = data["room"]

        leave_room(room)

        emit(

            "status",

            {

                "message":

                    "A user left."

            },

            room=room

        )

    @socketio.on("message")

    def message(data):

        emit(

            "message",

            data,

            room=data["room"]

        )