import Queue
import threading
from worker_thread import worker_thread
from thread_job import thread_job


class threadpool:
    _nthreads = 0
    _q_size = 0
    _job_q = Queue.Queue()
    _result_q = Queue.Queue()
    _total_jobs = 0
    _threads = []
    is_active = 0

    def __init__(self, nthreads=10):
        self._nthreads = nthreads

    def start(self):
        for i in range(self._nthreads):
            t = worker_thread(self._job_q, self._result_q)
            self.is_active = True
            self._threads.append(t)
            t.start()
        return True

    def add_job(self, job):
        self._job_q.put(job)
        self._total_jobs += 1
        return True

    def finish(self):
        self._job_q.join()
        self.is_active = False
        return True

    def unfinished_tasks(self):
        return self._job_q.qsize()

    def finished_tasks(self):
        return self._total_jobs - self._job_q.qsize()
