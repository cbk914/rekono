# Generated by Django 3.2.12 on 2022-02-26 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('executions', '0002_execution_step'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='tasks.task'),
        ),
    ]
