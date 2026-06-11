import os

path = r"C:\Users\86153\Desktop\codex项目\网站3.0\main\views.py"

with open(path, "rb") as f:
    raw = f.read()

if raw.startswith(b"\xef\xbb\xbf"):
    raw = raw[3:]

text = raw.decode("utf-8")

# Find the times validation block
old_block = """        # 对于需要次数的服务，校验次数必须为正整数
        if is_scale:
            times_str = request.POST.get('times', '').strip()
            try:
                times_val = int(times_str)
                if times_val <= 0:
                    messages.error(request, '次数必须为正整数')
                    return render(request, 'main/service_detail.html', {
                        'title': service_name,
                        'service_type': service_type,
                        'service_name': service_name,
                        'cost': base_cost,
                        'base_cost': base_cost,
                        'is_scale': is_scale,
                        'fields': fields,
                        'joy_dots': request.user.profile.joy_dots,
                    })
            except (ValueError, TypeError):
                messages.error(request, '次数必须为正整数')
                return render(request, 'main/service_detail.html', {
                    'title': service_name,
                    'service_type': service_type,
                    'service_name': service_name,
                    'cost': base_cost,
                    'base_cost': base_cost,
                    'is_scale': is_scale,
                    'fields': fields,
                    'joy_dots': request.user.profile.joy_dots,
                })
        else:
            times_val = None"""

new_block = """        # 对于需要次数的服务，校验次数必须为正整数
        if is_scale:
            times_str = request.POST.get('times', '').strip()
            if not times_str:
                times_val = 1
            else:
                try:
                    times_val = int(times_str)
                    if times_val <= 0:
                        messages.error(request, '次数必须为正整数')
                        return render(request, 'main/service_detail.html', {
                            'title': service_name,
                            'service_type': service_type,
                            'service_name': service_name,
                            'cost': base_cost,
                            'base_cost': base_cost,
                            'is_scale': is_scale,
                            'fields': fields,
                            'joy_dots': request.user.profile.joy_dots,
                        })
                except (ValueError, TypeError):
                    messages.error(request, '次数必须为正整数')
                    return render(request, 'main/service_detail.html', {
                        'title': service_name,
                        'service_type': service_type,
                        'service_name': service_name,
                        'cost': base_cost,
                        'base_cost': base_cost,
                        'is_scale': is_scale,
                        'fields': fields,
                        'joy_dots': request.user.profile.joy_dots,
                    })
        else:
            times_val = None"""

if old_block not in text:
    print("WARNING: old_block not found!")
    exit()

new_text = text.replace(old_block, new_block, 1)

with open(path, "wb") as f:
    f.write(new_text.encode("utf-8"))

print("Fixed times validation bug")
