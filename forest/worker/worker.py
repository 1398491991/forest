from forest.worker.threadpool import ThreadPool as _ThreadPool
# from threadpool import NoWorkersAvailable,NoResultsPending


class ThreadPool(_ThreadPool):
    def poll(self, block=False):
        """Process any new results in the queue."""
        while True:
            # still results pending?
            if not self.workRequests:
                print 'NoResultsPending'
            # are there still workers to process remaining requests?
            elif block and not self.workers:
                print  'NoWorkersAvailable'
            try:
                # get back next results
                request, result = self._results_queue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # hand results to callback, if any
                if request.callback and not \
                       (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Exception:
                pass
                # break