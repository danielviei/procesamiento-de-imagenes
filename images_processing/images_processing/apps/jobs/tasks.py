from celery import shared_task

@shared_task(name='images_processing.apps.jobs.taks.start_fsm')
def start_fsm(fsm_id):
    from .models import ImageTransformationFSM
    fsm = ImageTransformationFSM.objects.get(id=fsm_id)

    while int(fsm.state):
        if fsm.state == '1':
            fsm.invert_colors()
        elif fsm.state == '2':
            fsm.to_black_and_white()
        elif fsm.state == '3':
            fsm.rotate()
        elif fsm.state == '4':
            fsm.invert_vertically()
        elif fsm.state == '5':
            fsm.save_final_image()

    return "SUCCESS"
