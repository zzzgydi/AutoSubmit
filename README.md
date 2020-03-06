# 自动打卡

只是为了华工同学方便打卡，不作其他用途。

### SMTP 邮件通知

新增了邮件通知，需要自行填写对应的 SMTP 服务域名，账号密码等。

### 执行环境

- python3
- nodejs

### 使用

```python
python main.py
```

### 其他

在 linux 上开启定时任务：使用`crontab -e`编辑任务

比如我的任务为每天早上 9 点半进行自动打卡

```text
30 9 * * * python3 main.py >> log
```

### 注意

设置任务时需要注意路径。

1. 当出现找不到 node 时，可以将`autoSubmit.py`的代码`cmds = ['node', './script/main.js', rsa]`中的 node 改为系统中 node 的绝对路径，比如`/usr/local/bin/node`。
