"""S3 uploader for AWS bill PDFs."""

import os
from datetime import datetime
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def upload_pdf_to_s3(
    pdf_bytes: bytes,
    bucket_name: Optional[str] = None,
    expiration: int = 21600
) -> dict:
    """Upload PDF to S3 and generate a presigned URL.

    Args:
        pdf_bytes: PDF file as bytes
        bucket_name: S3 bucket name (defaults to env var BILL_PDF_BUCKET)
        expiration: URL expiration time in seconds (default: 6 hours)

    Returns:
        Dictionary with:
            - s3_key: S3 object key
            - s3_url: Presigned URL
            - bucket: Bucket name
            - expiration: Expiration time in seconds
    """
    # Get bucket name from environment or parameter
    bucket = bucket_name or os.getenv('BILL_PDF_BUCKET', 'aws-bill-invoices-demo')
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"invoices/{timestamp}_aws_bill.pdf"
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    
    try:
        # Upload PDF to S3
        s3_client.put_object(
            Bucket=bucket,
            Key=filename,
            Body=pdf_bytes,
            ContentType='application/pdf',
            ContentDisposition=f'inline; filename="aws_bill_{timestamp}.pdf"',
            Metadata={
                'generated_at': datetime.now().isoformat(),
                'content_type': 'aws_bill_invoice'
            }
        )
        
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': filename
            },
            ExpiresIn=expiration
        )
        
        return {
            's3_key': filename,
            's3_url': presigned_url,
            'bucket': bucket,
            'expiration_seconds': expiration,
            'status': 'uploaded'
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'status': 'error',
            'error_code': error_code,
            'error_message': error_message,
            'bucket': bucket,
            's3_key': filename
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': str(e),
            'bucket': bucket,
            's3_key': filename
        }


def create_bucket_if_not_exists(bucket_name: str, region: str = 'us-east-1') -> bool:
    """Create S3 bucket if it doesn't exist.

    Args:
        bucket_name: Name of the bucket to create
        region: AWS region (default: us-east-1)

    Returns:
        True if bucket exists or was created, False otherwise
    """
    s3_client = boto3.client('s3', region_name=region)
    
    try:
        # Check if bucket exists
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        if error_code == '404':
            # Bucket doesn't exist, create it
            try:
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                
                # Enable versioning (optional)
                s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                
                # Set lifecycle policy to delete old invoices after 30 days
                s3_client.put_bucket_lifecycle_configuration(
                    Bucket=bucket_name,
                    LifecycleConfiguration={
                        'Rules': [
                            {
                                'ID': 'DeleteOldInvoices',
                                'Status': 'Enabled',
                                'Prefix': 'invoices/',
                                'Expiration': {'Days': 30}
                            }
                        ]
                    }
                )
                
                return True
            except ClientError:
                return False
        else:
            return False
