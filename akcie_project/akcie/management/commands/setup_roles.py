from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from akcie.models import Akcie, Transakce, Dividenda

def setup_roles():
    # Vytvoření rolí: Admin, Poradce, Klient
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    poradce_group, _ = Group.objects.get_or_create(name='Poradce')
    klient_group, _ = Group.objects.get_or_create(name='Klient')

    # Admin má všechna práva
    for model in [Akcie, Transakce, Dividenda]:
        ct = ContentType.objects.get_for_model(model)
        for perm in Permission.objects.filter(content_type=ct):
            admin_group.permissions.add(perm)

    # Poradce může číst, přidávat, měnit, ale ne mazat
    for model in [Akcie, Transakce, Dividenda]:
        ct = ContentType.objects.get_for_model(model)
        for codename in ['add', 'change', 'view']:
            perm = Permission.objects.get(content_type=ct, codename=f'{codename}_{model._meta.model_name}')
            poradce_group.permissions.add(perm)

    # Klient může pouze číst
    for model in [Akcie, Transakce, Dividenda]:
        ct = ContentType.objects.get_for_model(model)
        perm = Permission.objects.get(content_type=ct, codename=f'view_{model._meta.model_name}')
        klient_group.permissions.add(perm)
