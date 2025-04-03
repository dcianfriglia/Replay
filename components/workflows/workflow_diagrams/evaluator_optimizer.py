import streamlit as st


def render_evaluator_optimizer_diagram():
    """Render Evaluator-Optimizer workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="100" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="105" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- Generator LLM -->
            <rect x="200" y="70" width="120" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="260" y="95" text-anchor="middle" font-family="sans-serif">LLM Call</text>
            <text x="260" y="115" text-anchor="middle" font-family="sans-serif">Generator</text>

            <!-- Solution arrow -->
            <path d="M 320 90 C 370 90, 370 60, 420 60" stroke="#6c757d" stroke-width="2" fill="transparent"/>
            <polygon points="420,60 410,55 410,65" fill="#6c757d"/>
            <text x="360" y="50" text-anchor="middle" font-family="sans-serif" font-size="12">Solution</text>

            <!-- Evaluator LLM -->
            <rect x="420" y="30" width="120" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="480" y="55" text-anchor="middle" font-family="sans-serif">LLM Call</text>
            <text x="480" y="75" text-anchor="middle" font-family="sans-serif">Evaluator</text>

            <!-- Accepted arrow -->
            <line x1="540" y1="60" x2="600" y2="60" stroke="#6c757d" stroke-width="2"/>
            <polygon points="600,60 590,55 590,65" fill="#6c757d"/>
            <text x="570" y="50" text-anchor="middle" font-family="sans-serif" font-size="12">Accepted</text>

            <!-- Output Node -->
            <circle cx="630" cy="60" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="630" y="65" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Rejected + Feedback arrow -->
            <path d="M 480 90 C 480 130, 300 130, 260 130" stroke="#6c757d" stroke-width="2" fill="transparent" stroke-dasharray="5,5"/>
            <polygon points="260,130 270,125 270,135" fill="#6c757d"/>
            <text x="370" y="150" text-anchor="middle" font-family="sans-serif" font-size="12">Rejected + Feedback</text>

            <!-- Input to Generator arrow -->
            <line x1="130" y1="100" x2="200" y2="100" stroke="#6c757d" stroke-width="2"/>
            <polygon points="200,100 190,95 190,105" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Evaluator-Optimizer workflow with feedback loop</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)