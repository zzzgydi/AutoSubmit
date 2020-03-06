# 自动打卡

只是为了华工同学方便打卡，不作其他用途。

### SMTP

新增了邮件通知

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
30 9 * * * python3 main.py
```
