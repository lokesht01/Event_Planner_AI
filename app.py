import streamlit as st
from dotenv import load_dotenv
from flow import run_flow
import os

load_dotenv()

st.set_page_config(page_title="Event Planner", layout="wide")

st.title("AI Event Planner")
st.markdown("*Plan your perfect event with AI-powered venue, logistics, and marketing recommendations*")

# Check if API keys are configured
azure_key = os.getenv("AZURE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if not azure_key and not openai_key:
    st.error("No API keys found! Please configure your .env file with either AZURE_API_KEY or OPENAI_API_KEY")
    st.stop()

# Input form
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("🎯 Event Topic", 
                          help="What is your event about?")
    city = st.text_input("📍 Event City",
                         help="Where will the event take place?")

with col2:
    participants = st.number_input("👥 Expected Participants", 
                                   min_value=10, max_value=10000,
                                   help="How many people do you expect?")
    date = st.date_input("📅 Event Date")

st.markdown("---")

if st.button("Generate Event Plan", type="primary", use_container_width=True):
    if not topic or not city:
        st.warning("Please fill in all required fields!")
    else:
        inputs = {
            "event_topic": topic,
            "event_city": city,
            "expected_participants": int(participants),
            "tentative_date": str(date),
        }
        
        with st.spinner("AI agents are working on your event plan..."):
            result = run_flow(inputs)
        
        if isinstance(result, dict) and result.get("status") == "error":
            st.error(f"❌ {result.get('message')}")
            with st.expander("Error Details"):
                st.code(result.get('error_type', 'Unknown error'))
        else:
            st.success("Event plan generated successfully!")
            
            # Display results in tabs
            if isinstance(result, dict):
                if "venue_recommendation" in result:
                    tab1, tab2, tab3 = st.tabs(["🏢 Venue", "📦 Logistics", "📱 Marketing"])
                    
                    with tab1:
                        st.markdown("### Venue Recommendation")
                        st.markdown(result["venue_recommendation"])
                    
                    with tab2:
                        st.markdown("### Logistics Plan")
                        st.markdown(result["logistics_plan"])
                    
                    with tab3:
                        st.markdown("### Marketing Strategy")
                        st.markdown(result["marketing_plan"])