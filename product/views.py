import os
import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .models import Product

class LoadDataView(APIView):
    def post(self, request):
        # Define the path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'products.csv')
        
        try:
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(csv_file_path)

            # Ensure numeric values for price, quantity_sold, and rating
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

            # Handle missing values
            price_median = df['price'].median()
            quantity_sold_median = df['quantity_sold'].median()

            # Apply the median values to missing entries
            df['price'].fillna(price_median, inplace=False)
            df['quantity_sold'].fillna(quantity_sold_median, inplace=False)
            df['rating'] = df['rating'].fillna(df.groupby('category')['rating'].transform('mean'))

            # Reset index to avoid index issues
            df.reset_index(drop=True, inplace=True)

            # Iterate over the DataFrame rows and create Product instances
            for _, row in df.iterrows():
                Product.objects.create(
                    product_name=row['product_name'],
                    category=row['category'],
                    price=row['price'],
                    quantity_sold=row['quantity_sold'],
                    rating=row['rating'],
                    review_count=row['review_count']
                )
                
            return Response({'message': 'Data loaded successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class CreateSummaryView(APIView):
    def get(self, request):
        try:
            # Retrieve data from the Product table
            products = Product.objects.all().values()

            if not products:
                return HttpResponse("No data found in the products table.", status=404)

            # Convert the data to a Pandas DataFrame
            df = pd.DataFrame(list(products))

            if df.empty:
                return HttpResponse("The DataFrame is empty.", status=404)

            # Ensure 'price' and 'quantity_sold' are numeric
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')

            # Drop rows with missing 'price' or 'quantity_sold'
            df = df.dropna(subset=['price', 'quantity_sold'])

            if df.empty:
                return HttpResponse("DataFrame is empty after dropping missing values.", status=404)

            # Ensure 'product_name' and 'category' are present
            if 'product_name' not in df.columns or 'category' not in df.columns:
                return HttpResponse("Required columns are missing in the DataFrame.", status=400)

            # Calculate total revenue and top product quantity sold per category
            summary_df = df.groupby('category').agg(
                total_revenue=('price', 'sum'),
                top_product_quantity_sold=('quantity_sold', 'max')
            ).reset_index()

            # Get the top product name for each category
            top_products = df[df['quantity_sold'].isin(summary_df['top_product_quantity_sold'])]
            top_products = top_products[['category', 'product_name', 'quantity_sold']]
            
            # For each category, get the top product with max quantity_sold
            summary_df = summary_df.merge(top_products, left_on=['category', 'top_product_quantity_sold'], right_on=['category', 'quantity_sold'])
            summary_df = summary_df.rename(columns={'product_name': 'top_product'})
            
            # Drop unnecessary columns
            summary_df = summary_df[['category', 'total_revenue', 'top_product', 'top_product_quantity_sold']]

            # Define the path to save the CSV file
            csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'summary_report.csv')

            # Write the summary DataFrame to a CSV file
            summary_df.to_csv(csv_file_path, index=False)

            # Return a response indicating success
            return HttpResponse(f"Summary report generated successfully at: {csv_file_path}")

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)