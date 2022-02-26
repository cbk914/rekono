# Generated by Django 3.2.12 on 2022-02-26 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('input_types', '0001_initial'),
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_tool', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='output',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='tools.configuration'),
        ),
        migrations.AddField(
            model_name='output',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='input_types.inputtype'),
        ),
        migrations.AddField(
            model_name='intensity',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intensities', to='tools.tool'),
        ),
        migrations.AddField(
            model_name='input',
            name='argument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='tools.argument'),
        ),
        migrations.AddField(
            model_name='input',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='input_types.inputtype'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to='tools.tool'),
        ),
        migrations.AddField(
            model_name='argument',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arguments', to='tools.tool'),
        ),
        migrations.AddConstraint(
            model_name='output',
            constraint=models.UniqueConstraint(fields=('configuration', 'type'), name='unique output'),
        ),
        migrations.AddConstraint(
            model_name='input',
            constraint=models.UniqueConstraint(fields=('argument', 'order'), name='unique input'),
        ),
        migrations.AddConstraint(
            model_name='configuration',
            constraint=models.UniqueConstraint(fields=('tool', 'name'), name='unique configuration'),
        ),
        migrations.AddConstraint(
            model_name='argument',
            constraint=models.UniqueConstraint(fields=('tool', 'name'), name='unique argument'),
        ),
    ]
