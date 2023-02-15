import sqlite3
from google_play_scraper import search
import cgi

# Retrieve the search query from the HTTP GET parameters
form = cgi.FieldStorage()
query = form.getvalue("query", "")

try:
    sqliteConnection = sqlite3.connect('apptable.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    #get results
    val = input("Enter Keyword to Search Google Play Store: ")

    result = search(
        val,
        lang="en",  # defaults to 'en'
        country="us",  # defaults to 'us'
        n_hits=30  # defaults to 30 (= Google's maximum)
    )

    r = result[0]

    #appid, title, etc
    keys = r.keys()

    #get all values
    for row in result:
        values = row.values()
        arr = []
        for v in values:
            arr.append(v)
        print(arr[0])
        count = cursor.execute('''INSERT INTO apps ('appID', 'title', 'rating', 'genre', 'price', 'developer', 'downloads','icon') VALUES (?,?,?,?,?,?,?,?)''', arr)
        sqliteConnection.commit()
        print("Record inserted successfully into apps table ", cursor.rowcount)
    cursor.close()


#cannot connect:
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")





# Connect to the SQLite database
conn = sqlite3.connect("products.db")

# Execute a SELECT statement to retrieve the products that match the query
cursor = conn.execute("SELECT name, description, price FROM products WHERE name LIKE ?", ("%" + query + "%",))
products = cursor.fetchall()

# Output the search results as an HTML table
print("Content-type: text/html\n")
print("<table>")
print("<tr><th>Name</th><th>Description</th><th>Price</th></tr>")
for product in products:
    print("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(*product))
print("</table>")



