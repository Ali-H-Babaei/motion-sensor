# import pyodbc
# # from llama_index import VectorStoreIndex, Document, ServiceContext
# # from langchain.chat_models import ChatOpenAI

# from llama_index.core import VectorStoreIndex, ServiceContext, Document
# # from langchain.chat_models import ChatOpenAI

# # Step 1: Connect to the SQL database and fetch data
# conn_str = (
#     r'DRIVER={ODBC Driver 17 for SQL Server};'
#     r'SERVER=tcp:bbdbaus.database.windows.net,1433;'
#     r'DATABASE=BBDBAUS;'
#     r'UID=bbdbaus;'
#     r'PWD=Aliiscool1234!;'
# )

# conn = pyodbc.connect(conn_str)
# cursor = conn.cursor()
# query = "SELECT top 3 * FROM [dbo].[UserStories]"
# cursor.execute(query)
# rows = cursor.fetchall()

# # Step 2: Process SQL Data into Documents
# # Convert each row into a Document that LlamaIndex can understand.
# documents = []
# for row in rows:
#     # Each document is a formatted string of the row (you can enhance this)
#     doc_text = f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}"
#     # Updated to pass doc_text as a keyword argument
#     documents.append(Document(text=doc_text))

# # Step 3: Set up the LLM and create an index using LlamaIndex
# # Use Langchain's OpenAI LLM with LlamaIndex
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
# service_context = ServiceContext.from_defaults(llm=llm)

# # Step 4: Create the index (updated to use VectorStoreIndex)
# index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# # Step 5: Ask questions about the data
# query = "Which user stories have missing descriptions?"
# response = index.query(query)

# # Print the results
# print(response)

# # Close the database connection
# cursor.close()
# conn.close()

import requests
from bs4 import BeautifulSoup

# URL format with page number as a variable
base_url = "https://www.gran-turismo.com/gb/gt7/sportmode/event/10248/0/0/page/{}"
name_to_search = "BaeBae44"  # The name you're looking for

# Define a function to search for your name across pages
def search_name():
    page_num = 1
    while True:
        # Fetch the page content, bypass SSL verification
        url = base_url.format(page_num)
        response = requests.get(url, verify=False)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Could not retrieve page {page_num}. Stopping search.")
            break

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the name in the page
        if name_to_search.lower() in soup.text.lower():
            print(f"Name found on page {page_num}!")
            break
        else:
            print(f"Name not found on page {page_num}. Moving to the next page...")

        # Stop when there are no more pages or if name is found
        if "No results" in soup.text:  # You can adjust this check based on the site's content
            print(f"Reached the last page without finding the name.")
            break

        page_num += 1

# Run the search
search_name()