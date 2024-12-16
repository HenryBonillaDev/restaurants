import csv
import os
from celery import shared_task
from django.db import connection
from restaurantsprj.settings import BASE_DIR
from reports.domain.models import SalesReport

@shared_task
def generate_sales_report(report_id, month=None, year=None):
    try:
        output_dir = os.path.join(BASE_DIR, "s3")
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"sales_report_{report_id}.csv")
        query = """
            SELECT 
                r.id AS restaurant_id, 
                r.name AS restaurant_name, 
                COUNT(o.id) AS total_sales, 
                SUM(o.total_amount) AS total_revenue
            FROM restaurants_restaurant r
            LEFT JOIN orders_order o ON r.id = o.restaurant_id
            WHERE o.active = TRUE 
        """
        params = []
        if month:
            query += " AND EXTRACT(MONTH FROM o.created_at) = %s"
            params.append(month)
        if year:
            query += " AND EXTRACT(YEAR FROM o.created_at) = %s"
            params.append(year)
        query += " GROUP BY r.id ORDER BY total_revenue DESC"

        with connection.cursor() as cursor, open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            cursor.execute(query, params)
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["Restaurant ID", "Restaurant Name", "Total Sales", "Total Revenue"])
            for row in cursor.fetchall():
                writer.writerow(row)
        
        report = SalesReport.objects.get(id=report_id)
        report.status = "ok"
        report.file_path = file_path
        report.save()

    except Exception as e:
        report = SalesReport.objects.get(id=report_id)
        report.status = "error"
        report.save()
        raise e
