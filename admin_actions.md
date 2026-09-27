# Django Admin Actions — Complete Guide

## 1. What is a Django Admin Action?

A Django Admin Action allows you to perform an operation on **multiple selected database objects at once**.

For example, in the Django Admin you could select:

```text
☑ Order 1
☑ Order 2
☑ Order 3
```

Then choose:

```text
--------- ACTIONS ---------
Mark selected orders as shipped
```

Django calls your action function.

The basic structure is:

```python
def order_shipped_action(modeladmin, request, queryset):
    pass
```

The three arguments are:

```text
modeladmin
    ↓
The ModelAdmin object

request
    ↓
The current HTTP request

queryset
    ↓
The objects selected by the administrator
```

---

# 2. The Three Parameters

## A. `modeladmin`

```python
def order_shipped_action(modeladmin, request, queryset):
```

`modeladmin` is the **ModelAdmin instance associated with the model**.

For example:

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [order_shipped_action]
```

When the action runs, Django passes this `OrderAdmin` object as:

```python
modeladmin
```

Therefore:

```python
modeladmin
```

represents:

```text
OrderAdmin
```

---

# 3. Useful `modeladmin` Methods

Because `modeladmin` is a `ModelAdmin` object, you can access many ModelAdmin methods.

## `modeladmin.get_queryset(request)`

Gets the queryset that the ModelAdmin normally uses.

```python
queryset = modeladmin.get_queryset(request)
```

Example:

```python
def my_action(modeladmin, request, queryset):

    all_orders = modeladmin.get_queryset(request)

    print(all_orders)
```

Important:

```python
queryset
```

is the objects selected by the administrator.

While:

```python
modeladmin.get_queryset(request)
```

is the queryset defined/filtered by the ModelAdmin.

---

# 4. `modeladmin.message_user()`

This is one of the most useful methods in Admin actions.

It displays a message to the administrator.

```python
modeladmin.message_user(
    request,
    "Orders have been shipped successfully."
)
```

For example:

```python
def order_shipped_action(modeladmin, request, queryset):

    queryset.update(status="Shipped")

    modeladmin.message_user(
        request,
        "Selected orders have been shipped."
    )
```

The message appears in Django Admin.

---

## Message levels

You can specify the message level:

```python
from django.contrib import messages
```

Then:

```python
modeladmin.message_user(
    request,
    "Orders shipped successfully.",
    level=messages.SUCCESS
)
```

Other levels include:

```python
messages.DEBUG
messages.INFO
messages.SUCCESS
messages.WARNING
messages.ERROR
```

Example:

```python
modeladmin.message_user(
    request,
    "You do not have permission.",
    level=messages.ERROR
)
```

---

# 5. `modeladmin.has_change_permission()`

Checks whether the current user has permission to change objects.

```python
modeladmin.has_change_permission(request)
```

You can also check a specific object:

```python
modeladmin.has_change_permission(
    request,
    obj=order
)
```

Example:

```python
def order_shipped_action(modeladmin, request, queryset):

    if not modeladmin.has_change_permission(request):
        modeladmin.message_user(
            request,
            "You do not have permission.",
            level=messages.ERROR
        )
        return

    queryset.update(status="Shipped")
```

---

# 6. Other Permission Methods on `modeladmin`

Useful ModelAdmin permission methods include:

```python
modeladmin.has_view_permission(request)
modeladmin.has_add_permission(request)
modeladmin.has_change_permission(request)
modeladmin.has_delete_permission(request)
```

Meaning:

```text
has_view_permission()
    ↓
Can the user view?

has_add_permission()
    ↓
Can the user add?

has_change_permission()
    ↓
Can the user change?

has_delete_permission()
    ↓
Can the user delete?
```

---

# 7. `modeladmin.get_object()`

You can retrieve an object by its primary key.

Conceptually:

```python
obj = modeladmin.get_object(request, object_id)
```

Example:

```python
order = modeladmin.get_object(request, "5")
```

This is useful when working with a particular Admin object.

---

# 8. `modeladmin.get_urls()`

This allows you to add custom URLs to your ModelAdmin.

Example:

```python
class OrderAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()

        # custom URLs here

        return urls
```

This is more advanced than normal actions, but it is useful when building custom Admin functionality.

---

# 9. `modeladmin.model`

You can access the model associated with the ModelAdmin:

```python
modeladmin.model
```

For example:

```python
print(modeladmin.model)
```

could give:

```text
<class 'core.models.Order'>
```

---

# 10. `modeladmin.opts`

Provides model metadata/options.

```python
modeladmin.opts
```

For example:

```python
modeladmin.opts.model_name
```

can give:

```text
order
```

---

# 11. `modeladmin.admin_site`

Provides access to the AdminSite.

```python
modeladmin.admin_site
```

This is useful for more advanced Admin customization.

---

# 12. `request`

The second argument is:

```python
request
```

This is Django's normal HTTP request object.

It contains information about the current request.

Most importantly for Admin actions:

```python
request.user
```

---

# 13. `request.user`

This tells you **which user is performing the Admin action**.

Example:

```python
def order_shipped_action(modeladmin, request, queryset):

    print(request.user)
```

If the logged-in Admin user is:

```text
nzegge
```

then:

```python
request.user
```

represents that user.

---

# 14. Working With `request.user`

You can check whether the user is authenticated:

```python
request.user.is_authenticated
```

Check whether they are staff:

```python
request.user.is_staff
```

Check whether they are a superuser:

```python
request.user.is_superuser
```

Check whether they are active:

```python
request.user.is_active
```

Example:

```python
if request.user.is_superuser:
    print("Superuser is performing the action")
```

---

# 15. User Permissions

You can check a specific permission:

```python
request.user.has_perm("core.change_order")
```

The format is:

```text
app_label.permission_codename
```

For example:

```python
request.user.has_perm("core.change_order")
```

means:

```text
Can this user change Order objects?
```

Other examples:

```python
request.user.has_perm("core.add_order")
request.user.has_perm("core.delete_order")
request.user.has_perm("core.view_order")
```

---

# 16. User Groups

You can inspect the groups belonging to the Admin user:

```python
request.user.groups.all()
```

Example:

```python
groups = request.user.groups.all()

for group in groups:
    print(group.name)
```

You can check whether the user belongs to a particular group:

```python
request.user.groups.filter(name="Managers").exists()
```

---

# 17. User's Email

Because `request.user` is your User object, you can access:

```python
request.user.email
```

Example:

```python
print(request.user.email)
```

This is the email of the **administrator performing the action**.

Do not confuse this with:

```python
order.user.email
```

which is the email of the **customer who owns the order**.

This distinction is extremely important.

```text
request.user
    ↓
Administrator performing the action


order.user
    ↓
Customer who owns the order
```

---

# 18. `request.method`

You can check the HTTP method:

```python
request.method
```

Examples:

```text
GET
POST
PUT
PATCH
DELETE
```

Admin actions are normally triggered through a:

```text
POST
```

request.

---

# 19. `request.POST`

Contains POST data.

```python
request.POST
```

For example:

```python
status = request.POST.get("status")
```

This becomes useful when creating custom Admin forms or custom Admin actions.

---

# 20. `request.GET`

Contains query parameters.

Example URL:

```text
/admin/core/order/?status=pending
```

You can access:

```python
status = request.GET.get("status")
```

Result:

```text
pending
```

---

# 21. `request.FILES`

Contains uploaded files.

```python
request.FILES
```

This becomes useful when your Admin customization includes file uploads.

---

# 22. `request.path`

Gets the current URL path:

```python
request.path
```

Example:

```text
/admin/core/order/
```

---

# 23. `request.session`

Provides access to the user's session:

```python
request.session
```

For example:

```python
request.session["something"] = "value"
```

---

# 24. `request.META`

Contains HTTP request metadata:

```python
request.META
```

For example, the user agent:

```python
request.META.get("HTTP_USER_AGENT")
```

---

# 25. `queryset`

This is the third and probably most important argument.

```python
def order_shipped_action(modeladmin, request, queryset):
```

`queryset` contains the **objects selected in Django Admin**.

Suppose Admin displays:

```text
☑ Order 1
☑ Order 2
☐ Order 3
☑ Order 4
```

Then:

```python
queryset
```

contains:

```text
Order 1
Order 2
Order 4
```

It does NOT contain Order 3.

---

# 26. `queryset.count()`

Counts the selected objects:

```python
count = queryset.count()
```

Example:

```python
def order_shipped_action(modeladmin, request, queryset):

    count = queryset.count()

    modeladmin.message_user(
        request,
        f"{count} orders selected."
    )
```

---

# 27. Loop Through the QuerySet

You can iterate through selected objects:

```python
for order in queryset:
    print(order)
```

Example:

```python
def order_shipped_action(modeladmin, request, queryset):

    for order in queryset:
        order.status = "Shipped"
        order.save()
```

This saves each object individually.

---

# 28. `queryset.update()`

If you want to update many objects at once:

```python
queryset.update(status="Shipped")
```

Example:

```python
def order_shipped_action(modeladmin, request, queryset):

    queryset.update(status="Shipped")
```

This is usually more efficient than:

```python
for order in queryset:
    order.status = "Shipped"
    order.save()
```

---

# 29. Important Difference: `update()` vs `save()`

This is extremely important when learning Admin actions.

### Individual save

```python
for order in queryset:
    order.status = "Shipped"
    order.save()
```

You are working with each object individually.

### QuerySet update

```python
queryset.update(status="Shipped")
```

Django sends one database update operation for the matching rows.

Also remember:

```python
queryset.update()
```

does **not** call each model's `save()` method.

Therefore, you should not assume model `save()` logic or `pre_save`/`post_save` behavior will run for every object as it would with individual `save()` calls.

---

# 30. `queryset.filter()`

You can filter the selected objects further:

```python
shipped_orders = queryset.filter(status="Shipped")
```

Example:

```python
pending_orders = queryset.filter(status="Pending")
```

---

# 31. `queryset.exclude()`

Exclude records:

```python
queryset.exclude(status="Cancelled")
```

Example:

```python
orders = queryset.exclude(status="Cancelled")
```

---

# 32. `queryset.exists()`

Check whether at least one object exists:

```python
if queryset.exists():
    print("There are selected orders")
```

This is often better than:

```python
if queryset.count() > 0:
```

when you only need to know whether something exists.

---

# 33. `queryset.first()`

Gets the first object:

```python
order = queryset.first()
```

If there are no objects:

```python
order is None
```

---

# 34. `queryset.last()`

Gets the last object:

```python
order = queryset.last()
```

---

# 35. `queryset.delete()`

Deletes the selected objects:

```python
queryset.delete()
```

Be very careful with this in Admin actions.

Example:

```python
def delete_orders(modeladmin, request, queryset):
    queryset.delete()
```

This permanently deletes the selected records.

---

# 36. `queryset.values()`

Gets dictionary-like data:

```python
queryset.values("id", "status")
```

Example:

```python
orders = queryset.values(
    "id",
    "status"
)

for order in orders:
    print(order)
```

Possible result:

```python
{
    "id": 1,
    "status": "Pending"
}
```

---

# 37. `queryset.values_list()`

Gets tuples or individual values.

```python
queryset.values_list("id", "status")
```

Example:

```python
for order_id, status in queryset.values_list(
    "id",
    "status"
):
    print(order_id, status)
```

---

# 38. `queryset.order_by()`

Sort the selected objects:

```python
queryset.order_by("-created_at")
```

Example:

```python
orders = queryset.order_by("-created_at")
```

`-` means descending.

Without `-`:

```python
queryset.order_by("created_at")
```

means ascending.

---

# 39. `queryset.select_related()`

Useful when working with ForeignKey/OneToOne relationships.

Suppose:

```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Instead of repeatedly loading:

```python
order.user
```

you can use:

```python
queryset.select_related("user")
```

Example:

```python
queryset = queryset.select_related("user")
```

---

# 40. `queryset.prefetch_related()`

Useful for reverse relationships and ManyToMany relationships.

Example:

```python
queryset.prefetch_related("items")
```

This can reduce unnecessary database queries.

---

# 41. Working With Users in an Order Action

Suppose:

```python
class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50)
```

You can write:

```python
def order_shipped_action(modeladmin, request, queryset):

    for order in queryset:

        user = order.user

        print(user.username)
        print(user.email)

        order.status = "Shipped"
        order.save()
```

Notice the two users:

```text
request.user
    ↓
Admin user performing the action


order.user
    ↓
Customer belonging to this order
```

---

# 42. Sending Email From an Action

For your current project, you might have:

```python
def order_shipped_action(modeladmin, request, queryset):

    for order in queryset:

        user = order.user

        user.email_user(
            subject="Your order has been shipped",
            message=(
                f"Your order {order.id} "
                f"has been shipped."
            ),
            from_email="admin@django.com",
            fail_silently=False,
        )

        order.status = "Shipped"
        order.save()
```

Notice:

```python
user.email_user(...)
```

does NOT need:

```python
recipient_list=[user.email]
```

because `email_user()` already knows the recipient.

---

# 43. Complete Professional Example

```python
from django.contrib import admin, messages


@admin.action(description="Mark selected orders as shipped")
def order_shipped_action(modeladmin, request, queryset):

    count = queryset.count()

    for order in queryset:

        # Customer who owns the order
        user = order.user

        # Change order status
        order.status = "Shipped"
        order.save()

        # Send email to customer
        user.email_user(
            subject="Your order has been shipped",
            message=(
                f"Hello {user.username},\n\n"
                f"Your order {order.id} "
                f"has been shipped."
            ),
            from_email="admin@django.com",
            fail_silently=False,
        )

    # Message to administrator
    modeladmin.message_user(
        request,
        f"{count} orders were shipped successfully.",
        level=messages.SUCCESS,
    )
```

Then:

```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    actions = [
        order_shipped_action
    ]
```

---

# 44. `@admin.action`

Modern Django provides:

```python
@admin.action(description="Mark selected orders as shipped")
```

Instead of:

```python
def order_shipped_action(modeladmin, request, queryset):
    ...
```

You still have exactly the same three arguments.

The decorator mainly gives Django metadata about the action.

---

# 45. Action With Permission

You can restrict an action based on permission.

Example:

```python
@admin.action(
    permissions=["change"],
    description="Mark selected orders as shipped"
)
def order_shipped_action(modeladmin, request, queryset):

    queryset.update(status="Shipped")
```

This means the action requires the appropriate change permission.

You can also use:

```python
permissions=["delete"]
```

or:

```python
permissions=["view"]
```

---

# 46. `has_<permission>_permission`

For more customized permission logic, ModelAdmin supports methods such as:

```python
def has_change_permission(self, request, obj=None):
    ...
```

Example:

```python
class OrderAdmin(admin.ModelAdmin):

    def has_change_permission(
        self,
        request,
        obj=None
    ):
        return request.user.is_superuser
```

Now only superusers can change orders through this ModelAdmin.

---

# 47. Action Permission vs User Permission

These are related but different.

### User permission

```python
request.user.has_perm("core.change_order")
```

asks:

> Does this particular user have this Django permission?

### ModelAdmin permission

```python
modeladmin.has_change_permission(request)
```

asks:

> Does this user have permission to change this model through this ModelAdmin?

### Action permission

```python
@admin.action(permissions=["change"])
```

tells Django which permission the action requires.

---

# 48. Transaction + Admin Action

Because an action may modify many records, transactions are very useful.

```python
from django.db import transaction


@admin.action(description="Ship selected orders")
def order_shipped_action(modeladmin, request, queryset):

    with transaction.atomic():

        for order in queryset:

            order.status = "Shipped"
            order.save()

            order.user.email_user(
                subject="Your order has been shipped",
                message=(
                    f"Your order {order.id} "
                    f"has been shipped."
                ),
                from_email="admin@django.com",
                fail_silently=False,
            )

    modeladmin.message_user(
        request,
        "Orders shipped successfully."
    )
```

The transaction protects the database operations.

However, email has an important difference: **an email sent to an external mail system cannot be "unsent" by a database rollback**. For production systems, email sending is often better handled with a background task such as Celery and/or an `on_commit()` callback.

---

# 49. `transaction.on_commit()`

If you want to send an email only after the database transaction successfully commits:

```python
from django.db import transaction
```

Example:

```python
transaction.on_commit(
    lambda: user.email_user(
        subject="Your order has been shipped",
        message="Your order has been shipped.",
        from_email="admin@django.com",
    )
)
```

The idea is:

```text
Database changes
       ↓
COMMIT succeeds
       ↓
Send email
```

instead of:

```text
Send email
       ↓
Database operation fails
       ↓
ROLLBACK
```

This becomes especially useful when combining:

```text
Django
+
Transactions
+
Signals
+
Celery
+
Email
```

---

# 50. Quick Reference

## `modeladmin`

```python
modeladmin.get_queryset(request)

modeladmin.message_user(request, message)

modeladmin.has_view_permission(request)

modeladmin.has_add_permission(request)

modeladmin.has_change_permission(request)

modeladmin.has_delete_permission(request)

modeladmin.get_object(request, object_id)

modeladmin.get_urls()

modeladmin.model

modeladmin.opts

modeladmin.admin_site
```

## `request`

```python
request.user

request.method

request.GET

request.POST

request.FILES

request.path

request.session

request.META
```

### Especially useful for users:

```python
request.user.is_authenticated

request.user.is_active

request.user.is_staff

request.user.is_superuser

request.user.email

request.user.username

request.user.groups.all()

request.user.has_perm("core.change_order")
```

## `queryset`

```python
queryset.count()

queryset.exists()

queryset.first()

queryset.last()

queryset.filter(...)

queryset.exclude(...)

queryset.update(...)

queryset.delete()

queryset.values(...)

queryset.values_list(...)

queryset.order_by(...)

queryset.select_related(...)

queryset.prefetch_related(...)
```

---

# 51. The Big Picture

When Django calls:

```python
def order_shipped_action(
    modeladmin,
    request,
    queryset
):
```

think:

```text
                 ADMIN ACTION
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
    modeladmin     request     queryset
          │           │           │
          │           │           │
       Admin       Current      Selected
       class        user        objects
          │           │           │
          ↓           ↓           ↓
    permissions   request.user   update()
    messages      GET/POST       filter()
    queryset      session        delete()
    settings      permissions    save()
```

The most important three things to memorize are:

```python
modeladmin.message_user(
    request,
    "Done!"
)
```

```python
request.user
```

and:

```python
queryset.update(status="Shipped")
```

---

# 52. Most Important Distinction

If you see:

```python
def action(modeladmin, request, queryset):
```

remember:

```text
modeladmin
    = "How can I control/use the Django Admin?"

request
    = "WHO is making this request and what did they send?"

queryset
    = "WHICH database objects did the admin select?"
```

And when working with users:

```python
request.user
```

means:

> **The administrator currently logged into Django Admin.**

While:

```python
order.user
```

means:

> **The user/customer associated with that order.**

And:

```python
instance
```

means:

> **The particular model object involved in the current operation**, such as the object passed to a signal.

These three concepts—`request.user`, `order.user`, and `instance`—are worth keeping separate in your mind.
