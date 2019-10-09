import json
import pickle
import time

import zmq
from torch.utils.data.dataloader import _BaseDataLoaderIter, _DatasetKind, DataLoader
from zmq.error import ZMQError

from remote_dataloader.common import CODE_INIT, byte_message, CODE_POLL


class _ZmqDataLoaderIter(_BaseDataLoaderIter):
    def __init__(self, loader):
        super(_ZmqDataLoaderIter, self).__init__(loader)
        self.dataset_fetcher = _DatasetKind.create_fetcher(self.dataset_kind, self.dataset, self.auto_collation, self.collate_fn, self.drop_last)
        self.pickled_fetcher = pickle.dumps(self.dataset_fetcher, protocol=pickle.HIGHEST_PROTOCOL)

        self.socket = loader.socket
        self.timeout = loader.timeout
        self.requested_queue = []
        self.received_result = {}

    def __next__(self):
        no_more_jobs = False
        while not no_more_jobs or len(self.requested_queue) > 0:
            #  Wait for next request from client
            try:
                message = self.socket.recv(zmq.NOBLOCK)
            except ZMQError:
                # check queue
                if len(self.requested_queue) > 0:
                    jobid, request_t = self.requested_queue[0]
                    if jobid in self.received_result:
                        self.requested_queue.pop(0)
                        data = self.received_result.pop(jobid)
                        return data
                continue

            # process client's message
            msg = pickle.loads(message)
            if msg['code'] == CODE_INIT:
                cmd = self.pickled_fetcher
            elif msg['code'] == CODE_POLL:
                jobid, data = msg['message']
                if jobid is not None:
                    self.received_result[jobid] = data
                try:
                    request_t = self.requested_queue[0][1] if len(self.requested_queue) > 0 else -1
                    if request_t > 0 and 0 < self.timeout < time.time() - request_t > 0:
                        jobid, request_t = self.requested_queue[0]
                        self.requested_queue[0][1] = time.time()
                    else:
                        jobid = str(self._next_index())
                        self.requested_queue.append([jobid, time.time()])
                    cmd = byte_message('server', CODE_POLL, jobid)
                except StopIteration:
                    cmd = byte_message('server', CODE_POLL, None)
                    no_more_jobs = True
            else:
                raise ValueError('cannot process message: %s' % msg)

            # Send reply back to client
            self.socket.send(cmd)
        raise StopIteration()


class RemoteDataLoader(DataLoader):
    def __init__(self, dataset, batch_size=1, shuffle=False, sampler=None,
                 batch_sampler=None, collate_fn=None, pin_memory=False, drop_last=False, timeout=0,
                 listen='*:1958'):
        super(RemoteDataLoader, self).__init__(dataset, batch_size, shuffle=shuffle, sampler=sampler,
                                               batch_sampler=batch_sampler, collate_fn=collate_fn, pin_memory=pin_memory,
                                               drop_last=drop_last)

        # socket
        self.timeout = timeout
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://%s" % listen)

    def __iter__(self):
        return _ZmqDataLoaderIter(self)
