import streamlit as st

import json
import os
from datetime import datetime

classes = ["O1","O2","O3","O4","O5"]

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def next_step():
    st.session_state.step += 1

def previous_step():
    st.session_state.step -= 1

def display_questions(step, paper):
    question = paper.get_question(step)
    st.markdown(
       f"## Question {question.identifier}"
    )
    with st.container(border=True):
        display_question_parts(question)

def display_question_parts(question, prefix="mark",level=0):
    current_prefix = f"{prefix}_{question.identifier}"

    for index, item in enumerate(question._subparts):
        if level == 0:
            st.markdown(f"### {item.identifier})")
        if not item.marks:
            display_question_parts(item,current_prefix, level+1)
        else:
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    if not level ==0:
                        st.markdown(f"**{item.identifier})**")
                with col2:
                    res_key = f"{current_prefix}_{item.identifier}"
                    #initialise the result key if it doesn't exist
                    if res_key not in st.session_state.results: 
                        st.session_state.results[res_key] = 0

                    saved_value = st.session_state.results.get(res_key, 0)
                    options = list(range(item.marks + 1))
                    try:
                        current_index = options.index(saved_value)
                    except ValueError:
                        print("ValueError")
                        current_index = 0
                    choice = st.radio(
                        "Marks", 
                        options = options, 
                        horizontal=True, 
                        key=res_key, 
                        label_visibility="collapsed",
                        index=current_index,
                        disabled=st.session_state.submitted
                        )
                    st.session_state.results[res_key] = choice
                st.markdown('<div class="sub-part-line"></div>', unsafe_allow_html=True)


def Create_form(paper):

    local_css("style.css")

    if 'step' not in st.session_state:
        st.session_state.step=0
    if "results" not in st.session_state:
        st.session_state.results = {}

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    if st.session_state.submitted and st.session_state.step == paper.get_length():
        st.balloons()
    

    with st.container():
        if st.session_state.step ==0:
            class_index=None
            if st.session_state.results.get('class'):
                class_index = classes.index(st.session_state.results.get('class'))
            st.title(f"{paper.identifier}")
            st.markdown("---")
            std_name = st.text_input("Full Name:",value =st.session_state.results.get('name') ,disabled=st.session_state.submitted )
            std_class = st.selectbox ("class", options = classes,index = class_index , disabled=st.session_state.submitted)

        if 0 <= st.session_state.step <= paper.get_length()-1:
            st.markdown(
            """ 
            Enter your marks below, question by question. 
            """
            )
            display_questions(st.session_state.step,paper)

        if 0 == st.session_state.step:
            col1, col2, col3 = st.columns([1,2,1])
            with col3:
                if st.button( "Next ➡", type="primary"):
                    if std_name and std_class:
                        st.session_state.results['name'] = std_name
                        st.session_state.results['class'] = std_class
                        next_step()
                        st.rerun()
                    else:
                        st.error("Please enter your name and class to continue.")

        if 1 <= st.session_state.step <= paper.get_length()-1:
            
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("⬅ Back"):
                    previous_step()
                    st.rerun()
            with col3:
                if st.button("Next ➡", type="primary"):
                    next_step()
                    st.rerun()


        if st.session_state.step == paper.get_length():
            st.title("Review & Submit")
            st.write(f"Name: {st.session_state.results.get('name')}")
            st.write(f"Your Answers: {st.session_state.results}")
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("⬅ Back"):
                    previous_step()
                    st.rerun()

            with col3:
                if st.button("Submit", disabled=st.session_state.submitted):
                # This is where you would call your SQL/SharePoint save function

                    st.session_state.submitted = True
                    saved_path = save_submission(paper.identifier,st.session_state.results)
                    
                    st.success("Results submitted successfully!")
                    st.rerun()


def save_submission(paper_id, data):
    # Create a results folder if it doesn't exist
    path =f"results/{paper_id}/raw"
    if not os.path.exists(path):
        os.makedirs(path)
    
    # Structure the final record
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "paper_id": paper_id,
        "student_name": data.get('name', 'Unknown'),
        "student_class": data.get('class', 'Unknown'),
        "marks": {key: data[key] for key in data if "mark_" in key }
    }
    filename = f"{record['student_class']}_{record['student_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(path, filename)
    
    with open(filepath, "w") as f:
        json.dump(record, f, indent=4)
    
    return filepath    

