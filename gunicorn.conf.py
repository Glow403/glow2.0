import os
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
workers = 2
threads = 4
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'