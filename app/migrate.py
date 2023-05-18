from models.models import (Base,Admin)
from utils.database import *
from passlib.context import CryptContext
from sqlalchemy import text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

database = Database()
engine = database.get_db_connection()
db = database.get_db_session(engine)

Base.metadata.create_all(bind=engine)



# SEEDING STAFF DATA INTO DATABASE

db_addStaff = Admin()
db_addStaff.admin_name = "Super Admin"
db_addStaff.email = "admin@admin.com"
db_addStaff.password = pwd_context.hash("password")
db_addStaff.contact = "0245678987",
db_addStaff.status = "Active"
db.add(db_addStaff)









# TRIGGER

# sqls = ["""\

# CREATE TRIGGER after_insert_courseBatch_insert_staff_role AFTER INSERT ON course_batch FOR EACH ROW BEGIN

#     IF (NEW.status = 'Active')
#     THEN

# INSERT into staff_role(staff_role.status, staff_role.batch_id, staff_role.course_id, staff_role.module_name)

# SELECT NEW.status, NEW.id, NEW.course_id, modules.module_name
# FROM modules where modules.course_id = NEW.course_id GROUP by modules.module_name ORDER by modules.module_name;

#     END IF;

# END
# """

#     ]


# if engine.name == "mysql":
#         print("mysql detected")
#         sqls
# else:
#         print("assuming sqlite")

# for sql in sqls:
#         db.execute(text(sql))


db.flush()
db.commit()
db.close()
