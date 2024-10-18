# Generated by Django 5.1.1 on 2024-10-11 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_contribuable_mot_de_passe'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribuable',
            name='bank_acct_no',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='dm_ref',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='passeport',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='photo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='propr_nif',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='statistic_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='contribuable',
            name='statistic_no',
            field=models.CharField(max_length=21, null=True),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='cin',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='contact',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='lieu_delivrance',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='lieu_naissance',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='contribuable',
            name='mot_de_passe',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
