from django.contrib.auth.decorators import login_required
from apps.files.serializers import FileSerializer
from django.urls import reverse_lazy
import mimetypes
from django.db import transaction
from apps.files.models import File
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404
import re


def make_file_key(profile, filename, file_id):
    """Make unique key for file storage on s3"""
    return 'user/{}/{}/{}'.format(profile, file_id, filename)

FILE_KEY_RE = re.compile(r'^user/(?P<profile>\d+)/(?P<file_id>[a-z_\-]+)/(?P<filename>.+)$')


def parse_file_key(file_key):
    match = FILE_KEY_RE.match(file_key)
    import pdb; pdb.set_trace()
    if match is not None:
        return {
            'profile': int(match.group('profile')),
            'file_id': match.group('file_id'),
            'filename': match.group('filename'),
            'raw': file_key
        }
    return None


def s3_encode_metadata(s):
    out_string = ''
    for c in s:
        if ord(c) == 92:  # character = \
            out_string += '\\0x5c\\'
        elif ord(c) > 127:
            safe_ord = str(hex(ord(c)))
            out_string += '\\'+safe_ord+'\\'
        else:
            out_string += c
    return out_string


def s3_get_resource():
    s3 = boto3.resource(
        's3',
        settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        )
    )
    return s3


def s3_get_bucket(bucket_name):
    s3 = s3_get_resource()
    bucket = s3.Bucket(bucket_name)
    return bucket

def s3_delete(filekeys):

    bucket = s3_get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    objects = []

    objects.append({'Key': filekeys})
    try:
        response = bucket.delete_objects(
            Delete={
                'Objects': objects,
                'Quiet': False
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except:
        return False

def s3_get_client():
    try:
        client = boto3.client(
            's3',
            settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'}
            )
        )
        return client
    except ClientError as e:
        print("Couldn't establish S3 client connection: ", e)
        return None


def s3_upload(*, filekey, filebody, filename, uploader_pk, description):

    bucket = s3_get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    if not description:
        description = filename

    mimetypes.init()
    content_type, content_encoding = mimetypes.guess_type(filename)
    if not content_type:
        content_type = 'application/binary'
    if not content_encoding:
        content_encoding = ''

    # Upload file object to bucket
    # put_object retained for backwards compatibility with the docstore model
    if hasattr(filebody, 'read'):
        bucket.upload_fileobj(
            filebody,
            filekey,
            ExtraArgs={
                'ContentDisposition': (
                    'attachment; filename={}'.format(filename)
                ),
                'ContentType': filebody.content_type or content_type,
                'ServerSideEncryption': 'aws:kms',
                'SSEKMSKeyId' : 'alias/aws/s3'
            }
        )
        return

    s3obj = bucket.put_object(
        Body=filebody,
        ContentDisposition='attachment; filename={}'.format(filename),
        ContentType=content_type,
        Key=filekey,
        Metadata={
            'uploader_pk': '{}'.format(uploader_pk),
            'description': s3_encode_metadata(description),
            'filename': s3_encode_metadata(filename),
        },
        ServerSideEncryption='aws:kms',
        SSEKMSKeyId='alias/aws/s3'
    )
    return s3obj


def get_file_url(requestor, file_id):
    """ Get file url """
    try:
        retrieved_file = File.objects.get(id=file_id)
    except ObjectDoesNotExist:
        return 'Does not exist'

    return s3_presigned_url(retrieved_file.s3_key)


def upload_files(
    requestor,
    *,
    profile_pk,
    files,
    description,
):
    """ Upload files """
    with transaction.atomic():
        for file_object in files.values():
            filename = file_object.name

            serializer = FileSerializer(
                data={
                    'name': filename,
                    'type': file_object.content_type,
                    'uploader': requestor.pk,
                    'description': description,
                }
            )
            if serializer.is_valid(raise_exception=True):
                file_entry = serializer.save()

            file_key = make_file_key(
                profile_pk, filename, file_entry.id
            )

            # upload file into s3 bucket
            s3_upload(
                filekey=file_key,
                filebody=file_object,
                filename=filename,
                uploader_pk=requestor.pk,
                description=description
            )

            # update file instance with generated file key
            serializer = FileSerializer(
                file_entry, data={'s3_key': file_key}, partial=True
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return serializer.data


def list_files(requestor, profile_pk):

    result = []

    files = File.objects.filter(
        uploader=profile_pk
    )
    for file in files:
        result.append({
            'filename': file.name,
            'uploader': file.uploader.get_full_name(),
            'created_at': file.created_at,
            'metadata': {
                'uploader_pk': str(file.uploader.pk),
                'description': file.description,
                'filename': file.name
            },
            'description': file.description,
            'type': file.type,
            's3_key': file.s3_key,
        })

    return result

def retrieve_file(requestor, *, file_pk):
  
    return File.objects.get(pk=file_pk)

# def update_file(requestor, *, file_pk):
  
def update_file(
    requestor,
    *,
    profile_pk,
    file_pk,
    description,
    files,
):
    """ Update file """
    retrieved_file = File.objects.get(pk=file_pk,uploader=profile_pk)

    with transaction.atomic():
        if len(files) > 0:
            for file_object in files.values():
                filename = file_object.name
                file_object = file_object.content_type
        else:
            filename = retrieved_file.name
            file_object = retrieved_file.type

        if description != '':
            description = description
        else:
            description = retrieved_file.description

        payload ={
            'name': filename,
            'type': file_object,
            'description': description,
        }
        serializer = FileSerializer(retrieved_file, data= payload, partial=True)
        if serializer.is_valid(raise_exception=True):
            file_entry = serializer.save()

        file_key = make_file_key(
          profile_pk, filename, file_entry.id
        )
        s3_delete(retrieved_file.s3_key)
        # upload file into s3 bucket
        s3_upload(
            filekey=file_key,
            filebody=file_object,
            filename=filename,
            uploader_pk=requestor.pk,
            description=description
        )
        
        # update file instance with generated file key
        serializer = FileSerializer(
            file_entry, data={'s3_key': file_key}, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return serializer.data

def s3_presigned_url(file_key):
    # generate signed download url
    s3client = s3_get_client()
    url = s3client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_key
        }
    )
    return url

def retrieve_file_url(requestor, *, file_key):
    return s3_presigned_url(file_key)
