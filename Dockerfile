FROM missinglinkai/frameworks:latest

RUN python -m pip install nose fudge unittest2
RUN python3 -m pip install nose fudge unittest2