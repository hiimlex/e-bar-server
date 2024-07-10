from .. import socketio


def socket_update_orders():
    socketio.emit('/socket/orders')