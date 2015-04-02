import threading
import Queue


class worker_thread(threading.Thread):

    def __init__(self, job_q, result_q):
        super(worker_thread, self).__init__()
        self._job_q = job_q
        self._result_q = result_q

    def run(self):
        while self._job_q.qsize():
            try:
                job = self._job_q.get(None)
            except Queue.Empty:  # Exit the worker if Q empty
                return False
            job.execute()
            self._result_q.put(job)
            self._job_q.task_done()
        return True
