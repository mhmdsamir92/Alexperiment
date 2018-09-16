# Generated by Django 2.1.1 on 2018-09-15 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.TextField()),
                ('is_final_result', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.Run')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowPerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='wf_perm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lab.WorkflowPerm'),
        ),
    ]