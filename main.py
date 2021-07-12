
import os
import uuid
from sys import path

import requests

from definitions import (fileMovePath, postmetadataNames, postTypes,
                         wp_postInsert, wp_postmetadataInsert)
from helper import (createMySqlConnection, getProductsFromCsv, insertPostMetas,
                    makeStringUsableForSQLSyntax,
                    makeUrlFriendlyStringFromValue, moveFile, writeFile)

dbHost = "localhost"
dbUser = "root"
dbPassword = "12345"


importDateToWrite = "2021-07-12"

# getting products from csv file
products = getProductsFromCsv('products.csv')
# creating mysql connection
mydb = createMySqlConnection(dbHost, dbUser, dbPassword)

mycursor = mydb.cursor()


for product in products:
    productInsertSql = wp_postInsert.format(
        # Admin Id. Must change it to your user id
        post_author="1",
        post_parent=0,
        post_type=postTypes[0],
        post_date=importDateToWrite,
        post_content=makeStringUsableForSQLSyntax(product.description),
        post_title=makeStringUsableForSQLSyntax(product.name),
        # post_name is the url for that product. It must be friendly url. I'm translating from Turkish
        post_name=makeUrlFriendlyStringFromValue(product.name),
        post_status="publish",
        comment_status="open",
        comment_count=0,
        post_mime_type=" ",
        ping_status="closed",
        post_excerpt=" ",
        to_ping=" ",
        pinged=" ",
        post_content_filtered=" ")
    mycursor.execute(productInsertSql)

    insertedProductRowId = mycursor.lastrowid



    # need to change this part to your image handling
    insertedImageIds = []

    images = product.images.split(";")
    for image in images:
        imageId = uuid.uuid4()
        imageName = os.path.basename(image)
        changedImageName = imageId.__str__()+"-" + imageName
        # downloading image from url
        receive = requests.get(image)
        path = "images" + "/" + changedImageName
        # write downloaded image to a file
        writeFile(path, receive.content)
        insert = wp_postInsert.format(
            # Admin Id. Must change it to your user id
            post_author="1",
            post_parent=insertedProductRowId,
            post_type=postTypes[1],
            post_date=importDateToWrite,
            post_content="",
            post_title=imageName,
            post_name=changedImageName,
            # post_status must be inherit for media. If not media page not show inserted images
            post_status="inherit",
            comment_status="open",
            comment_count=0,
            post_mime_type="image/jpeg",
            ping_status="closed",
            post_excerpt="",
            to_ping="",
            pinged="",
            post_content_filtered=""
        )
        mycursor.execute(insert)
        lastImageId = mycursor.lastrowid
        insertedImageIds.append(lastImageId)
        moveFile(path, fileMovePath)
        mycursor.execute(wp_postmetadataInsert.format(post_id=lastImageId,
                                                      meta_key=postmetadataNames["_wp_attachment_image_alt"], meta_value=imageName))
        mycursor.execute(wp_postmetadataInsert.format(post_id=lastImageId,
                                                      meta_key=postmetadataNames["_wp_attached_file"], meta_value="2021/07/"+changedImageName))

    insertPostMetas(mycursor, product, insertedProductRowId, insertedImageIds)
