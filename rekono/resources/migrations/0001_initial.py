# Generated by Django 3.2.12 on 2022-02-26 10:30

from django.db import migrations, models
import input_types.base
import security.input_validation


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wordlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100, unique=True, validators=[security.input_validation.validate_name])),
                ('type', models.TextField(choices=[('Password', 'Password'), ('Endpoint', 'Endpoint')], max_length=10)),
                ('path', models.TextField(max_length=200, unique=True)),
                ('checksum', models.TextField(blank=True, max_length=128, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, input_types.base.BaseInput),
        ),
    ]
