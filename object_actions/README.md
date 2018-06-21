Object Actions
=====================

If you've ever tried making your own admin object tools and you were
like me, you immediately gave up. Why can't they be as easy as making
Django Admin Actions? Well now they can be.


Quick-Start Guide
-----------------

In your admin.py::

    from object_actions import BaayObjectActions


    class ArticleAdmin(BaayObjectActions, admin.ModelAdmin):
        def publish_this(self, request, obj):
            publish_obj(obj)
        publish_this.label = "Publish"  # optional
        publish_this.short_description = "Submit this article"  # optional

        change_actions = ('publish_this', )


Usage
-----

Defining new tool actions are just like defining regular `admin actions
<https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/>`_. The major
difference is the action functions for you write for the change view will take
an object instance instead of a queryset (see *Re-using Admin Actions* below).

Tool actions are exposed by putting them in a ``change_actions`` attribute in
your model admin. You can also add tool actions to the changelist views too.
You'll get a queryset like a regular admin action::

    from object_actions import BaayObjectActions

    class MyModelAdmin(BaayObjectActions, admin.ModelAdmin):
        def toolfunc(self, request, obj):
            pass
        toolfunc.label = "This will be the label of the button"  # optional
        toolfunc.short_description = "This will be the tooltip of the button"  # optional

        def make_published(modeladmin, request, queryset):
            queryset.update(status='p')

        change_actions = ('toolfunc', )
        changelist_actions = ('make_published', )

Just like admin actions, you can send a message with ``self.message_user``.
Normally, you would do something to the object and go back to the same
place, but if you return a HttpResponse, it will follow it (hey, just
like admin actions!).

If your admin modifies ``get_urls``, ``change_view``, or ``changelist_view``,
you'll need to take extra care.

Re-using Admin Actions
``````````````````````

If you would like a preexisting admin action to also be an change action, add
the ``takes_instance_or_queryset`` decorator like::


    from object_actions import (BaayObjectActions,
            takes_instance_or_queryset)

    class RobotAdmin(BaayObjectActions, admin.ModelAdmin):
        # ... snip ...

        @takes_instance_or_queryset
        def tighten_lug_nuts(self, request, queryset):
            queryset.update(lugnuts=F('lugnuts') - 1)

        change_actions = ['tighten_lug_nuts']
        actions = ['tighten_lug_nuts']

Customizing Admin Actions
`````````````````````````

To give the action some a helpful title tooltip, add a ``short_description``
attribute, similar to how admin actions work::

    def increment_vote(self, request, obj):
        obj.votes = obj.votes + 1
        obj.save()
    increment_vote.short_description = "Increment the vote count by one"

By default, Object Actions will guess what to label the button based on
the name of the function. You can override this with a ``label`` attribute::

    def increment_vote(self, request, obj):
        obj.votes = obj.votes + 1
        obj.save()
    increment_vote.label = "Vote++"

If you need even more control, you can add arbitrary attributes to the buttons
by adding a Django widget style `attrs` attribute::

    def increment_vote(self, request, obj):
        obj.votes = obj.votes + 1
        obj.save()
    increment_vote.attrs = {
        'class': 'addlink',
    }

Programmatically Disabling Actions
``````````````````````````````````

You can programmatically disable registered actions by defining your own custom
``get_change_actions()`` method. In this example, certain actions only apply to
certain object states (i.e. You should not be able to close an company account
if the account is already closed)::

    def get_change_actions(self, request, object_id, form_url):
        actions = super(PollAdmin, self).get_change_actions(request, object_id, form_url)
        actions = list(actions)
        if not request.user.is_superuser:
            return []

        obj = self.model.objects.get(pk=object_id)
        if obj.question.endswith('?'):
            actions.remove('question_mark')

        return actions
