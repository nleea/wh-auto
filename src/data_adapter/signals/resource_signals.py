from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from data_adapter.resources import Resources
from data_adapter.permission import Permission
import uuid

is_bulk_inserting = False


@event.listens_for(Resources, "after_insert")
def create_permissions_resources(mapper, connection, target):
    global is_bulk_inserting

    if is_bulk_inserting:
        return

    session = Session(bind=connection)

    try:
        is_bulk_inserting = True
        permission_list = Permission.list_permission()

        for permission in permission_list:
            resource_name = f"{target.resource}:{permission.name}"
            new_resource = Resources(
                resource=resource_name,
                is_visible=False,
                path=None,
                name=None,
                uuid=uuid.uuid4(),
            )
            try:
                session.merge(new_resource)
                session.commit()
            except IntegrityError:
                session.rollback()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        is_bulk_inserting = False
        session.close()
