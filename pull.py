#!/usr/bin/python3
# Grab data from the Riff.CC MySQL service and render it to the Curator's PostgreSQL database

# Credits:
#  - https://stackoverflow.com/questions/10195139/how-to-retrieve-sql-result-column-value-using-column-name-in-python
#  - https://github.com/PyMySQL/PyMySQL
#  - https://stackoverflow.com/questions/37926717/psycopg2-unable-to-insert-into-specific-columns

# Import needed modules
from __future__ import with_statement
import os, sys, yaml
import pymysql.cursors
import psycopg2

# Set our API key
from pathlib import Path
apiname = os.path.expanduser('~/.rcc-api')
apitoken = Path(apiname).read_text()

# Dynamically load in our magic config files
configname = os.path.expanduser('~/.rcc-tools.yml')
config = yaml.safe_load(open(configname))

# Check if the config is empty
if config is None:
    print("Failed to load configuration.")
    sys.exit(1338)

# Get our Riff.CC credentials and load them in
rccuser = config["rccuser"]
rccpass = config["rccpass"]
sqlpassword = config["password"]
curator_user = config["curator_user"]
curator_pass = config["curator_pass"]
curator_host = config["curator_host"]

# Connect to the Unit3D database
connection = pymysql.connect(host='localhost',
                             user='unit3d',
                             password=sqlpassword,
                             database='unit3d',
                             cursorclass=pymysql.cursors.DictCursor)

# Connect to the Curator database
connpg = psycopg2.connect(host=curator_host,
                          database="collection",
                          user=curator_user,
                          password=curator_pass)

# create a cursor
cursorpg = connpg.cursor()

# execute a statement
print('PostgreSQL database version:')
cursorpg.execute('SELECT * FROM releases')
record = cursorpg.fetchall()
print(record)

with connection:
    with connection.cursor() as cursor:
        # Read everything from Unit3D (traditional site)
        sql = "SELECT * FROM `torrents` WHERE id=1"
        cursor.execute(sql)
        result_set = cursor.fetchall()
        for row in result_set:
            print("hello")
            release_id = row["id"]
            name = row["name"]
            slug = row["slug"]
            description = row["description"]
            mediainfo = row["mediainfo"]
            category_id = row["category_id"]
            uploader_id = row["user_id"]
            featured = row["featured"]
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            type_id = row["type_id"]
            ipfs_hash = row["stream_id"]
            resolution_id = row["resolution_id"]
            print("Processing id "+ str(id))
            print("Name:" + name + " uploader_id: " + str(uploader_id) + " ipfs hash " + ipfs_hash)

            # cursorpg.execute
            print('''INSERT INTO releases
                (id, name, category_id, type_id, resolution_id, uploader_id, featured, created_at, updated_at, description, mediainfo, slug, ipfs_hash)
                VALUES ("{release_id}", "{name}", "{category_id}", "{type_id}", "{resolution_id}", "{uploader_id}", "{featured}", "{created_at}", "{updated_at}", "{description}", "{mediainfo}", "{slug}", "{ipfs_hash}"));
                '''.format(release_id=release_id,name=name,category_id=category_id,type_id=type_id,resolution_id=resolution_id,uploader_id=uploader_id,featured=featured,created_at=created_at,updated_at=updated_at,description=description,mediainfo=mediainfo,slug=slug,ipfs_hash=ipfs_hash))
            # Dump it into The Curator (new prototype)
