Minimal Django project to start a long-running backend process while a percentage progress
indicator is displayed to the client. The client can cancel the request and cause the backend
processing to be terminated).
 
- The Python framework is a 'minimal Django' site: Django in one file!
- The processing task on the backend is a simple update/sleep loop for a second at a time, for 10 secs
- The long-running task uses multiprocessing (ie: thread-like) behaviour to control the long running process
- The user interface uses Angular JS and Ajax
- Some TDD test coverage to guide development.
- This is a proof-of-concept project: Long-running web processes can be usefully managed by a celery worker queue.

To run
======

python longprocess.py runserver

To run tests
============

python longprocess.py test

