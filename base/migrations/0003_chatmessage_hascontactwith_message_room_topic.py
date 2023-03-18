# Generated by Django 3.2.7 on 2023-03-18 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20230318_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(default='avatar.svg', null=True, upload_to='')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cohosts', models.ManyToManyField(blank=True, related_name='cohosts', to=settings.AUTH_USER_MODEL)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('notallowed', models.ManyToManyField(blank=True, related_name='notallowed', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.topic')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(null=True)),
                ('uploadfile', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('isimg', models.BooleanField(null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Hascontactwith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactpersons', models.ManyToManyField(blank=True, related_name='contactpersons', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chatmessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(null=True)),
                ('uploadfile', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('isimg', models.BooleanField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fromuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fromuser', to=settings.AUTH_USER_MODEL)),
                ('touser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='touser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
