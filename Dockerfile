FROM missinglinkai/jenkins-k8s-slave:sdk

RUN python -m pip install nose fudge unittest2
RUN python3 -m pip install nose fudge unittest2