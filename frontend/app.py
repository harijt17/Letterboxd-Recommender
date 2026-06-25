import requests
import streamlit as st


API_URL = (
    "https://letterboxd-recommender-y38p.onrender.com/api"
)

st.set_page_config(
    page_title="Letterboxd Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title(
    "🎬 Letterboxd Recommender"
)

st.write(
    "Upload your Letterboxd export and get personalized movie recommendations."
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

# --------------------------------------------------
# STEP 1: Upload ZIP
# --------------------------------------------------

st.header("Step 1: Upload Export")

uploaded_file = st.file_uploader(
    "Letterboxd Export ZIP",
    type=["zip"]
)

if uploaded_file:

    if st.button(
        "Process Export"
    ):

        with st.spinner(
            "Processing export..."
        ):

            files = {

                "file":
                (
                    uploaded_file.name,
                    uploaded_file,
                    "application/zip"
                )
            }

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                data = response.json()

                st.session_state.session_id = (
                    data["session_id"]
                )

                st.success(
                    "Export processed successfully!"
                )

                watched_response = requests.get(
                    f"{API_URL}/watched/"
                    f"{st.session_state.session_id}"
                )

                if watched_response.status_code == 200:

                    st.session_state.watched_movies = (
                        watched_response
                        .json()["movies"]
                    )

            else:

                st.error(
                    response.text
                )

# --------------------------------------------------
# STEP 2: Favorites
# --------------------------------------------------

if st.session_state.session_id:

    st.header(
        "Step 2: Select 4 Favorites"
    )

    favorites = st.multiselect(
        "Choose 4 favorite movies",
        st.session_state.watched_movies,
        max_selections=4
    )

    if st.button(
        "Save Favorites"
    ):

        if len(favorites) != 4:

            st.warning(
                "Please select exactly 4 movies."
            )

        else:

            response = requests.post(
                f"{API_URL}/favorites/"
                f"{st.session_state.session_id}",
                json=favorites
            )

            if response.status_code == 200:

                st.success(
                    "Favorites saved!"
                )

            else:

                st.error(
                    response.text
                )

# --------------------------------------------------
# STEP 3: Recommendations
# --------------------------------------------------

if st.session_state.session_id:

    st.header(
        "Step 3: Generate Recommendations"
    )

    if st.button(
        "Get Recommendations"
    ):

        with st.spinner(
            "Generating recommendations..."
        ):

            response = requests.get(
                f"{API_URL}/recommend/"
                f"{st.session_state.session_id}"
            )

            if response.status_code == 200:

                st.session_state.recommendations = (
                    response.json()
                )

            else:

                st.error(
                    response.text
                )

# --------------------------------------------------
# STEP 4: Display Recommendations
# --------------------------------------------------

if st.session_state.recommendations:

    result = (
        st.session_state
        .recommendations
    )

    st.header(
        "Recommended Movies"
    )

    st.write(
        f"Candidates searched: "
        f"{result['candidate_count']}"
    )

    for movie in result[
        "recommendations"
    ]:

        with st.container():

            st.subheader(
                movie.get(
                    "display_title",
                    movie["title"]
                )
            )

            st.write(
                f"⭐ Score: "
                f"{movie['score']}"
            )

            st.write(
                movie["reason"]
            )

            st.write(
                f"Genres: "
                f"{movie.get('genres', '')}"
            )

            st.divider()