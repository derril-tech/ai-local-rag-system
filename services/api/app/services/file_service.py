# File service
# Handles file storage and management

from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError
import os
import mimetypes

class FileService:
    """Service for file storage and management"""
    
    def __init__(self):
        # Initialize S3/MinIO client
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000'),
            aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID', 'minioadmin'),
            aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY', 'minioadmin'),
            region_name=os.getenv('S3_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME', 'rag-system')
    
    def is_supported_file_type(self, filename: str) -> bool:
        """Check if file type is supported"""
        supported_extensions = {
            '.pdf', '.txt', '.docx', '.doc', '.pptx', '.ppt',
            '.xlsx', '.xls', '.csv', '.json', '.xml', '.html',
            '.md', '.rtf', '.odt', '.ods', '.odp'
        }
        
        file_ext = os.path.splitext(filename.lower())[1]
        return file_ext in supported_extensions
    
    def get_mime_type(self, filename: str) -> str:
        """Get MIME type for file"""
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    
    async def upload_file(self, file_content: bytes, filename: str, content_type: str) -> str:
        """Upload file to storage"""
        try:
            # Generate unique file path
            import uuid
            file_id = str(uuid.uuid4())
            file_path = f"uploads/{file_id}/{filename}"
            
            # Upload to S3/MinIO
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=file_content,
                ContentType=content_type
            )
            
            return file_path
        except ClientError as e:
            raise Exception(f"Failed to upload file: {e}")
    
    async def download_file(self, file_path: str) -> bytes:
        """Download file from storage"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['Body'].read()
        except ClientError as e:
            raise Exception(f"Failed to download file: {e}")
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete file: {e}")
    
    async def get_file_url(self, file_path: str, expires_in: int = 3600) -> str:
        """Get signed URL for file access"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate signed URL: {e}")
    
    async def list_files(self, prefix: str = "", limit: int = 100) -> List[Dict[str, Any]]:
        """List files in storage"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=limit
            )
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
                })
            
            return files
        except ClientError as e:
            raise Exception(f"Failed to list files: {e}")
