from decimal import Decimal
import math
import time
import uuid
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
import pandas as pd
from django.db import transaction

# Create your views here.


def query_builder(request):
    industry_data = (
        Record.objects.exclude(industry__exact="")
        .values_list("industry", flat=True)
        .distinct()
    )

    year_founded = Record.objects.values_list("year_founded", flat=True).distinct()
    city = Record.objects.values_list("city", flat=True).distinct()
    state = (
        Record.objects.exclude(state__exact="")
        .values_list("state", flat=True)
        .distinct()
    )
    country = (
        Record.objects.exclude(country__exact="")
        .values_list("country", flat=True)
        .distinct()
    )

    return render(
        request,
        "query.html",
        {
            "industry": industry_data,
            "year": year_founded,
            "city": city,
            "state": state,
            "country": country,
        },
    )


def upload_data(request):
    if request.method == "POST":
        try:
            file = request.FILES["file"]
            chunk_size = 100000
            records_to_create = []

            with transaction.atomic():
                df = pd.read_csv(file)

                for index, row_values in df.iterrows():
                    record = Record()
                    record.name = row_values.get("name")
                    record.domain = row_values.get("domain")
                    record.industry = row_values.get("industry")
                    record.size_range = row_values.get("size range")
                    record.linkedin_url = row_values.get("linkedin url")

                    record.year_founded = (
                        int(row_values.get("year founded"))
                        if not pd.isna(row_values.get("year founded"))
                        else None
                    )
                    record.current_employees = (
                        int(row_values.get("current employee estimate"))
                        if row_values.get("current employee estimate")
                        and not pd.isna(row_values.get("current employee estimate"))
                        else None
                    )
                    record.total_employees = (
                        int(row_values.get("total employee estimate"))
                        if row_values.get("total employee estimate")
                        and not pd.isna(row_values.get("total employee estimate"))
                        else None
                    )

                    locality = row_values.get("locality")
                    if isinstance(locality, str):
                        locality_parts = locality.split(",")
                        record.city = locality_parts[0].strip()
                        record.state = locality_parts[1].strip()
                        record.country = locality_parts[2].strip()
                    else:
                        record.city = ""
                        record.state = ""
                        record.country = ""

                    records_to_create.append(record)
                    if len(records_to_create) >= chunk_size:
                        Record.objects.bulk_create(records_to_create)
                        records_to_create = []

                if records_to_create:
                    Record.objects.bulk_create(records_to_create)

                messages.success(request, "Data uploaded successfully")
                return redirect("dashboard")

        except Exception as e:
            messages.error(request, "Something went wrong while processing the file")
            return redirect("dashboard")


class RecordCountView(generics.RetrieveAPIView):
    serializer_class = RecordSerializer

    def get(self, request, *args, **kwargs):
        industry = self.request.query_params.get("industry")
        year_founded = self.request.query_params.get("year")
        city = self.request.query_params.get("city")
        state = self.request.query_params.get("state")
        country = self.request.query_params.get("country")
        keyword = self.request.query_params.get("keyword")

        records = Record.objects.all()

        if keyword:
            records = records.filter(
                Q(industry__icontains=keyword)
                | Q(year_founded__icontains=keyword)
                | Q(city__icontains=keyword)
                | Q(state__icontains=keyword)
                | Q(country__icontains=keyword)
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

        return render(request, "query.html")
