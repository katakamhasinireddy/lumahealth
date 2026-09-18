import streamlit as st
from google import genai
client = genai.Client()
from PIL import Image

st.title("🛡️ LumaHealth")
st.write("Your wellness companion and safety layer.")

food_tab, chat_tab, sensor_tab = st.tabs(
    ["🍎 Food", "💬 Health Chat", "⌚ Sensor"]
)
with food_tab:
    st.write("Upload a photo of your meal for an estimated nutrition analysis.")

    uploaded_file = st.file_uploader(
        "Upload your food image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your meal")

        if st.button("🔍 Analyze Meal"):

            client = genai.Client()

            food_prompt = """
    Look at this food image.

    Identify the food items and give an approximate estimate of:
    - Calories
    - Protein
    - Carbohydrates
    - Fat

    Keep the answer short and easy to read.

    These are estimates only because the exact portion size,
    ingredients, and preparation method cannot be determined from
    an image.
    """

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[image, food_prompt]
            )

            st.subheader("📊 Estimated Nutrition")
            st.write(response.text)
with chat_tab:
    st.subheader("💬 Health Chat")

    user_message = st.text_input(
        "How are you feeling?"
    )

    if st.button("Send"):
        client = genai.Client()

        prompt = f"""
        You are a safe health and wellness assistant.

        User message: {user_message}

        Classify it as:
        WELLNESS, NUTRITION, or URGENT.

        Give a short, helpful response.
        Do not diagnose medical conditions.
        If the message sounds urgent, clearly recommend
        seeking appropriate medical care.""" 
try:        
    response = client.models.generate_content(
       model="gemini-3.8-flash",
       contents=prompt
    )
except Exception as e:
    st.error(f"Error generating response: {e}")
    response = None
if response: 
    st.write(response.text)    
with sensor_tab:
    st.subheader("⌚ Sensor Monitoring")

    # Synthetic heart-rate data
    heart_rate = [72, 75, 74, 78, 76, 125, 77]

    st.write("Synthetic heart-rate readings:")
    st.line_chart(heart_rate)

    latest_hr = heart_rate[-1]
    st.metric("Latest Heart Rate", f"{latest_hr} BPM")

    if latest_hr > 120:
        st.warning("⚠️ Unusual sensor pattern detected.")
        st.info("This is an automated alert based on synthetic demo data.")
    else:
        st.success("✅ No unusual sensor pattern detected.")

    st.divider()

    # Steps Tracker
    st.subheader("🚶 Steps Tracker")

    steps = 6840
    step_goal = 10000

    st.metric("Today's Steps", f"{steps:,}")

    progress = min(steps / step_goal, 1.0)
    st.progress(progress, text=f"{steps:,} / {step_goal:,} steps")

    remaining = max(step_goal - steps, 0)

    if steps >= step_goal:
        st.success("🎉 Step goal reached!")
    else:
        st.info(f"Keep going! {remaining:,} steps remaining.")
    st.divider()

    