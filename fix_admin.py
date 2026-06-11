path = r"C:\Users\86153\Desktop\codex项目\网站3.0\main\views.py"
with open(path, "rb") as f:
    raw = f.read()
if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]
text = raw.decode("utf-8")
old_start = text.find("def create_first_admin(request):")
if old_start < 0:
    print("Not found")
    exit()
new_func = "def create_first_admin(request):\n"
new_func += '    """\u521d\u59cb\u5316\u7b2c\u4e00\u4e2a\u7ba1\u7406\u5458\u8d26\u53f7\uff08\u4ec5\u9996\u6b21\u8bbf\u95ee\u65f6\u4f7f\u7528\uff09"""\n'
new_func += "    from django.contrib.auth.models import User\n"
new_func += "    try:\n"
new_func += "        admin = User.objects.get(username='admin')\n"
new_func += '        return HttpResponse(\n'
new_func += '            \x27\u7ba1\u7406\u5458\u5df2\u5b58\u5728\uff0c<a href="/admin/">\u524d\u5f80\u540e\u53f0</a>\x27,\n'
new_func += "            content_type='text/html'\n"
new_func += "        )\n"
new_func += "    except User.DoesNotExist:\n"
new_func += "        User.objects.create_superuser(username='admin', email='', password='admin123')\n"
new_func += "        return HttpResponse(\n"
new_func += '            \x27\u7ba1\u7406\u5458\u521b\u5efa\u6210\u529f\uff01\u7528\u6237\u540d: <b>admin</b> \u5bc6\u7801: <b>admin123</b><br><a href="/admin/">\u524d\u5f80\u540e\u53f0</a>\x27,\n'
new_func += "            content_type='text/html'\n"
new_func += "        )\n"
new_text = text[:old_start] + new_func
with open(path, "wb") as f:
    f.write(new_text.encode("utf-8"))
print("Done")
