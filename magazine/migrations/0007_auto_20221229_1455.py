# Generated by Django 3.2.13 on 2022-12-29 05:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('magazine', '0006_auto_20221229_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='magazine',
            name='tag',
            field=models.CharField(choices=[('BODO', '보도자료'), ('RECOMMEND', '추천·리뷰'), ('BASIC', '기초상식'), ('NEWS', '뉴스'), ('YEAR', '연말정산'), ('ECT', '기타')], default='ECT', max_length=20, verbose_name='태그명'),
        ),
    ]