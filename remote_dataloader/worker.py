import ast
import json
import pickle
import time

import zmq
import argparse
import socket

from remote_dataloader.common import random_string, byte_message, CODE_INIT, CODE_POLL

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--server', type=str, help='server id:port. (eg. 0.0.0.0:1958)', required=True)
    args = parser.parse_args()

    # connect
    context = zmq.Context()
    myid = '%s-%s' % (socket.gethostname(), random_string())
    print("Connecting to server=%s myid=%s" % (args.server, myid))
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s" % args.server)

    # request to initialization
    socket.send(byte_message(myid, CODE_INIT, ''))
    fetcher = pickle.loads(socket.recv())

    print("Initialized.")

    jobid = data = None
    while True:
        socket.send(byte_message(myid, CODE_POLL, (jobid, data)))

        msg = pickle.loads(socket.recv())
        jobid = msg['message']    # list converted to string(eg. "[id1, id2, ...]")
        if jobid is None:
            jobid = data = None
            time.sleep(1)
        else:
            data = fetcher.fetch(ast.literal_eval(jobid))
