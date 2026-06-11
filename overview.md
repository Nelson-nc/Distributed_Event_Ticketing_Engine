# Overview

a ticketing system API
- view all event in 'api/events'

- reserve ticket in 'api/events/\<eventID>/reserve'

- and fake payment in 'api/payments/webhook/' which the event/ticket detail is passed in the body and the status is updated.

<br/>

---

<br/>

cool/new features i just learned are atomic transaction, auto delete and queuing, etc.
- __django.db.transaction.atomic()__: for every db related code in a 
function decorated by it or context, if one should fail all fails. just to be safe

- __Model.objects.select_for_update().get(id=id)__ the name implies what it does select it for updating, combine it with atomic for the best result.

- __task.py__: for creating task, don't know to what extent i can be used/useful but i am using it to auto delete ticket that haven't been paid for.

- __logger__ = logging.getLogger(\_\_name__) for logging, its new because its shorter than what i usually do.

- __celery.shared_task__: @shared_task used for creating tasks that'll work for any app environment.

- __clean_expired_reservations()__: it get all reserved ticket that have not been paid for since the past 5 min and delete them and also increment the available_ticket for the event.

- __celery.py__: to setup python celery and django. the steps are quite easy
    - we set up our default django settings (settings.py)
    - next create a Celery app
        - main ('ticketing_system') which is sort of like a name
        - broker and backend which are your db (i use redis by the way)
    - get all config that start with the namespace 'CELERY' from our default settings
    - the set it to automatically discover the CELERY settings

- CELERY_BROKEN_URL & CELERY_RESULT_BACKEND: our redis db