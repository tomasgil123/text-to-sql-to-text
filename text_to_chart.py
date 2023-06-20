import openai
import re
import streamlit as st

def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

def print_chart_to_screen(text):
    # if this fails, we want to print the error message to the screen
    try:
        delimiter = "####"
        system_message = f"""
            You are expert at making charts with python code. Given a user text you need 
            to come up with only one string that must be executed with python exec() function and output a chart.
            Data necessary to build the charts should be included inside the string that goes inside the exec() function. 
            The user text will be delimited with four hashtags,\ i.e. {delimiter}.
        """
        messages =  [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{delimiter}{text}{delimiter}"},  
        ]
        response = get_completion_from_messages(messages)

        parsed_response = re.search(r"```(.*?)```", response, re.DOTALL).group(1)
        # lets replace plt.show in the string by st.pyplot(plt.gcf()) in order for it to work
        parsed_response = parsed_response.replace("plt.show()", "st.pyplot(plt.gcf())")
        exec(parsed_response)
    except Exception as err:
        st.write(err)