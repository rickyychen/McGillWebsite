# Generated by Django 3.1.3 on 2020-12-07 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20201205_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, default='')),
                ('newsDay', models.CharField(default='section', max_length=50)),
            ],
        ),
    ]