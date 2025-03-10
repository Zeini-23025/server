# Generated by Django 5.1.7 on 2025-03-08 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('identifiant', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExceptionCalendrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semaine', models.IntegerField()),
                ('jour', models.CharField(max_length=50)),
                ('type_exception', models.CharField(max_length=50)),
                ('valeur', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('semestre', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('credits', models.IntegerField()),
                ('semestre', models.IntegerField()),
                ('filiere', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DisponibiliteEnseignant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(max_length=50)),
                ('creneau', models.CharField(max_length=50)),
                ('semaine', models.IntegerField()),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enseignant')),
            ],
        ),
        migrations.CreateModel(
            name='ConflitGroupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raison', models.CharField(max_length=255)),
                ('groupe1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflits_groupe1', to='app.groupe')),
                ('groupe2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conflits_groupe2', to='app.groupe')),
            ],
        ),
        migrations.CreateModel(
            name='GroupeMatiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.groupe')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='EmploiTemps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jour', models.CharField(max_length=50)),
                ('creneau', models.CharField(max_length=50)),
                ('type_cours', models.CharField(max_length=50)),
                ('semaine', models.IntegerField()),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enseignant')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.groupe')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='ChargeHebdomadaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heures_cm', models.IntegerField()),
                ('heures_td', models.IntegerField()),
                ('heures_tp', models.IntegerField()),
                ('semaine', models.IntegerField()),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='AffectationEnseignant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_cours', models.CharField(max_length=50)),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.enseignant')),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.groupe')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.matiere')),
            ],
        ),
    ]
