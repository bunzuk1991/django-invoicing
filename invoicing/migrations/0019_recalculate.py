from django.db import migrations, transaction
from invoicing.models import Invoice


def recalculate(*args, **kwargs):
    for invoice in Invoice.objects.all():
        with transaction.atomic():
            invoice.total = invoice.calculate_total()
            invoice.vat = invoice.calculate_vat()
            invoice.save(update_fields=['total'])
            invoice.save(update_fields=['vat'])


class Migration(migrations.Migration):
    dependencies = [
        ('invoicing', '0018_invoice_attachments'),
    ]

    operations = [
        migrations.RunPython(recalculate, lambda *args, **kwargs: None)
    ]
