from src import Database
import sys


if __name__ == "__main__":
    status, code, msg = Database.checkDatabase()
    if status:
        print("Connected to Database ")
        sys.exit()
    if code != "f405":
        print("Connect to database failed: %s" % msg)
        sys.exit()
    res = Database.createTables()
    print(res)
    print("Connected to Database; Tables Created ");