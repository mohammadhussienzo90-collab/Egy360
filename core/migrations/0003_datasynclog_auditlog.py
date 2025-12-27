# Generated migration for DataSyncLog and AuditLog models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_setup_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSyncLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_type', models.CharField(choices=[
                    ('travelpayouts', 'Travelpayouts Affiliate Sync'),
                    ('hotels', 'Hotel Data Sync'),
                    ('tours', 'Tour Data Sync'),
                    ('pricing', 'Pricing Update'),
                    ('images', 'Image Sync'),
                ], max_length=50)),
                ('status', models.CharField(choices=[
                    ('running', 'Running'),
                    ('success', 'Success'),
                    ('failed', 'Failed'),
                    ('partial', 'Partial Success'),
                ], default='running', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('records_processed', models.IntegerField(default=0)),
                ('records_updated', models.IntegerField(default=0)),
                ('records_created', models.IntegerField(default=0)),
                ('records_failed', models.IntegerField(default=0)),
                ('errors', models.JSONField(blank=True, default=list)),
                ('details', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Data Sync Log',
                'verbose_name_plural': 'Data Sync Logs',
                'db_table': 'data_sync_logs',
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[
                    ('create', 'Create'),
                    ('update', 'Update'),
                    ('delete', 'Delete'),
                    ('restore', 'Restore'),
                ], max_length=20)),
                ('model_name', models.CharField(max_length=100)),
                ('object_id', models.IntegerField()),
                ('object_repr', models.CharField(blank=True, max_length=200)),
                ('changes', models.JSONField(blank=True, default=dict)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='audit_logs',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
                'db_table': 'audit_logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['model_name', 'object_id'], name='audit_model_obj_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['user'], name='audit_user_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['timestamp'], name='audit_timestamp_idx'),
        ),
    ]
