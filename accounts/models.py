import os
import sys
import uuid
import json
import logging

from accounts import settings

from pynamodb.models import Model
from pynamodb.connection import TableConnection
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, 
    UnicodeSetAttribute, UTCDateTimeAttribute,
    ListAttribute, MapAttribute, BinaryAttribute
)

from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, LocalSecondaryIndex
from datetime import datetime

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.propagate = True


class SkillSet(MapAttribute):
    name = UnicodeAttribute(null=True)
    price = NumberAttribute(default=0, null=True)


class NameIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "nameIdx"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    name = UnicodeAttribute(hash_key=True)


class Users(Model):
    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        table_name = settings.TABLE_NAME
        # host = "http://localhost:8000"
        region = os.getenv("AWS_REGION")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    uuid = UnicodeAttribute(hash_key=True)
    userType = UnicodeAttribute()
    # userType = UnicodeAttribute(range_key=True)
    username = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    firstName = UnicodeAttribute(null=False)
    lastName = UnicodeAttribute(null=False)
    phone = UnicodeAttribute(null=False)
    address = UnicodeAttribute()
    area = UnicodeAttribute()
    city = UnicodeAttribute()
    # days = ListAttribute(default=list, null=True)
    days = ListAttribute(null=True)
    time = UnicodeAttribute(null=True)
    finalRating = UnicodeAttribute(null=True)
    image = UnicodeAttribute(null=True)
    skillSet = ListAttribute(of=SkillSet, null=True)
    appointments = ListAttribute(default=list, null=True)

    nameIndex = NameIndex()

    def save(self, **kwargs):
        return super(Users, self).save(**kwargs)


def InitUserTable():
    try:
        if not Users.exists():
            # Users.delete_table()
            log.info("Creating Users table .....")
            Users.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)
    except Exception as e:
        log.error(f"DB initialization failed: {str(e)}")
        sys.exit(1)


def SaveInDB(body, update=False):
    if body["userType"] == "provider":
        u = Users(
            userType=body["userType"],
            uuid=body["uuid"],
            username=body["username"],
            email=body["email"],
            firstName=body["firstName"],
            lastName=body["lastName"],
            phone=body["phone"],
            address=body["address"],
            area=body["area"],
            city=body["city"],
            days=body["days"],
            time=body["time"],
            skillSet=body["skillSet"],
            image="None",
            finalRating="0"
        )
    else:
        u = Users(
            userType=body["userType"],
            uuid=body["uuid"],
            username=body["username"],
            email=body["email"],
            firstName=body["firstName"],
            lastName=body["lastName"],
            phone=body["phone"],
            address=body["address"],
            area=body["area"],
            city=body["city"]
        )

    if update:
        u.update()
    else:
        u.save()


def UpdateItem(uid, userType, body=None, update=False, delete=False):
    try:
        conn = TableConnection(
            table_name=settings.TABLE_NAME, 
            region=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        if delete:
            return conn.delete_item(hash_key=uid), None
            # return conn.delete_item(hash_key=uid, range_key=userType), None
        elif update and body:
            userObj = Users.get(uid)
            # userObj = Users.get(uid, userType)
            userObj.refresh()
            r = userObj.update(actions=[
                getattr(Users, k).set(v) for k, v in body.items()
            ])
            return r, None
            # return conn.put_item(hash_key=uid, range_key=userType, attributes={"firstName": body["firstName"]}), None
    except Exception as e:
        return None, str(e)


def SerializeUserObj(user):

    if user.userType == "provider":
        out = {
            "userType": user.userType,
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "phone": user.phone,
            "address": user.address,
            "area": user.area,            
            "city": user.city,
            "image": user.image,
            "days":user.days,
            "time": user.time,
            "skillSet": [{"name": s.name, "price": s.price} for s in user.skillSet],
            "appointments": user.appointments,
            "finalRating": user.finalRating
        }
    else:
        out = {
            "userType": user.userType,
            "uuid": user.uuid,
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "phone": user.phone,
            "address": user.address,
            "area": user.area,            
            "city": user.city,
            # "time": user.time,
            "appointments": user.appointments
        }        

    return out
