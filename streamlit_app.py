import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Set page config
st.set_page_config(
    page_title="Introvert or Extrovert Quiz",
    page_icon="🤔",
    layout="centered"
)

# Quiz questions and options
questions = [
    {
        "question": "How do you typically recharge after a long day?",
        "options": [
            ("Spending time alone reading or relaxing", 0),
            ("Meeting friends or engaging in social activities", 2),
            ("A mix of both, depending on my mood", 1)
        ]
    },
    {
        "question": "In group settings, you usually:",
        "options": [
            ("Prefer to listen and observe", 0),
            ("Lead conversations and share stories", 2),
            ("Participate when the topic interests you", 1)
        ]
    },
    {
        "question": "Your ideal weekend would be:",
        "options": [
            ("Staying home with a good book or movie", 0),
            ("Going out to parties or social events", 2),
            ("A balance of social time and alone time", 1)
        ]
    },
    {
        "question": "When solving problems, you prefer to:",
        "options": [
            ("Think it through on your own", 0),
            ("Discuss it with others", 2),
            ("Research first, then maybe consult others", 1)
        ]
    },
    {
        "question": "In social situations, you tend to:",
        "options": [
            ("Feel drained after extended interaction", 0),
            ("Feel energized by meeting new people", 2),
            ("Enjoy it but need breaks occasionally", 1)
        ]
    }
]

def calculate_result(scores):
    total_score = sum(scores)
    max_possible = len(questions) * 2
    percentage = (total_score / max_possible) * 100
    
    if percentage <= 33:
        return "Introvert", percentage
    elif percentage >= 66:
        return "Extrovert", percentage
    else:
        return "Ambivert", percentage

def create_result_image(personality_type, score):
    # Create a new image with a white background
    width = 800
    height = 400
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Add decorative elements
    draw.rectangle([0, 0, width, height], fill='white', outline='black', width=5)
    
    # Add text
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        # Fallback to default font if arial is not available
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw the personality type
    text = f"You are an {personality_type}!"
    text_width = draw.textlength(text, font=font_large)
    draw.text(
        ((width - text_width) / 2, 100),
        text,
        fill='black',
        font=font_large
    )
    
    # Draw the score
    score_text = f"Score: {score:.1f}%"
    score_width = draw.textlength(score_text, font=font_small)
    draw.text(
        ((width - score_width) / 2, 200),
        score_text,
        fill='black',
        font=font_small
    )
    
    return image

def main():
    st.title("🤔 Introvert or Extrovert Quiz")
    st.write("Answer these questions to discover where you fall on the introvert-extrovert spectrum!")
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.scores = []
        st.session_state.quiz_completed = False
    
    if not st.session_state.quiz_completed:
        if st.session_state.current_question < len(questions):
            q = questions[st.session_state.current_question]
            st.subheader(f"Question {st.session_state.current_question + 1}")
            st.write(q["question"])
            
            # Create radio buttons for options
            options = [opt[0] for opt in q["options"]]
            scores = [opt[1] for opt in q["options"]]
            choice = st.radio("Choose your answer:", options, key=f"q_{st.session_state.current_question}")
            
            if st.button("Next" if st.session_state.current_question < len(questions)-1 else "Finish"):
                score = scores[options.index(choice)]
                st.session_state.scores.append(score)
                
                if st.session_state.current_question == len(questions)-1:
                    st.session_state.quiz_completed = True
                else:
                    st.session_state.current_question += 1
                st.rerun()
                
        if st.button("Start Over"):
            st.session_state.current_question = 0
            st.session_state.scores = []
            st.session_state.quiz_completed = False
            st.rerun()
    
    if st.session_state.quiz_completed:
        personality_type, score = calculate_result(st.session_state.scores)
        
        st.header("🎉 Your Results!")
        st.subheader(f"You are an {personality_type}!")
        
        # Create and display gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "Introvert-Extrovert Scale"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': "lightgray"},
                    {'range': [33, 66], 'color': "gray"},
                    {'range': [66, 100], 'color': "darkgray"}
                ]
            }
        ))
        st.plotly_chart(fig)
        
        # Create shareable image
        result_image = create_result_image(personality_type, score)
        
        # Convert image to bytes for download
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Create download button
        st.download_button(
            label="Download Your Result",
            data=img_byte_arr,
            file_name="personality_result.png",
            mime="image/png"
        )
        
        # Display personality description
        descriptions = {
            "Introvert": """
                As an introvert, you tend to:
                - Recharge by spending time alone
                - Think deeply before speaking
                - Prefer meaningful one-on-one conversations
                - Work well independently
            """,
            "Extrovert": """
                As an extrovert, you tend to:
                - Gain energy from social interactions
                - Think out loud and process externally
                - Enjoy group activities and meeting new people
                - Thrive in collaborative environments
            """,
            "Ambivert": """
                As an ambivert, you tend to:
                - Have a balanced approach to social interaction
                - Adapt well to different social situations
                - Enjoy both alone time and social activities
                - Switch between independent and collaborative work
            """
        }
        
        st.write(descriptions[personality_type])

if __name__ == "__main__":
    main()
