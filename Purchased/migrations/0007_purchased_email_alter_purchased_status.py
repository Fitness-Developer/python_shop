# Generated by Django 5.1.1 on 2024-12-02 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Purchased', '0006_alter_purchased_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchased',
            name='email',
            field=models.EmailField(default=2, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchased',
            name='status',
            field=models.CharField(choices=[('В ожидании', 'В ожидании'), ('В пути', 'В пути'), ('Прибыл', 'Прибыл')], default='В ожидании', max_length=20),
        ),
    ]
