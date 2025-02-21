from celery import shared_task
import csv
from django.db import transaction
from .dynamic_registry import DYNAMIC_MODELS 
from django.apps import apps
from django.db import models, connection, transaction, IntegrityError
import redis
from django.core.mail import send_mail



import csv
import redis
from django.db import transaction
from django.core.mail import send_mail
from celery import shared_task

BATCH_SIZE = 5000  # Process records in chunks

@shared_task
def process_csv_import(table_name, file_path):
    r = redis.Redis(host='127.0.0.1', port=6381, db=0)
    if not r.ping():
        return "Failed to connect to Redis."

    DynamicModel = get_dynamic_model(table_name)
    if not DynamicModel:
        return f"Table '{table_name}' not found."

    required_fields = [field.name for field in DynamicModel._meta.fields if not field.null and not field.blank]

    total_records = 0
    error_count = 0
    errors = []
    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_records += 1
            missing_fields = [field for field in required_fields if not row.get(field)]
            if missing_fields:
                errors.append(f"Missing fields {missing_fields} in row {total_records}")
                error_count += 1
                continue

            # Validate uniqueness (if applicable)
            if "email" in row and DynamicModel.objects.filter(email=row["email"]).exists():
                errors.append(f"Duplicate email: {row['email']} in row {total_records}")
                error_count += 1
                continue

            records.append(DynamicModel(**row))

            # Insert in batches
            if len(records) >= BATCH_SIZE:
                with transaction.atomic():
                    DynamicModel.objects.bulk_create(records, ignore_conflicts=True)
                records = []  # Clear batch

            # Track progress in Redis
            r.set(f"csv_import:{table_name}:progress", f"{total_records} processed, {error_count} errors")

    # Insert remaining records
    if records:
        with transaction.atomic():
            DynamicModel.objects.bulk_create(records, ignore_conflicts=True)

    # Log errors in Redis
    r.set(f"csv_import:{table_name}:errors", "\n".join(errors))

    # Send email notification
    subject = "Import Completed"
    message = f"Import completed with {total_records} records processed. {error_count} errors encountered."
    send_mail(
        subject,
        message,
        "testassignment00@gmail.com",
        ["mazenbanna15@gmail.com","hzeineddine@arabiagis.com"],
        html_message=f"<strong>{message}</strong>"
    )

    return f"Import completed: {total_records} records processed, {error_count} errors."



def get_dynamic_model(table_name):
    table_name = table_name.lower()
    if table_name in DYNAMIC_MODELS:
        return DYNAMIC_MODELS[table_name]

    try:
        return apps.get_model('assignmentapp', table_name)
    except LookupError:
        pass  

    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s);", [table_name])
        if cursor.fetchone()[0]:
            print(f" Table '{table_name}' exists but model is not registered.")
            return None  
    
    return None
