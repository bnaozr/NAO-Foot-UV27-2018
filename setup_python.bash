VnaoPath=`pwd`/
if [ -z ${PYTHONPATH+x} ]
then
    #echo "PYTHONPATH is unset"
    export PYTHONPATH=${VnaoPath}/pynaoqi-python-2.7-naoqi-1.14-linux64/
else
    #echo "PYTHONPATH is set to '$PYTHONPATH'"
    export PYTHONPATH=${PYTHONPATH}:${VnaoPath}/pynaoqi-python-2.7-naoqi-1.14-linux64/
fi
