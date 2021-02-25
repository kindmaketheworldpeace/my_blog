# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0006_auto_20180412_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u5220\u9664'),
        ),
        migrations.AlterField(
            model_name='jobtask',
            name='step',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', '\u4efb\u52a1\u521d\u59cb\u5316'), (b'SSH_LOGIN', '\u767b\u5f55\u76ee\u6807\u4e3b\u673a'), (b'INSTALL_DEP', '\u5b89\u88c5\u57fa\u7840\u4f9d\u8d56'), (b'DOWNLOAD_FILE', '\u4e0b\u8f7d\u5b89\u88c5\u5305'), (b'UPLOAD_FILE', '\u4e0a\u4f20\u5b89\u88c5\u5305'), (b'EXECUTE_SCRIPT', '\u6267\u884c\u5b89\u88c5\u811a\u672c'), (b'SCRIPT_DONE', '\u5b89\u88c5\u811a\u672c\u6267\u884c\u5b8c\u6bd5'), (b'REGISTER_CMDB', '\u6ce8\u518c\u4e3b\u673a\u5230CMDB'), (b'WAIT_AGENT', '\u68c0\u6d4bAgent\u72b6\u6001\u548c\u7248\u672c'), (b'CREATE_JOB_SCRIPT', '\u51c6\u5907\u5b89\u88c5\u811a\u672c'), (b'CREATE_UNINSTALL_SCRIPT', '\u51c6\u5907\u5378\u8f7d\u811a\u672c'), (b'EXECUTE_JOB', '\u6267\u884c\u6279\u91cf\u5b89\u88c5\u4f5c\u4e1a'), (b'EXECUTE_UNINSTALL_JOB', '\u6267\u884c\u6279\u91cf\u5378\u8f7d\u4f5c\u4e1a'), (b'DETECT_WIN_ARC', '\u68c0\u6d4bWindows\u7cfb\u7edf\u7248\u672c'), (b'OVER_SUCCESS', '\u4efb\u52a1\u6267\u884c\u6210\u529f'), (b'OVER_FAILED', '\u4efb\u52a1\u6267\u884c\u5931\u8d25')]),
        ),
    ]
