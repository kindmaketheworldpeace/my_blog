# **Changlog**


# [Version: 1.0.81]
## Bug Fix
 - 修复升级问题

# [Version: 1.0.80]
## Bug Fix
 - 导入按钮文字修复


# [Version: 1.0.79]
## Feature
 - 支持导入功能

## Minor
 - 批量导入右侧提示弹框
 - 超时时间动态配置
 - 支持主机导入，提供模板下载


# [Version: 1.0.77]
## Bug Fix
 - 修复非 root 时, 安装脚本未 sudo 的问题


# [Version: 1.0.76]
## Bug Fix
 - 去除多余信息
 - 修复非 root 时, 安装脚本未 sudo 的问题
 - 用密钥批量安装pagent的时候密钥不正确问题修复


# [Version: 1.0.73]
## Minor
 - 当组件接口返回失败信息时记录整个请求响应的信息到日志


# [Version: 1.0.72]
## Minor：
 - 使用新命令获取windows版本
 - 当一台机器已安装在另一个业务下时，提示用户并不进行安装
 - 数据迁移后检查并确保主机所在业务的云区域存在


# [Version: 1.0.71]
## Minor：
 - 在aix和windows系统安装任务进行下载文件前，预先对本地文件做一次md5校验
 - 重构后端代码结构


# [Version: 1.0.70]
## BugFix：
 - P-agent密钥安装方式未传密钥问题
 - 数据迁移功能不稳定，导致迁移过来数据在节点管理中不显示问题


# [Version: 1.0.69]
## Minor：
 - 当一台机器在另一业务下已安装，再进行安装时进行提示
 - 批量终止任务时提醒用户哪些机器将要被终止


# [Version: 1.0.68]
## BugFix:
 - nginx端口号长度限制，并更新报错信息
 - 没有配置nginx server的外网ip时，安装proxy与PAgent的机器会卸载失败


# [Version: 1.0.67]
## BugFix:
 - 在windows机器上卸载agent时尝试使用'system'帐户，而不是'System'帐户来调作业平台
 - 更新状态的时候成功的时候没有加上问题处理
 - 修复send_cmd没有把真正的错误日志打印出来问题
 - 没有运行机器的时候不需要执行作业了
 - ip端口加正则
 - 删除record表中的多余记录信息
 - 记录历史数据
 - 安装Pagent获取脚本时使用nginx的inner_ip而不是outer_ip


# [Version: 1.0.66]
## BugFix:
 - windows运行job的用户名采用 administrator 和 system试错卸载
 - 批量安装机器的时候，轮询状态的时候改为根据每一个机器来轮询
 - proxy connection refused的异常处理
 - 在CMDB删除机器再卸载的时候，错误日志没有展示出来问题修复


# [Version: 1.0.65]
## BugFix:
 - 编辑的时候提示不存在agent，无法进行批量操作
 - nginx连接不上时，没有及时报错，还继续进行安装

# [Version: 2.0.10]

## Bugfix
 - 对象引用错误导致分拆参数失败


# [Version: 2.0.8]
## Feature
 - 新增拆分任务接口

## Bugfix
 - 插件初始化接口更新插件安装信息时唯一性选择未包含操作系统信息


# [Version: 2.0.7]
## Bugfix
 - 新增插件接口返回字段从messages改为message

# [Version: 2.0.6]
## Feature
 - 节点管理接口接入esb 依赖esb版本: ee_2.6.13

## Bugfix
 - 接口返回结果错误


# [Version: 2.0.5]
## Feature
 - 新增cmdb接口支持 通过插件查询机器信息
 - 新增插件更新接口
 - 新增从nginx服务拉取配置文件初始化信息流程

## Minor
 - 任务信息新增错误码描述
 - 调整插件表表名

# [Version: 2.0.3]
## Bugfix
 - #184
 - #185
 - #187
 - #188
 - #189
 - #190
 - #191

# [Version: 2.0.2]
## Bugfix
 - 机器状态支持条件查询
 - 机器支持多ip精确过滤

# [Version: 2.0.1]
## Feature
 - 新增插件管理功能 可通过界面对机器插件进行操作和更新
 - 新增任务查看界面 可查看任务运行日志

