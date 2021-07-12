import csv
import os
import shutil

import mysql.connector

from definitions import (postmetadataNames, postTypes, wp_postInsert,
                         wp_postmetadataInsert)
from models.product import Product


def getProductsFromCsv(path):
    products: list[Product] = []

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                products.append(
                    Product(row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
                line_count += 1
        print(f'Processed {line_count} lines.')
    return products


def makeStringUsableForSQLSyntax(value: str):
    value = value[0]
    return value


# for turkish language
def makeUrlFriendlyStringFromValue(value: str):
    value = makeStringUsableForSQLSyntax(value)
    value = value.lower().replace("ı", "i").replace("ş", "s").replace(
        "ğ", "g").replace("ç", "c").replace("ö", "o").replace("ü", "u").replace(" ", "-")

    return value


def createMySqlConnection(host, user, password):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    # host="localhost",
    #     user="root",
    #     password="12345"


def insertPostMetas(mycursor, product, insertedProductRowId, insertedImageIds):
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["Price"], meta_value=makeStringUsableForSQLSyntax(product.regularPrice)))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["SalePrice"], meta_value=makeStringUsableForSQLSyntax(product.salePrice)))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["RegularPrice"], meta_value=makeStringUsableForSQLSyntax(product.regularPrice)))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["SKU"], meta_value=makeStringUsableForSQLSyntax(product.SKU)))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["StockStatus"], meta_value="instock"))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["Stock"], meta_value=makeStringUsableForSQLSyntax(product.stock)))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["TotalSales"], meta_value=0))
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["ManageStock"], meta_value="yes"))
    images = ""
    for i in range(len(insertedImageIds)):
        if(i == 0):
            mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                          meta_key=postmetadataNames["Thumbnail"], meta_value=insertedImageIds[i]))
        else:
            images += str(insertedImageIds[i]) + ","
    mycursor.execute(wp_postmetadataInsert.format(post_id=insertedProductRowId,
                                                  meta_key=postmetadataNames["Image"], meta_value=images.removesuffix(",")))


def writeFile(path, content):
    # if not os.path.exists(path):
    #     os.mkdir(os.path.curdir + "/" + path)

    with open(path, 'wb') as f:
        f.write(content)


def moveFile(source, destination):

    original = source
    target = destination

    shutil.move(original, target)
