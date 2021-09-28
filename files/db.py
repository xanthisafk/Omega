import psycopg2

class PostgreSQL():
    # Init will attemp to connect
    def __init__(self,DB_NAME:str = None, DB_USER:str = None, DB_PASS:str = None, DB_HOST:str = None):
        """
        Creates a postgreSQL object.

        args:
            DB_NAME: str -> Name of database
            DB_USER: str -> Username for connection
            DB_PASS: str -> Password of user
            DB_HOST: str -> URL of host to connect
        returns:
            None
        """
        self.conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        self.cur = self.conn.cursor()

    # connect if randomly disconnect
    async def connect(self, DB_NAME:str = None, DB_USER:str = None, DB_PASS:str = None, DB_HOST:str = None):
        """
        Create a connection.

        args:
            DB_NAME: str -> Name of database
            DB_USER: str -> Username for connection
            DB_PASS: str -> Password of user
            DB_HOST: str -> URL of host to connect
        returns:
            None
        """
        try:
            self.conn.close()
        except: pass

        self.conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST)
        self.cur = self.conn.cursor()
    
    # close connection
    async def close(self):
        """
        Close the connection with database.

        args:
            None
        returns:
            None
        """
        self.conn.close()

    # commit changes
    async def commit(self):
        """
        Commits the changes to database.

        args:
            None
        returns:
            None
        """
        self.conn.commit()

    # execute changes
    async def execute(self,string:str):
        """
        Excutes the string passed.
        
        args:
            string:str -> String that will be executed
        returns:
            response:list/tuples -> Returns the result
        """
        self.cur.execute(string)
        try:
            response = self.cur.fetchall()
        except Exception as e:
            if isinstance(e,psycopg2.ProgrammingError):
                response = e
            else:
                print(e)
                response = e
        return response
    
    # fetch string
    async def fetch(self,string:str):
        """
        Fetches the given string and returns the response.

        args:
            None
        returns:
            None
        """
        response = self.execute(string)
        return response

    # create a fetch string from given data
    async def string_fetch(self,row,table,column=None,value=None):
        """
        Create a string based on arguments given and then fetch the response.

        args:
            row: str -> name of row to be searches

        returns:
            response: list of tupeles -> Containing all the fetched data.
        """
        string = f"SELECT {row} FROM {table}"

        if column is not None and type(value) == int:
            string += f" WHERE {column} = {value}"
        if column is not None:
            string += f" WHERE {column} = '{value}'"

        self.cur.execute(string)
        response = self.cur.fetchall()
        return response

    # create an insert string from given data
    async def insert(self,table,fields,values,row=None,data=None):
        """
        Create a string of text and execute it.

        args:
            table: str -> name of table to work in
            fields: str/list -> name of field(s) that will be inserted. Can be list
            values: str/int/list -> name of value(s) to be inserted. Can be list

            optional:
                row:str -> row name for "WHERE" clause
                data: str/int -> value of `row` for "WHERE" clause
        
        returns
            string: str -> Generated string
        """
        s1 = f"INSERT INTO {table} "

        s2 = " ("
        if isinstance(fields,list):
            for i in fields:
                s2+=f"{i},"
            s2 = s2[:-1]+") "
        else:
            s2 = f"({fields}) "

        s3 = "VALUES ("
        if isinstance(values,list):
            for i in values:
                if isinstance(i,int):
                    s3+=f"{i},"
                elif isinstance(i,str):
                    s3+=f"'{i}',"
            s3 = s3[:-1]+") "
        else:
            if isinstance(values,int):
                s3 = f"VALUES ({values}) "
            elif isinstance(values,str):
                s3 = f"VALUES ('{values}') "

        string = s1+s2+s3

        if row is not None:
            s4 = f"WHERE {row} = "
            if isinstance(data,str):
                s4+=f"'{data}'"
            else:
                s4+=data
            string = string + s4
        
        self.cur.execute(string)
        return string 