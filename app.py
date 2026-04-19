import json
import re
from pathlib import Path

import streamlit as st

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Fitness Coach", page_icon="💪", layout="wide")

# -------------------------
# STORAGE
# -------------------------
STORE_PATH = Path(__file__).with_name("progress_store.json")


def load_store() -> dict:
    if STORE_PATH.exists():
        try:
            return json.loads(STORE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_store(store: dict) -> None:
    try:
        STORE_PATH.write_text(json.dumps(store, indent=2), encoding="utf-8")
    except Exception:
        pass


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "guest"


# -------------------------
# SESSION STATE
# -------------------------
if "generated" not in st.session_state:
    st.session_state.generated = False

if "profile_name" not in st.session_state:
    st.session_state.profile_name = "Guest"

if "profile_id" not in st.session_state:
    st.session_state.profile_id = "guest"

if "weight" not in st.session_state:
    st.session_state.weight = 54.0

if "height" not in st.session_state:
    st.session_state.height = 175.0

if "goal" not in st.session_state:
    st.session_state.goal = "Muscle Gain"

if "experience" not in st.session_state:
    st.session_state.experience = "Beginner"

if "days" not in st.session_state:
    st.session_state.days = 6


# -------------------------
# STYLES
# -------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 1rem;
    }
    .panel {
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(255,255,255,0.04);
        margin-bottom: 12px;
    }
    .big-number {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="main-title">💪 Built for You ❤️navz❤️</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Workout plan, food plan, advice, and saved daily progress by profile name</div>',
    unsafe_allow_html=True,
)

# -------------------------
# HELPERS
# -------------------------
def bmi_status(bmi: float) -> str:
    if bmi < 18.5:
        return "🟢 Underweight → Bulk Mode"
    elif bmi < 25:
        return "🔵 Healthy range → Lean Muscle Mode"
    return "🟠 Overweight → Fat Loss Mode"


def calorie_factor(goal: str) -> int:
    if goal == "Muscle Gain":
        return 35
    if goal == "Weight Loss":
        return 25
    return 30


def protein_factor(goal: str) -> float:
    if goal == "Muscle Gain":
        return 2.0
    if goal == "Weight Loss":
        return 1.8
    return 1.6


def water_target_liters(weight_kg: float) -> float:
    return round(max(2.0, weight_kg * 0.035), 1)


def sets_for_experience(experience: str) -> str:
    if experience == "Beginner":
        return "3 sets × 10–12 reps"
    if experience == "Intermediate":
        return "4 sets × 8–12 reps"
    return "4–5 sets × 6–10 reps"


def meal_plan(goal: str) -> str:
    if goal == "Muscle Gain":
        return """
**Breakfast:** Oats + milk + banana + 3–4 eggs  
**Lunch:** Rice + chicken / paneer + vegetables  
**Snack:** Peanut butter sandwich / curd / nuts  
**Dinner:** Rice / roti + protein source + salad  
**Before bed:** Milk or curd
"""
    if goal == "Weight Loss":
        return """
**Breakfast:** Eggs / oats / fruit  
**Lunch:** Smaller rice portion + dal + vegetables + protein  
**Snack:** Curd / sprouts / nuts (small)  
**Dinner:** Light meal with more protein and fewer carbs  
**Avoid:** sugary drinks, junk food, late-night overeating
"""
    return """
**Breakfast:** Eggs / oats / idli / fruit  
**Lunch:** Rice / roti + dal + vegetables + protein  
**Snack:** Fruit / curd / nuts  
**Dinner:** Balanced meal with protein + vegetables  
**Rule:** stay consistent and avoid too much junk
"""


def advice_plan(goal: str, bmi: float) -> str:
    if bmi < 18.5:
        return "Eat more, train hard, and sleep well. Your body needs a calorie surplus to grow."
    if bmi < 25:
        return "Stay consistent, increase weights slowly, and keep your meals balanced."
    return "Stay in a calorie deficit, keep protein high, and add cardio regularly."


def build_workout(days: int, goal: str, experience: str):
    sets = sets_for_experience(experience)

    if goal == "Muscle Gain":
        if days == 3:
            return [
                ("Day 1: Full Body A", [
                    f"Squat — {sets}",
                    f"Bench Press — {sets}",
                    f"Lat Pulldown — {sets}",
                    "Plank — 3 × 30–45 sec",
                ]),
                ("Day 2: Rest / Light Walk", [
                    "20–30 min walking",
                    "Mobility / stretching",
                ]),
                ("Day 3: Full Body B", [
                    f"Deadlift — {sets}",
                    f"Incline Dumbbell Press — {sets}",
                    f"Dumbbell Row — {sets}",
                    f"Shoulder Press — {sets}",
                ]),
            ]

        if days == 4:
            return [
                ("Day 1: Upper Body", [
                    f"Bench Press — {sets}",
                    f"Row — {sets}",
                    f"Shoulder Press — {sets}",
                    f"Biceps Curl — {sets}",
                ]),
                ("Day 2: Lower Body", [
                    f"Squat — {sets}",
                    f"Romanian Deadlift — {sets}",
                    f"Lunges — {sets}",
                    f"Calf Raises — {sets}",
                ]),
                ("Day 3: Upper Body 2", [
                    f"Incline Press — {sets}",
                    f"Lat Pulldown — {sets}",
                    f"Lateral Raises — {sets}",
                    f"Triceps Pushdown — {sets}",
                ]),
                ("Day 4: Lower Body 2", [
                    f"Leg Press — {sets}",
                    f"Leg Curl — {sets}",
                    f"Bulgarian Split Squat — {sets}",
                    "Abs — 3 rounds",
                ]),
            ]

        if days == 5:
            return [
                ("Day 1: Chest + Triceps", [
                    f"Bench Press — {sets}",
                    f"Incline Press — {sets}",
                    f"Dips — {sets}",
                    f"Triceps Pushdown — {sets}",
                ]),
                ("Day 2: Back + Biceps", [
                    f"Pull-ups / Lat Pulldown — {sets}",
                    f"Barbell Row — {sets}",
                    f"Seated Row — {sets}",
                    f"Biceps Curl — {sets}",
                ]),
                ("Day 3: Legs", [
                    f"Squat — {sets}",
                    f"Romanian Deadlift — {sets}",
                    f"Leg Press — {sets}",
                    f"Calf Raises — {sets}",
                ]),
                ("Day 4: Shoulders + Abs", [
                    f"Shoulder Press — {sets}",
                    f"Lateral Raises — {sets}",
                    f"Rear Delt Fly — {sets}",
                    "Plank / Crunches — 3 rounds",
                ]),
                ("Day 5: Arms + Light Cardio", [
                    f"Barbell Curl — {sets}",
                    f"Hammer Curl — {sets}",
                    f"Close-Grip Pushups — {sets}",
                    "10–15 min light cardio",
                ]),
            ]

        return [
            ("Day 1: Push", [
                f"Bench Press — {sets}",
                f"Shoulder Press — {sets}",
                f"Triceps Pushdown — {sets}",
                f"Incline Press — {sets}",
            ]),
            ("Day 2: Pull", [
                f"Lat Pulldown — {sets}",
                f"Barbell Row — {sets}",
                f"Biceps Curl — {sets}",
                f"Face Pull — {sets}",
            ]),
            ("Day 3: Legs", [
                f"Squat — {sets}",
                f"Leg Press — {sets}",
                f"Leg Curl — {sets}",
                f"Calf Raises — {sets}",
            ]),
            ("Day 4: Push 2", [
                f"Incline Press — {sets}",
                f"Dumbbell Fly — {sets}",
                f"Lateral Raises — {sets}",
                f"Dips — {sets}",
            ]),
            ("Day 5: Pull 2", [
                f"Seated Row — {sets}",
                f"Pull-ups — {sets}",
                f"Rear Delt Fly — {sets}",
                f"Hammer Curl — {sets}",
            ]),
            ("Day 6: Legs + Core", [
                f"Deadlift / RDL — {sets}",
                f"Lunges — {sets}",
                "Abs circuit — 3 rounds",
                "10 min stretch",
            ]),
        ]

    if goal == "Weight Loss":
        if days == 3:
            return [
                ("Day 1: Full Body + Cardio", [
                    "Squat — 3 × 12",
                    "Pushups — 3 × 10",
                    "Row — 3 × 12",
                    "15–20 min brisk walk / cycling",
                ]),
                ("Day 2: Cardio + Core", [
                    "20–30 min cardio",
                    "Plank — 3 × 30 sec",
                    "Crunches — 3 × 15",
                ]),
                ("Day 3: Full Body + Cardio", [
                    "Lunges — 3 × 12",
                    "Shoulder Press — 3 × 12",
                    "Lat Pulldown — 3 × 12",
                    "15–20 min cardio",
                ]),
            ]

        if days == 4:
            return [
                ("Day 1: Upper Body", [
                    "Pushups — 3 × 12",
                    "Row — 3 × 12",
                    "Shoulder Press — 3 × 12",
                ]),
                ("Day 2: Cardio", [
                    "25–30 min brisk walking / cycling",
                    "Abs circuit — 3 rounds",
                ]),
                ("Day 3: Lower Body", [
                    "Squat — 3 × 12",
                    "Lunges — 3 × 12",
                    "Calf Raises — 3 × 15",
                ]),
                ("Day 4: Cardio + Core", [
                    "20–30 min cardio",
                    "Plank — 3 × 30 sec",
                    "Leg Raises — 3 × 15",
                ]),
            ]

        if days == 5:
            return [
                ("Day 1: Full Body", [
                    "Squat — 3 × 12",
                    "Bench / Pushups — 3 × 12",
                    "Row — 3 × 12",
                ]),
                ("Day 2: Cardio", [
                    "25–30 min cardio",
                    "Stretching — 10 min",
                ]),
                ("Day 3: Full Body", [
                    "Lunges — 3 × 12",
                    "Shoulder Press — 3 × 12",
                    "Plank — 3 × 30 sec",
                ]),
                ("Day 4: Cardio + Core", [
                    "20 min cardio",
                    "Crunches — 3 × 15",
                    "Leg Raises — 3 × 15",
                ]),
                ("Day 5: Full Body + Walk", [
                    "Squat — 3 × 12",
                    "Pushups — 3 × 10",
                    "30 min walk",
                ]),
            ]

        return [
            ("Day 1: Strength A", [
                "Squat — 3 × 12",
                "Pushups — 3 × 12",
                "Row — 3 × 12",
            ]),
            ("Day 2: Cardio", [
                "25–35 min cardio",
                "Mobility work",
            ]),
            ("Day 3: Strength B", [
                "Lunges — 3 × 12",
                "Shoulder Press — 3 × 12",
                "Plank — 3 × 30 sec",
            ]),
            ("Day 4: Cardio", [
                "25–35 min cardio",
                "Abs circuit — 3 rounds",
            ]),
            ("Day 5: Strength C", [
                "Deadlift (light) — 3 × 10",
                "Pushups — 3 × 12",
                "Lat Pulldown — 3 × 12",
            ]),
            ("Day 6: Walk + Recovery", [
                "30 min walk",
                "Stretching / yoga",
            ]),
        ]

    if days == 3:
        return [
            ("Day 1: Full Body", [
                "Squat — 3 × 10",
                "Pushups — 3 × 10",
                "Row — 3 × 10",
            ]),
            ("Day 2: Cardio + Mobility", [
                "20 min cardio",
                "Stretching — 10 min",
            ]),
            ("Day 3: Full Body", [
                "Lunges — 3 × 10",
                "Shoulder Press — 3 × 10",
                "Plank — 3 × 30 sec",
            ]),
        ]

    if days == 4:
        return [
            ("Day 1: Upper Body", [
                "Bench / Pushups — 3 × 10",
                "Row — 3 × 10",
                "Shoulder Press — 3 × 10",
            ]),
            ("Day 2: Lower Body", [
                "Squat — 3 × 10",
                "Lunges — 3 × 10",
                "Calf Raises — 3 × 15",
            ]),
            ("Day 3: Cardio", [
                "20–25 min cardio",
                "Stretching",
            ]),
            ("Day 4: Full Body", [
                "Deadlift (light) — 3 × 8",
                "Pushups — 3 × 10",
                "Plank — 3 × 30 sec",
            ]),
        ]

    if days == 5:
        return [
            ("Day 1: Upper Body", [
                "Bench / Pushups — 3 × 10",
                "Row — 3 × 10",
                "Biceps Curl — 3 × 12",
            ]),
            ("Day 2: Lower Body", [
                "Squat — 3 × 10",
                "Lunges — 3 × 10",
                "Calf Raises — 3 × 15",
            ]),
            ("Day 3: Cardio", [
                "25 min cardio",
                "Mobility",
            ]),
            ("Day 4: Full Body", [
                "Shoulder Press — 3 × 10",
                "Row — 3 × 10",
                "Plank — 3 × 30 sec",
            ]),
            ("Day 5: Recovery", [
                "Walk 20 min",
                "Stretching / yoga",
            ]),
        ]

    return [
        ("Day 1: Strength", [
            "Squat — 3 × 10",
            "Pushups — 3 × 10",
            "Row — 3 × 10",
        ]),
        ("Day 2: Cardio", [
            "20 min cardio",
            "Stretching",
        ]),
        ("Day 3: Strength", [
            "Lunges — 3 × 10",
            "Shoulder Press — 3 × 10",
            "Plank — 3 × 30 sec",
        ]),
        ("Day 4: Cardio", [
            "20 min cardio",
            "Recovery walk",
        ]),
        ("Day 5: Strength", [
            "Deadlift (light) — 3 × 8",
            "Pushups — 3 × 10",
            "Abs — 3 rounds",
        ]),
        ("Day 6: Recovery", [
            "Walk 20–30 min",
            "Stretching / mobility",
        ]),
    ]


# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("📥 Enter Details")

name_input = st.sidebar.text_input("Profile name", placeholder="Enter your name")
weight_input = st.sidebar.text_input("Weight (kg)", placeholder="e.g. 54")
height_input = st.sidebar.text_input("Height (cm)", placeholder="e.g. 175")

goal_input = st.sidebar.selectbox("Goal", ["Weight Loss", "Muscle Gain", "Maintain"])
experience_input = st.sidebar.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
days_input = st.sidebar.selectbox("Workout Days", [3, 4, 5, 6])

generate_clicked = st.sidebar.button("🚀 Generate / Update Plan")

if generate_clicked:
    try:
        weight_val = float(weight_input)
        height_val = float(height_input)

        if weight_val <= 0 or height_val <= 0:
            st.error("❌ Weight and height must be greater than zero.")
        else:
            st.session_state.generated = True
            st.session_state.profile_name = name_input.strip() or "Guest"
            st.session_state.profile_id = slugify(st.session_state.profile_name)
            st.session_state.weight = weight_val
            st.session_state.height = height_val
            st.session_state.goal = goal_input
            st.session_state.experience = experience_input
            st.session_state.days = days_input

    except ValueError:
        st.error("❌ Enter valid numbers for weight and height, like 54 and 175.")

# -------------------------
# MAIN OUTPUT
# -------------------------
if st.session_state.generated:
    profile_name = st.session_state.profile_name
    profile_id = st.session_state.profile_id
    weight = st.session_state.weight
    height = st.session_state.height
    goal = st.session_state.goal
    experience = st.session_state.experience
    days = st.session_state.days

    bmi = weight / ((height / 100) ** 2)
    calories = weight * calorie_factor(goal)
    protein = weight * protein_factor(goal)
    water = water_target_liters(weight)

    store = load_store()

    if profile_id not in store:
        store[profile_id] = {
            "name": profile_name,
            "goal": goal,
            "experience": experience,
            "days": days,
            "completed": [],
            "weeks": {},
            "weeks_completed": 0,
            "current_week": 1,
        }

    profile = store[profile_id]
    profile["name"] = profile_name
    profile["goal"] = goal
    profile["experience"] = experience
    profile["days"] = days
    profile.setdefault("completed", [])
    profile.setdefault("weeks", {})
    profile.setdefault("weeks_completed", 0)
    profile["current_week"] = int(profile.get("current_week", 1))

    save_store(store)

    week_token_key = f"week_token_{profile_id}"
    if week_token_key not in st.session_state:
        st.session_state[week_token_key] = profile["current_week"]

    week_token = int(st.session_state[week_token_key])

    current_week_data = profile.get("weeks", {}).get(str(week_token), {})
    saved_completed_days = set(current_week_data.get("completed_days", []))

    for day_num in range(1, days + 1):
        key = f"done_{profile_id}_w{week_token}_{day_num}"
        if key not in st.session_state:
            st.session_state[key] = day_num in saved_completed_days

    st.subheader(f"🔥 {profile_name}'s Fitness Plan — Week {week_token}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("BMI", round(bmi, 2))
    c2.metric("Calories", f"{int(calories)} kcal")
    c3.metric("Protein", f"{int(protein)} g")
    c4.metric("Water", f"{water} L")

    st.divider()

    status_msg = bmi_status(bmi)
    if bmi < 18.5:
        st.success(status_msg)
    elif bmi < 25:
        st.info(status_msg)
    else:
        st.warning(status_msg)

    st.caption("These are practical estimates. Adjust every 2 weeks based on progress.")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["🏋️ Workout", "🍽️ Food Plan", "🔥 Advice", "✅ Progress"])

    workout_data = build_workout(days, goal, experience)

    with tab1:
        st.markdown("### 🏋️ Weekly Workout Plan")
        st.caption("Each day is shown with sets and reps.")

        for day_title, exercises in workout_data:
            st.markdown(
                f"""
                <div class="panel">
                    <div class="big-number">{day_title}</div>
                    {"".join([f"• {ex}<br>" for ex in exercises])}
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        st.markdown("### 🍽️ Food Plan")

        left, right = st.columns(2)

        with left:
            st.markdown(
                f"""
                <div class="panel">
                <div class="big-number">Daily Targets</div>
                Calories: {int(calories)} kcal/day<br>
                Protein: {int(protein)} g/day<br>
                Water: {water} L/day
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            st.markdown(
                f"""
                <div class="panel">
                <div class="big-number">Meal Blueprint</div>
                {meal_plan(goal)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Extra Food Tips")
        st.write("- Eat 4–5 meals if trying to gain muscle")
        st.write("- Keep protein in every meal")
        st.write("- Sleep 7–8 hours")
        st.write("- Drink water through the day")

    with tab3:
        st.markdown("### 🔥 Smart Advice")

        a1, a2 = st.columns(2)

        with a1:
            st.markdown(
                f"""
                <div class="panel">
                <div class="big-number">Why this plan?</div>
                {advice_plan(goal, bmi)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with a2:
            st.markdown(
                """
                <div class="panel">
                <div class="big-number">Rules that work</div>
                - Add a little weight or reps over time<br>
                - Never skip sleep<br>
                - Track your body weight weekly<br>
                - Stay consistent for 90 days
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.success("Consistency = transformation 🚀")

    with tab4:
        st.markdown(f"### ✅ Daily Progress Tracker — Week {week_token}")
        st.caption("Tick the box when a day is finished. This gets saved for this profile name.")

        completed_days = []

        for idx, (day_title, _) in enumerate(workout_data, start=1):
            row1, row2 = st.columns([5, 1])

            with row1:
                st.markdown(f"**{day_title}**")
            with row2:
                checked = st.checkbox("Done", key=f"done_{profile_id}_w{week_token}_{idx}")

            if checked:
                completed_days.append(idx)

        profile["weeks"][str(week_token)] = {
            "completed_days": completed_days,
            "days": days,
            "goal": goal,
            "experience": experience,
        }
        save_store(store)

        st.progress(len(completed_days) / days)
        st.write(f"**{len(completed_days)}/{days} days completed**")

        if len(completed_days) == days:
            st.success("🔥 Week complete! Start a fresh week when you are ready.")

            def start_next_week():
                current_store = load_store()
                current_profile = current_store.setdefault(profile_id, {})
                current_profile.setdefault("weeks", {})
                current_profile.setdefault("weeks_completed", 0)
                current_profile["weeks"][str(week_token)] = {
                    "completed_days": completed_days,
                    "days": days,
                    "goal": goal,
                    "experience": experience,
                }
                current_profile["weeks_completed"] = int(current_profile.get("weeks_completed", 0)) + 1
                current_profile["current_week"] = week_token + 1
                save_store(current_store)
                st.session_state[week_token_key] = week_token + 1

            st.button("Start Next Week", key=f"next_week_btn_{profile_id}_{week_token}", on_click=start_next_week)

        weeks_done = store.get(profile_id, {}).get("weeks_completed", 0)
        st.caption(f"Weeks completed for this profile: {weeks_done}")

    st.divider()
    st.success(f"{profile_name}, your plan is ready and your progress is saved for this profile.")
else:
    st.info("Enter your details in the sidebar and press Generate / Update Plan.")