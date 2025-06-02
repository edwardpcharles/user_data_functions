import fabric.functions as fn

udf = fn.UserDataFunctions()

@udf.connection(argName="sqlDB",alias="sqldb")
@udf.function()
def updatePrice(sqlDB: fn.FabricSqlConnection, tableArry: list, price: str) -> str:
    connection = sqlDB.connect()
    cursor = connection.cursor()
    new_price = 0
    try:
        new_price = int(price)
    except:
        raise fn.UserThrownError("Please enter a integer.")
    for product in tableArry:
        update_data = (new_price, product)
        update_query = f"UPDATE [dbo].[product_dim] SET [List Price] = ? WHERE [Product ID] = ?;"
        cursor.execute(update_query, update_data)
        connection.commit() 

    cursor.close()
    connection.close()   

    return "Product Pricing Updated"
