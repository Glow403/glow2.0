from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


class UserProfile(models.Model):
    """用户扩展信息：欢乐豆"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    joy_dots = models.IntegerField(default=0, verbose_name='欢乐豆', validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '用户扩展'
        verbose_name_plural = '用户扩展'

    def __str__(self):
        return f"{self.user.username} - 欢乐豆: {self.joy_dots}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ServiceOrder(models.Model):
    """服务订单"""
    SERVICE_CHOICES = [
        ('brush_course', '刷课'),
        ('campus_run', '校园跑'),
        ('homework', '作业'),
        ('internship_proof', '实习证明'),
        ('thesis', '论文'),
        ('medical_record', '病历'),
        ('other', '其他'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name='服务项目')
    username = models.CharField(max_length=100, verbose_name='账号')
    password = models.CharField(max_length=100, verbose_name='密码')
    course_name = models.CharField(max_length=200, blank=True, default='', verbose_name='课程名称')
    times = models.IntegerField(blank=True, null=True, verbose_name='次数')
    distance = models.CharField(max_length=50, blank=True, default='', verbose_name='距离(KM)')
    remark = models.TextField(blank=True, default='', verbose_name='备注')
    cost = models.IntegerField(default=0, verbose_name='消耗欢乐豆', validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='提交时间')

    class Meta:
        verbose_name = '服务订单'
        verbose_name_plural = '服务订单'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_service_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"
