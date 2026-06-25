from django.conf import settings
from django.db import migrations, models
import apps.accounts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gathering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(default=apps.accounts.models._generate_gathering_code, max_length=32, unique=True)),
                ('members', models.ManyToManyField(blank=True, related_name='user_gatherings', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='owned_gatherings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
