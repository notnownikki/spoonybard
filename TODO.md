Dev plan and checklist
======================

This is a checklist of what's being currently worked on so
I can write small features and mark off what's done. It's
not a roadmap for public consuption.

Right now
---------

* Executor marked as in use
* Job calls start and finish on executor

Next
----

* Accept incoming github PR notifications
* Pull code for a PR into a local clone of the repo
  * Queue the change
  * Fetch the ref into local repo
  * Change must know how to update the status of the change (e.g. github, gerrit...)
* UI auth by github
* List of PRs and their status
* Convert PR into jobs to run
* Local runner provider
* SSH runner provider
* Register remote slave for SSH runner to use
* Queue jobs
* Dispatch jobs to runners
* Monitor jobs
* Collect console logs
* Report success / failure to PR
* Time based jobs
