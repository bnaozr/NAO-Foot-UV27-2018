VnaoPath=`pwd`/
export LD_LIBRARY_PATH=${VnaoPath}/naoqi/lib:${VnaoPath}V-REP_PRO_EDU_V3_3_2_64_Linux
printenv | grep LD_LIBRARY_PATH
./V-REP_PRO_EDU_V3_3_2_64_Linux/vrepv1.sh &
