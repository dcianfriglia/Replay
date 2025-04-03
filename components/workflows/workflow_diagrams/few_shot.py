import streamlit as st


def render_few_shot_diagram():
    """Render Few-Shot Learning workflow diagram"""

    html = """
    <div class="workflow-diagram">
        <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
            <!-- Input Node -->
            <circle cx="100" cy="150" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="100" y="155" text-anchor="middle" font-family="sans-serif">In</text>

            <!-- Example Inputs -->
            <rect x="230" y="20" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="300" y="45" text-anchor="middle" font-family="sans-serif" font-size="14">Example 1 Input</text>

            <rect x="230" y="70" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="300" y="95" text-anchor="middle" font-family="sans-serif" font-size="14">Example 2 Input</text>

            <rect x="230" y="120" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="300" y="145" text-anchor="middle" font-family="sans-serif" font-size="14">Example 3 Input</text>

            <!-- Example Outputs -->
            <rect x="430" y="20" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="500" y="45" text-anchor="middle" font-family="sans-serif" font-size="14">Example 1 Output</text>

            <rect x="430" y="70" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="500" y="95" text-anchor="middle" font-family="sans-serif" font-size="14">Example 2 Output</text>

            <rect x="430" y="120" width="140" height="40" rx="5" ry="5" fill="#f0f9ff" stroke="#0c63e4" stroke-width="2"/>
            <text x="500" y="145" text-anchor="middle" font-family="sans-serif" font-size="14">Example 3 Output</text>

            <!-- Example Arrows -->
            <line x1="370" y1="40" x2="430" y2="40" stroke="#6c757d" stroke-width="2"/>
            <polygon points="430,40 420,35 420,45" fill="#6c757d"/>

            <line x1="370" y1="90" x2="430" y2="90" stroke="#6c757d" stroke-width="2"/>
            <polygon points="430,90 420,85 420,95" fill="#6c757d"/>

            <line x1="370" y1="140" x2="430" y2="140" stroke="#6c757d" stroke-width="2"/>
            <polygon points="430,140 420,135 420,145" fill="#6c757d"/>

            <!-- User Input -->
            <rect x="230" y="210" width="140" height="40" rx="5" ry="5" fill="#d1e7dd" stroke="#0f5132" stroke-width="2"/>
            <text x="300" y="235" text-anchor="middle" font-family="sans-serif" font-size="14">User Input</text>

            <!-- Input arrow -->
            <line x1="130" y1="150" x2="180" y2="150" stroke="#6c757d" stroke-width="2"/>
            <polygon points="180,150 170,145 170,155" fill="#6c757d"/>

            <!-- Few-shot LLM -->
            <rect x="180" y="120" width="140" height="60" rx="5" ry="5" fill="#d4edda" stroke="#155724" stroke-width="2"/>
            <text x="250" y="145" text-anchor="middle" font-family="sans-serif">Few-Shot</text>
            <text x="250" y="165" text-anchor="middle" font-family="sans-serif">LLM</text>

            <!-- LLM to User Input arrow -->
            <line x1="250" y1="180" x2="250" y2="210" stroke="#6c757d" stroke-width="2"/>
            <polygon points="250,210 245,200 255,200" fill="#6c757d"/>

            <!-- Generated Output -->
            <rect x="430" y="210" width="140" height="40" rx="5" ry="5" fill="#d1e7dd" stroke="#0f5132" stroke-width="2"/>
            <text x="500" y="235" text-anchor="middle" font-family="sans-serif" font-size="14">Generated Output</text>

            <!-- User Input to Output arrow -->
            <line x1="370" y1="230" x2="430" y2="230" stroke="#6c757d" stroke-width="2"/>
            <polygon points="430,230 420,225 420,235" fill="#6c757d"/>

            <!-- Output Node -->
            <circle cx="650" cy="230" r="30" fill="#f8d7da" stroke="#721c24" stroke-width="2"/>
            <text x="650" y="235" text-anchor="middle" font-family="sans-serif">Out</text>

            <!-- Generated Output to Final Output arrow -->
            <line x1="570" y1="230" x2="620" y2="230" stroke="#6c757d" stroke-width="2"/>
            <polygon points="620,230 610,225 610,235" fill="#6c757d"/>
        </svg>
        <p class="diagram-caption">The Few-Shot Learning workflow showing example-guided generation</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)