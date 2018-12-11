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


def make_file_key(profile, filename, file_id):
    """Make unique key for file storage on s3"""
    return 'user/{}/{}/{}'.format(profile, file_id, filename)

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
            'file': FileSerializer(file).data,
            'presigned_url': s3_presigned_url(file.s3_key),

        })

    return result

def retrieve_file(requestor, file_pk):

    file = File.objects.get(pk=file_pk)
    url = s3_presigned_url(file.s3_key)
    return {
      'file': FileSerializer(file).data,
      'presigned_url': url,
    }

  
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

def delete_file(requestor,profile_pk, file_pk):
    """ Delete file """

    retrieved_file = File.objects.get(pk=file_pk,uploader=profile_pk)

    s3_delete(retrieved_file.s3_key)

    return retrieved_file.delete()



class MockS3Obj(object):

    def __init__(self, *, filekey, filebody, content_type):
        self.key = filekey
        self.content = filebody
        self.content_length = len(filebody)
        self.content_type = content_type
        self.metadata = {}


class MockStore(object):
    """ S3 Mock API calls. We know it's working if we can run the unit tests without having to configure settings.S3_SECRET_KEY """
    def __init__(self):
        self.store = {}

    def mock_upload(self, *, filekey, filebody, filename, uploader_pk, description):

        if filename.endswith('.jpg'):
            content_type = 'image/jpeg'
        else:
            content_type = 'application/binary'

        s3obj = MockS3Obj(filekey=filekey, filebody=filebody, content_type=content_type)
        self.store[filekey] = s3obj

        return s3obj

    def mock_delete(self, filekeys):

        keys = []

        for key in filekeys:
            if key.startswith('/'):
                filekey = key[1:]
            else:
                filekey = key

            if filekey in self.store:
                keys.append(filekey)
            else:
                # We asked to delete a non-existent S3Obj
                return False

        print(self.store)
        for key in keys:
            del self.store[key]

        with transaction.atomic():
            for key in keys:
                file = DocstoreFile.objects.filter(s3_key=key)
                if file.count():
                    file.delete()
                else:
                    print("Couldn't find file {} in DocStoreFile table".format(key))

        # NOTE(Jeroen): This return value goes unchecked because this entire call is wrapped an exception handler
        # And the return value from the service layer calling this isn't even checked in the view.
        return True

    def mock_presigned_url(self, filekey):
        if filekey not in self.store:
            raise BadRequest()

        result = "https://s3.{region}.amazonaws.com/{bucket}/{file}/" \
            "?X-Amz-Credential={access}%2F{date}%2F{region}%2Fs3%2Faws4_request&X-Amz-Date={datetime}" \
            "&X-Amz-SignedHeaders=host&X-Amz-Expires=3600&X-Amz-Algorithm=AWS4-HMAC-SHA256" \
            "&X-Amz-Signature=d8aa92b4732905b5b61713b2126d7b5a46e2534f1158b1ba6829f9e1bc98f877".format(
                region=settings.S3_REGION,
                bucket=settings.S3_BUCKET_NAME,
                access='currently-unchecked',
                # access=settings.S3_ACCESS_KEY,
                date='20180815',
                datetime='20180815T133552Z',
                file=filekey
            )
        return result

