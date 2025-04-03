import streamlit as st


def render_routing_diagram():
    """Render Routing workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="105" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- Router LLM -->
            <rect x="180" y="70" width="120" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="240" y="105" text-anchor="middle" font-family="sans-serif">LLM Call Router</text>

            <!-- Router arrows -->
            <line x1="300" y1="85" x2="380" y2="50" stroke="#6c757d" stroke-width="2"/>
            <polygon points="380,50 370,48 372,58" fill="#6c757d"/>

            <line x1="300" y1="100" x2="380" y2="100" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="380,100 370,95 370,105" fill="#6c757d"/>

            <line x1="300" y1="115" x2="380" y2="150" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="380,150 370,145 374,155" fill="#6c757d"/>

            <!-- LLM Calls -->
            <rect x="380" y="20" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="55" text-anchor="middle" font-family="sans-serif">LLM Call 1</text>

            <rect x="380" y="70" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="105" text-anchor="middle" font-family="sans-serif">LLM Call 2</text>

            <rect x="380" y="120" width="100" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="430" y="155" text-anchor="middle" font-family="sans-serif">LLM Call 3</text>

            <!-- Output arrows -->
            <line x1="480" y1="50" x2="550" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="550,100 540,94 538,104" fill="#6c757d"/>

            <line x1="480" y1="100" x2="550" y2="100" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="550,100 540,95 540,105" fill="#6c757d"/>

            <line x1="480" y1="150" x2="550" y2="100" stroke="#6c757d" stroke-width="2" stroke-dasharray="5,5"/>
            <polygon points="550,100 542,108 538,98" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="600" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="600" y="105" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Input to Router arrow -->
            <line x1="130" y1="100" x2="180" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,100 170,95 170,105" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Routing workflow showing specialized handlers</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)