import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'main/templates/main/base.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the footer with a conditional: hide on login page
old_footer = """<footer class="footer">
<div> 2026 校园服务网 All Rights Reserved</div>
<div class="contact">客服联系方式：<span>v：asdf675400</span></div>
</footer>"""

new_footer = """{% if request.resolver_match.url_name != 'login' and request.resolver_match.url_name != 'register' %}
<footer class="footer">
<div> 2026 校园服务网 All Rights Reserved</div>
<div class="contact">客服联系方式：<span>v：asdf675400</span></div>
</footer>
{% endif %}"""

if old_footer in content:
    content = content.replace(old_footer, new_footer)
    print("SUCCESS: footer now conditionally hidden on login/register pages")
else:
    print("ERROR: footer not found")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
