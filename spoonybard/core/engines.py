class Core(object):
    def queue_job(self, job):
        pass

    def queue_change(self, change):
        """
        TODO: take a change, find the jobs to respond to it, queue the jobs
        when jobs complete, update the change
        """

    def run(self):
        """
        TODO:
        set up queues
        check change queue
            queue jobs for change
            add jobs to change
        check jobs queue
            find available executor for job
            start the job running
        check running jobs
            find ones that have finished
            free up the executors
        check changes
            find changes where all jobs have finished
                make them update the original source
        """
