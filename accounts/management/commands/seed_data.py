import os

from django.core.management.base import BaseCommand

from accounts.models import User
from resep.models import MasterObat


class Command(BaseCommand):
    help = 'Seed initial data: admin, admisi, dokter users, and master obat'

    def handle(self, *args, **options):
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admisi_username = os.environ.get('ADMISI_USERNAME', 'admisi')
        admisi_password = os.environ.get('ADMISI_PASSWORD', 'admisi123')
        dokter_username = os.environ.get('DOKTER_USERNAME', 'dokter')
        dokter_password = os.environ.get('DOKTER_PASSWORD', 'dokter123')

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user created ({admin_username})'))

        if not User.objects.filter(username=admisi_username).exists():
            User.objects.create_user(
                username=admisi_username,
                password=admisi_password,
                role='admisi',
            )
            self.stdout.write(self.style.SUCCESS(f'Admisi user created ({admisi_username})'))

        if not User.objects.filter(username=dokter_username).exists():
            User.objects.create_user(
                username=dokter_username,
                password=dokter_password,
                role='dokter',
            )
            self.stdout.write(self.style.SUCCESS(f'Dokter user created ({dokter_username})'))

        master_obat_list = [
            ('Paracetamol 500mg', '500mg', 'tablet'),
            ('Amoxicillin 500mg', '500mg', 'kapsul'),
            ('Ibuprofen 400mg', '400mg', 'tablet'),
            ('Asam Mefenamat 500mg', '500mg', 'kapsul'),
            ('Ciprofloxacin 500mg', '500mg', 'tablet'),
            ('Dexamethasone 0.5mg', '0.5mg', 'tablet'),
            ('Antalgin 500mg', '500mg', 'tablet'),
            ('Chlorhexidine Mouthwash', '0.2%', 'botol'),
            ('Povidone Iodine 1%', '1%', 'botol'),
            ('Hydrogen Peroxide 3%', '3%', 'botol'),
            ('Cataflam 50mg', '50mg', 'tablet'),
            ('Metronidazole 500mg', '500mg', 'tablet'),
        ]
        created = 0
        for nama, dosis, satuan in master_obat_list:
            if not MasterObat.objects.filter(nama=nama).exists():
                MasterObat.objects.create(nama=nama, dosis_default=dosis, satuan=satuan)
                created += 1

        if created:
            self.stdout.write(self.style.SUCCESS(f'{created} master obat created'))
