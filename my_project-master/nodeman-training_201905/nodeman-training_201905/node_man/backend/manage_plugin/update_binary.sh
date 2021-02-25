#!/bin/bash

usage () {
    echo "usage: update_binary OPTIONS"
    echo "OPTIONS"
    echo "  -t  plugin category, cloud be: official/external/scripts"
    echo "  -r  uninstall"
    echo "  -m  upgrade type: append or override"
    echo "  -n  plugin name"
    echo "  -f  package of plugin"
    echo "  -p  home path of plugin"
    #echo "  -v  plugin VERSION, for verification"

    exit 0
}

backup () {
    local backup_filename=${PLUGIN_NAME}-$(date +%Y%m%d%H%M%S).pz

    tar zcPf ${backup_filename} $BINDIR $ETCDIR
    mv ${backup_filename} ${GSE_HOME}
}

guess_target_dir () {
    case $CATEGORY in
        official | 1)
            export BINDIR=$GSE_HOME/plugins/bin
            export ETCDIR=$GSE_HOME/plugins/etc
            ;;
        external | 2)
            export BINDIR=$GSE_HOME/external_plugins/$PLUGIN_NAME/bin
            export ETCDIR=$GSE_HOME/external_plugins/$PLUGIN_NAME/etc
            ;;
        scripts | 3)
            export BINDIR=$GSE_HOME/external_scripts/
            export ETCDIR=$GSE_HOME/external_scripts/
            ;;
        *)
            echo "unkown category. abort"
            exit 1
            ;;
    esac
}

REMOVE=0
UPGRADE_TYPE=append
RESERVE_CONF=0
TMP=/tmp/

while getopts rut:T:n:m:f:z:v:p:h arg; do
    case $arg in
        T)  TIMEOUT=$OPTARG ;;
        t)  export CATEGORY=$OPTARG ;;
        r)  export REMOVE=1 ;;
        m)  export UPGRADE_TYPE=$OPTARG ;;
        n)  export PLUGIN_NAME=${OPTARG,,} ;;
        p)  export GSE_HOME=${OPTARG} ;;
        z)  export TMP=${OPTARG} ;;
        u)  export RESERVE_CONF=1 ;;
        #v)  export VERSION=$OPTARG ;;
        f)  export PACKAGE=$OPTARG ;;     # 官方插件/第三方插件有效
        *)  usage ;;
    esac
done

if [ "$REMOVE" == 1 ]; then
    cd $BINDIR/bin
    ./stop.sh ${PLUGIN_NAME} || { echo "stop plugin $PLUGIN_NAME failed"; exit 1; }

    rm -rf $BINDIR/bin/${PLUGIN_NAME} $ETCDIR/${PLUGIN_NAME}.conf
    exit $?
fi

guess_target_dir

backup $PLUGIN_NAME

if [ "${UPGRADE_TYPE^^}" != "APPEND" -a "${CATEGORY^^}" != "OFFICIAL" ]; then
    echo "removing plugin files"
    # 官方插件, 用覆盖的方式, 删掉所有目录, 默认情况下, 官方插件所有都在同一个包里.
    # 第三方插件, 删掉的是对应的插件目录.
    rm -rf ${BINDIR%/*}
fi

# 解压配置到目标路径
cd $TMP
echo "coming into:"
echo $TMP
tar xvf $PACKAGE -C $GSE_HOME; ret+=$?

# 恢复配置文件
if [ "$RESERVE_CONF" == 1 ]; then
    echo "recover config file"
    tar xPf $(ls -rt $GSE_HOME/${PLUGIN_NAME}-*.pz | tail -1) $ETCDIR
    ret+=$?
fi

# 输出看看更新后的信息. debug 时用.
ls -l $BINDIR/$PLUGIN_NAME $ETCDIR/${PLUGIN_NAME}.conf
cat $ETCDIR/${PLUGIN_NAME}.conf
exit $ret
