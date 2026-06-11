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
            times_val = None
