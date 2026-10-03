from django.core.management.base import BaseCommand

from accounts.models import User
from resep.models import MasterObat


class Command(BaseCommand):
    help = 'Seed initial data: admin, admisi, dokter users, and master obat'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                role='admin',
            )
            self.stdout.write(self.style.SUCCESS('Admin user created (admin/admin123)'))

        if not User.objects.filter(username='admisi').exists():
            User.objects.create_user(
                username='admisi',
                password='admisi123',
                role='admisi',
            )
            self.stdout.write(self.style.SUCCESS('Admisi user created (admisi/admisi123)'))

        if not User.objects.filter(username='dokter').exists():
            User.objects.create_user(
                username='dokter',
                password='dokter123',
                role='dokter',
            )
            self.stdout.write(self.style.SUCCESS('Dokter user created (dokter/dokter123)'))

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
