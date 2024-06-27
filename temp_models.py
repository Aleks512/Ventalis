# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiApimessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    timestamp = models.DateTimeField()
    receiver = models.ForeignKey('UsersNewuser', models.DO_NOTHING)
    sender = models.ForeignKey('UsersNewuser', models.DO_NOTHING, related_name='apiapimessage_sender_set')

    class Meta:
        managed = False
        db_table = 'api_apimessage'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Consultants(models.Model):
    newuser_ptr = models.OneToOneField('UsersNewuser', models.DO_NOTHING, primary_key=True)
    matricule = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'consultants'


class Customers(models.Model):
    newuser_ptr = models.OneToOneField('UsersNewuser', models.DO_NOTHING, primary_key=True)
    consultant_applied = models.ForeignKey(Consultants, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersNewuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MessagerieMessagemodel(models.Model):
    id = models.BigAutoField(primary_key=True)
    body = models.CharField(max_length=1000)
    image = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField()
    is_read = models.BooleanField()
    receiver_user_id = models.BigIntegerField()
    sender_user_id = models.BigIntegerField()
    thread = models.ForeignKey('MessagerieThreadmodel', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'messagerie_messagemodel'


class MessagerieThreadmodel(models.Model):
    id = models.BigAutoField(primary_key=True)
    has_unread = models.BooleanField()
    receiver_id = models.BigIntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'messagerie_threadmodel'


class StoreCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    slug = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'store_category'


class StoreOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    transactionid = models.CharField(db_column='transactionId', max_length=20, blank=True, null=True)  # Field name made lowercase.
    date_ordered = models.DateTimeField()
    completed = models.BooleanField()
    comment = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_order'


class StoreOrderitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=2)
    ordered = models.BooleanField()
    quantity = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    order = models.ForeignKey(StoreOrder, models.DO_NOTHING)
    product = models.ForeignKey('StoreProduct', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_orderitem'


class StoreOrderitemstatushistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=2)
    comment = models.TextField(blank=True, null=True)
    date_modified = models.DateTimeField()
    consultant = models.ForeignKey(Consultants, models.DO_NOTHING)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    order_item = models.ForeignKey(StoreOrderitem, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_orderitemstatushistory'


class StoreProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    slug = models.CharField(unique=True, max_length=255)
    updated = models.DateTimeField()
    category = models.ForeignKey(StoreCategory, models.DO_NOTHING)
    created_by = models.ForeignKey('UsersNewuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'store_product'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey('UsersNewuser', models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class UsersAddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date_added = models.DateTimeField()
    address_type = models.CharField(max_length=1)
    default = models.BooleanField()
    order = models.ForeignKey(StoreOrder, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_address'


class UsersNewuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_client = models.BooleanField()
    is_employee = models.BooleanField()
    is_superuser = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users_newuser'


class UsersNewuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    newuser = models.ForeignKey(UsersNewuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_newuser_groups'
        unique_together = (('newuser', 'group'),)


class UsersNewuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    newuser = models.ForeignKey(UsersNewuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_newuser_user_permissions'
        unique_together = (('newuser', 'permission'),)
