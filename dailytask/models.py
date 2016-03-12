from django.db import models

class Task(models.Model):
    """
    任务类
    """
    content = models.CharField(max_length=255) # 任务内容
    parent = models.IntegerField(default=0) # 父任务id，默认为0
    create_date = models.DateTimeField(auto_now_add=True) # 任务创建时间
    done_date = models.DateTimeField(null=True) # 任务完成时间
    have_completed = models.BooleanField(default=False) # 是否已经完成
    
    def __str__(self):
        return self.content