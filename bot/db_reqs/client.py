from asgiref.sync import sync_to_async
from base_process import models as base_mdls


@sync_to_async
def get_about_us_info():
    about_us_info = base_mdls.AboutCompany.objects.values_list('name', 'description',
                                                               'image', 'address',
                                                               'work_days', 'work_time', 'phone',).first()
    return about_us_info
