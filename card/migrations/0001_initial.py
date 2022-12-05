# Generated by Django 3.2.13 on 2022-12-05 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.IntegerField()),
                ('bnf_name', models.CharField(max_length=200, null=True)),
                ('bnf_content', models.TextField(null=True)),
                ('bnf_detail', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.IntegerField()),
                ('card_name', models.CharField(max_length=200, null=True)),
                ('card_brand', models.CharField(max_length=30, null=True)),
                ('card_in_out_1', models.CharField(max_length=100, null=True)),
                ('card_in_out_2', models.CharField(max_length=100, null=True)),
                ('card_in_out_3', models.CharField(max_length=100, null=True)),
                ('card_img', models.TextField()),
                ('card_record', models.CharField(max_length=100, null=True)),
                ('card_overseas', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetailComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('rate', models.CharField(choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], max_length=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='card.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
