# Generated manually for tour_booking field addition

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_orderlineitem_product'),
        ('tours', '0002_tourbooking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='tour_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tours.tourbooking'),
        ),
    ]

