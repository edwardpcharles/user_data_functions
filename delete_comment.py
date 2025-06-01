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


@udf.connection(argName="sqlDB",alias="sqldb")
@udf.function()
def updateAnnotation(sqlDB: fn.FabricSqlConnection, primarykey: str, commentdatetime: str,  user: str, comment: str) -> str:
        
    if(primarykey=="" or len(primarykey) < 1):
        raise fn.UserThrownError("Please Select a comment in the table")   

    data = (primarykey)
 
    connection = sqlDB.connect()
    cursor = connection.cursor() 

    query = "SELECT [user_id] FROM [dbo].[report_comments] where commentid = ?"
    cursor.execute(query, data)

    try:
        user_id = str(cursor.fetchone()[0])
    except:
        raise fn.UserThrownError("Comment ID does not exist")   

    if(user != user_id):
        raise fn.UserThrownError("You were not the user who made this comment. You can't update it sorry...")

    update_data = (comment, commentdatetime, primarykey)
    update_query = "UPDATE [dbo].[report_comments] SET comment = ?, update_date_time = ? WHERE commentid = ?;"

    cursor.execute(update_query, update_data)

    connection.commit()
    connection.close()               
    return "Comment Updated"

@udf.connection(argName="sqlDB",alias="sqldb")
@udf.function()
def deleteAnnotation(sqlDB: fn.FabricSqlConnection, primarykey: str,  user: str) -> str:
        
    if(primarykey=="" or len(primarykey) < 1):
        raise fn.UserThrownError("Please Select a comment in the table")   

    data = (primarykey)
 
    connection = sqlDB.connect()
    cursor = connection.cursor() 

    query = "SELECT [user_id] FROM [dbo].[report_comments] where commentid = ?"
    cursor.execute(query, data)

    try:
        user_id = str(cursor.fetchone()[0])
    except:
        raise fn.UserThrownError("Comment ID does not exist")   

    if(user != user_id):
        raise fn.UserThrownError("You were not the user who made this comment. You can't update it sorry...")

    update_query = "delete from [dbo].[report_comments] WHERE commentid = ?;"

    cursor.execute(update_query, data)

    connection.commit()
    connection.close()               
    return "Comment Deleted"
