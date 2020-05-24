# Generated by Django 3.0.4 on 2020-05-15 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0022_auto_20200515_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='city',
            field=models.CharField(choices=[('1', 'Adana'), ('2', 'Adıyaman'), ('3', 'Afyonkarahisar'), ('4', 'Ağrı '), ('5', 'Amasya '), ('6', 'Ankara '), ('7', 'Antalya '), ('8', 'Artvin '), ('9', 'Aydın '), ('10', 'Balıkesir'), ('11', 'Bilecik '), ('12', 'Bingöl '), ('13', 'Bitlis '), ('14', 'Bolu '), ('15', 'Burdur '), ('16', 'Bursa '), ('17', 'Çanakkale'), ('18', 'Çankırı '), ('19', 'Çorum '), ('20', 'Denizli '), ('21', 'Diyarbakır '), ('22', 'Edirne '), ('23', 'Elazığ '), ('24', 'Erzincan '), ('25', 'Erzurum '), ('26', 'Eskişehir '), ('27', 'Gaziantep '), ('28', 'Giresun '), ('29', 'Gümüşhane '), ('30', 'Hakkâri '), ('31', 'Hatay '), ('32', 'Isparta '), ('33', 'Mersin '), ('Istanbul', 'İstanbul '), ('35', 'İzmir '), ('59', 'Tekirdağ'), ('60', 'Tokat '), ('61', 'Trabzon '), ('62', 'Tunceli '), ('63', 'Şanlıurfa '), ('64', 'Uşak '), ('65', 'Van '), ('66', 'Yozgat'), ('67', 'Zonguldak'), ('68', 'Aksaray '), ('69', 'Bayburt '), ('70', 'Karaman '), ('71', 'Kırıkkale '), ('72', 'Batman '), ('73', 'Şırnak '), ('74', 'Bartın '), ('75', 'Ardahan '), ('76', 'Iğdır '), ('77', 'Yalova '), ('78', 'Karabük '), ('79', 'Kilis '), ('80', 'Osmaniye'), ('81', 'Düzce ')], max_length=10),
        ),
    ]
