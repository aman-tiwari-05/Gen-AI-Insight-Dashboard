import streamlit as st 
import pandas as pd 
from llamaapi import LlamaAPI

import matplotlib


def chat_with_csv(query,history):
    llm = LlamaAPI('LL-q6cmMq3sQBRU8ndjbum9DJab2MvhOytn7KzERtXuY1STwpWBWSdtNCNw1GCYmFqV')
    history.append({"role": "user", "content": query})

    api_request_json = {
    
            "messages": history
        }
    response=llm.run(api_request_json)
    response=response.json()["choices"][0]['message']['content']
    history.pop()
    if("List"  in query):
        response+="\nst.dataframe(result)"
   
    else:
        response+="\nst.success(result)"
    print(response)
    exec(response)
    
    


st.set_page_config(layout='wide')
st.title("Chat With CSV")

input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)

if input_csvs:
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
    selected_index = [file.name for file in input_csvs].index(selected_file)

    st.info("CSV uploaded successfully")
    
    data = pd.read_csv(input_csvs[selected_index])
    
    history=[
        {"role": "system", "content": f"""As a Data Scientist assistant, you're proficient in Python and adept at generating insights using libraries like Pandas, Numpy, and Matplotlib based on user queries.

Given information about a CSV dataset including its columns, rows, and user queries, your task is to return the Python code that fulfills those queries.\n # Assume 'data' is the name of the DataFrame storing the CSV data\n Ensure:
\n Information about the data set is: {data.info()} and sample data set is {data.head()}
The Python code returned contains column or row names identical to the provided dataset information.\n
Do not include code to read/import files, as they're already imported.\n
The final result or answer that user wants  should be stored in the variable 'result'.\n
Do not return any other statement apart from the required python code as the user want to execute the response as python code provided by you
and don't forget to Print the final result in your response. \n Just return your response as  the python executable code \n Make sure that final result should have balance paranthesis or bracket  and can be executed successfully make sure this error doesn't occurs: 'closing parenthesis ']' does not match opening parenthesis '(''
"""},]
    
    st.dataframe(data.head(3),use_container_width=True)

    st.info("Chat Below")
    input_text = st.text_area("Enter the query")

    if input_text:
        if st.button("Chat with csv"):
            st.info("Your Query: "+ input_text)
            chat_with_csv(input_text,history)
            

















   
        
      


# How many time Mumbai Indians have won the matches?   Which are the top 5 teams which has won most number of matches?     Which venue has hosted most number of matches


     