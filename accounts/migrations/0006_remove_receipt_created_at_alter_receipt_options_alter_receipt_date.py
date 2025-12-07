# Generated migration to swap created_at with date field

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_receipt_options_remove_receipt_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='created_at',
        ),
        migrations.AddField(
            model_name='receipt',
            name='date',
            field=models.DateField(default=timezone.now),
        ),
        migrations.AlterModelOptions(
            name='receipt',
            options={'ordering': ['-date']},
        ),
    ]
