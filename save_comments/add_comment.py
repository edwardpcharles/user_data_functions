import fabric.functions as fn

udf = fn.UserDataFunctions()

@udf.connection(argName="sqlDB",alias="sqldb")
@udf.function()
def AddAnnotation(sqlDB: fn.FabricSqlConnection, commentdatetime: str, salespo: str, user: str, comment: str) -> str:
    
    data = (commentdatetime, user, salespo, comment,"1900-12-31")
 
    connection = sqlDB.connect()
    cursor = connection.cursor()    

    if(salespo=="" or len(salespo) < 1):
        raise fn.UserThrownError("Please Select a PO on the table to add a comment")
 
    
    insert_query = "INSERT INTO [dbo].[report_comments] ([commentdatetime],[user_id],[sales_po],[comment], [update_date_time]) VALUES (?, ?, ?, ?, ?);"
    cursor.execute(insert_query, data)
    connection.commit()
    connection.close()               
    return "Comment was successfully added"
