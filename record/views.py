from decimal import Decimal
from django.shortcuts import render, redirect
import csv
from .models import Record
from django.contrib import messages
import io
from rest_framework import generics
from rest_framework.response import Response
from .models import Record
from .serializers import RecordSerializer
from django.db.models import Q

# Create your views here.

def query_builder(request):
    industry_data = Record.objects.values_list('industry', flat=True).distinct()
    year_founded = Record.objects.values_list('year_founded', flat=True).distinct()
    city = Record.objects.values_list('city', flat=True).distinct()
    state = Record.objects.values_list('state', flat=True).distinct()
    country = Record.objects.values_list('country', flat=True).distinct()


    return render(request, "query.html",
                  {"industry":industry_data,
                    "year":year_founded,
                    "city":city,
                    "state":state,
                    "country":country
                    })



def upload_data(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if file:
           
                                
            chunk_size = 1000  
            rows_processed = 0  
            try:
                for chunk in file.chunks():
                    try:
                        decoded_chunk = chunk.decode('utf-8')
                    except UnicodeDecodeError as e:
                        continue  
                    reader_chunk = reader_chunk = csv.DictReader(io.StringIO(decoded_chunk))
                    
                    records_to_create = []
                    
                    for row in reader_chunk:
                        try:
                            name = row.get('name')
                            domain = row.get('domain')
                            year_founded_str = row.get('year founded', '')  # Get year founded or use empty string if not present
                            industry = row.get('industry')
                            size_range = row.get('size range')
                            linkedin_url = row.get('linkedin url')
                            current_employees = int(row.get('current employee estimate')) if row.get('current employee estimate') else None
                            total_employees = int(row.get('total employee estimate')) if row.get('total employee estimate') else None

                            if 'locality' in row and row['locality']:
                                locality_parts = row['locality'].split(',')
                                city = locality_parts[0].strip()
                                state = locality_parts[1].strip()
                                country = locality_parts[2].strip()
                            else:
                                city = ''
                                state = ''
                                country = ''

                            year_founded = int(year_founded_str) if year_founded_str else None

                            record = Record(
                                name=name,
                                domain=domain,
                                year_founded=year_founded,
                                industry=industry,
                                size_range=size_range,
                                city=city,
                                state=state,
                                country=country,
                                linkedin_url=linkedin_url,
                                current_employees=current_employees,
                                total_employees=total_employees
                            )
                            
                            records_to_create.append(record)
                            
                            rows_processed += 1

                        except Exception as e:
                            print(f"Error processing row: {e}")

                    if records_to_create:
                        Record.objects.bulk_create(records_to_create)

                    print(f"Total rows processed: {rows_processed}")

                messages.success(request, "Data uploaded successfully")
                return redirect("dashboard")

            except Exception as e:
                messages.error(request, "Something went wrong while processing the file")
                return redirect("dashboard")


        else:
            messages.error(request, "Please upload a valid document")
            return redirect("dashboard")

    return redirect("dashboard")



class RecordCountView(generics.RetrieveAPIView):
    serializer_class = RecordSerializer
    
    def get(self, request, *args, **kwargs):
        industry = self.request.query_params.get('industry')
        year_founded = self.request.query_params.get('year')
        city = self.request.query_params.get('city')
        state = self.request.query_params.get('state')
        country = self.request.query_params.get('country')
        keyword = self.request.query_params.get('keyword')
        
        records = Record.objects.all()

        if keyword:
            records = records.filter(
                Q(industry__icontains=keyword) |
                Q(year_founded__icontains=keyword) |
                Q(city__icontains=keyword) |
                Q(state__icontains=keyword) |
                Q(country__icontains=keyword)
            )

        if industry:
            records = records.filter(industry__icontains=industry)

        if year_founded:
            records = records.filter(year_founded=year_founded)

        if city:
            records = records.filter(city=city)

        if state:
            records = records.filter(state=state)

        if country:
            records = records.filter(country=country)

        record_count = records.count()
        messages.success(request, f"{record_count} records found for the query")

        return render(request,"query.html")
