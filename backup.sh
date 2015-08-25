#!/bin/sh 
if [ $# -ne 3 ]; then
  echo "ERROR : MUST BE #./backup.sh hosts/xxxx  local_src_dir/  remote_dst_dir/";
  exit -1;
fi

REMOTE_HOSTS=$1; 
LOCAL_SRC=$2;
REMOTE_DST=$3;

DATE=`date "+%Y%m%d-%H%M%S"`;
TARGET_DIR=`basename $REMOTE_DST`;
BACKUP_DIR="/opt/backup/${TARGET_DIR}/${DATE}"
#mkdir -p ${BACKUP_DIR}

for host in `cat $REMOTE_HOSTS`; do
  echo $host;
  rsync -ab --backup-dir=$BACKUP_DIR  ${LOCAL_SRC}/ root@${host}:${REMOTE_DST};
  while [ 1 -eq 1 ]
  do
    read -p "y or n?" OPTION
    case "$OPTION" in
    y)
      echo "go on!"
      break
      ;;
    n)
      exit 1
      ;;
    *)
      continue
    esac
  done
done

echo '===================================chown aalog.dev DIR==================================='
echo '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
echo "./b_d.sh $1 \" chown -R aalog.dev $3 \""
