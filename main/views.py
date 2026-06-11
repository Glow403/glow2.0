from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST
from .models import ServiceOrder
from django.contrib.auth.models import User

# 各服务基础消耗欢乐豆（单次）
SERVICE_COST = {
    'brush_course': 4,
    'campus_run': 2,
    'homework': 2,
    'internship_proof': 0,
    'thesis': 0,
    'medical_record': 0,
    'other': 0,
}

# 各服务所需字段
SERVICE_FIELDS = {
    'brush_course': [
        {'key': 'username', 'label': '账号', 'type': 'text'},
        {'key': 'password', 'label': '密码', 'type': 'password'},
        {'key': 'course_name', 'label': '课程名称', 'type': 'text'},
        {'key': 'remark', 'label': '备注', 'type': 'textarea'},
    ],
    'campus_run': [
        {'key': 'username', 'label': '账号', 'type': 'text'},
        {'key': 'password', 'label': '密码', 'type': 'password'},
        {'key': 'times', 'label': '次数', 'type': 'number'},
        {'key': 'distance', 'label': '一次多少KM', 'type': 'text'},
        {'key': 'remark', 'label': '备注', 'type': 'textarea'},
    ],
    'homework': [
        {'key': 'username', 'label': '账号', 'type': 'text'},
        {'key': 'password', 'label': '密码', 'type': 'password'},
        {'key': 'course_name', 'label': '课程名称', 'type': 'text'},
        {'key': 'remark', 'label': '备注（除选择填空外需联系客服）', 'type': 'textarea'},
    ],
    'default': [
        {'key': 'username', 'label': '你的联系', 'type': 'text'},
        {'key': 'remark', 'label': '备注', 'type': 'textarea'},
    ],
}

# 可按次数倍增消耗的服务类型
SCALE_BY_TIMES = ['campus_run', 'brush_course', 'homework']


def get_service_config(service_type):
    """获取服务表单配置"""
    return SERVICE_FIELDS.get(service_type, SERVICE_FIELDS['default'])


def calculate_cost(service_type, times):
    """根据服务类型和次数计算消耗欢乐豆"""
    try:
        times_val = int(times)
    except (TypeError, ValueError):
        return 0
    if service_type in SCALE_BY_TIMES and times_val > 0:
        return SERVICE_COST.get(service_type, 0) * times_val
    return SERVICE_COST.get(service_type, 0)


def validate_required_fields(fields, post_data):
    """校验必填字段是否为空"""
    for field in fields:
        value = post_data.get(field['key'], '').strip()
        if not value:
            return False, field['label']
    return True, None


def index(request):
    """首页：未登录显示登录注册页"""
    if request.user.is_authenticated:
        return redirect('main:services')
    return render(request, 'main/login.html', {
        'title': '登录 / 注册',
    })


def user_login(request):
    """登录处理"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, '账号和密码不能为空')
            return render(request, 'main/login.html', {'title': '登录'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('main:services')
        else:
            messages.error(request, '账号或密码错误')
    return render(request, 'main/login.html', {'title': '登录'})


def user_register(request):
    """注册处理"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, '账号和密码不能为空')
            return render(request, 'main/login.html', {'title': '注册', 'register_mode': True})

        if password != confirm_password:
            messages.error(request, '两次密码输入不一致')
            return render(request, 'main/login.html', {'title': '注册', 'register_mode': True})

        if len(password) < 6:
            messages.error(request, '密码长度不能少于6位')
            return render(request, 'main/login.html', {'title': '注册', 'register_mode': True})

        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, '该账号已存在')
            return render(request, 'main/login.html', {'title': '注册', 'register_mode': True})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, '注册成功！')
        return redirect('main:services')

    return render(request, 'main/login.html', {'title': '注册', 'register_mode': True})


@login_required
def user_logout_view(request):
    logout(request)
    messages.success(request, '已退出登录')
    return redirect('main:index')


@login_required
def services(request):
    """首页：登录后看到服务项目列表"""
    user = request.user
    user_profile = user.profile
    recent_orders = ServiceOrder.objects.filter(user=user)[:5]
    return render(request, 'main/services.html', {
        'title': '服务项目',
        'joy_dots': user_profile.joy_dots,
        'recent_orders': recent_orders,
    })


@login_required
def service_page(request, service_type):
    """????"""
    # ????? profile?????????? AttributeError?
    if request.user.is_authenticated:
        if not hasattr(request.user, "profile"):
            from .models import UserProfile
            UserProfile.objects.get_or_create(user=request.user)

    from .models import ServiceOrder

    """各业务页面"""
    service_names = {
        'brush_course': '刷课',
        'campus_run': '校园跑',
        'homework': '作业',
        'internship_proof': '实习证明',
        'thesis': '论文',
        'medical_record': '病历',
        'other': '其他',
    }

    if service_type not in service_names:
        messages.error(request, '无效的服务类型')
        return redirect('main:services')

    service_name = service_names[service_type]
    fields = get_service_config(service_type)
    base_cost = SERVICE_COST.get(service_type, 0)
    is_scale = service_type in SCALE_BY_TIMES

    if request.method == 'POST':
        # 校验必填字段
        valid, field_name = validate_required_fields(fields, request.POST)
        if not valid:
            messages.error(request, f'请填写"{field_name}"')
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

        # 对于需要次数的服务，校验次数必须为正整数
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
            times_val = None

        # 收集表单数据
        order_data = {}
        for field in fields:
            order_data[field['key']] = request.POST.get(field['key'], '').strip()

        # 计算实际消耗
        cost = calculate_cost(service_type, times_val)

        # 使用事务保证原子性：扣款 + 创建订单
        with transaction.atomic():
            # 重新读取最新余额，防止并发超扣
            profile, _ = request.user.profile.__class__.objects.select_for_update().get_or_create(user=request.user)
            if cost > 0 and profile.joy_dots < cost:
                messages.error(request, f'欢乐豆不足！需要 {cost} 个欢乐豆，当前余额 {profile.joy_dots}')
                return render(request, 'main/service_detail.html', {
                    'title': service_name,
                    'service_type': service_type,
                    'service_name': service_name,
                    'cost': base_cost,
                    'base_cost': base_cost,
                    'is_scale': is_scale,
                    'fields': fields,
                    'joy_dots': profile.joy_dots,
                })

            # 扣除欢乐豆
            if cost > 0:
                profile.joy_dots -= cost
                profile.save(update_fields=['joy_dots'])

            # 创建订单
            ServiceOrder.objects.create(
                user=request.user,
                service_type=service_type,
                cost=cost,
                **order_data,
            )

        messages.success(request, f'提交成功！本次消耗 {cost} 个欢乐豆')
        return redirect('main:services')

    # 计算显示消耗的欢乐豆（GET请求时基于 times 参数）
    show_times = request.GET.get('times', '')
    display_cost = calculate_cost(service_type, show_times) if (is_scale and show_times) else base_cost

    return render(request, 'main/service_detail.html', {
        'title': service_name,
        'service_type': service_type,
        'service_name': service_name,
        'cost': display_cost,
        'base_cost': base_cost,
        'is_scale': is_scale,
        'fields': fields,
        'joy_dots': request.user.profile.joy_dots,
    })


@login_required
def my_orders(request):
    """我的订单"""
    orders = ServiceOrder.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'main/my_orders.html', {
        'title': '我的订单',
        'orders': orders,
    })


def create_first_admin(request):
    """??????????????????"""
    from django.contrib.auth.models import User
    try:
        admin = User.objects.get(username='admin')
        return render(request, 'main/base.html', {'title': '??????'})
    except User.DoesNotExist:
        admin = User.objects.create_superuser(
            username='admin',
            email='',
            password='admin123',
        )
        return render(request, 'main/base.html', {
            'title': '????',
            'message': f'????????????: admin, ??: admin123',
        })
