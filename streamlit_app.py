import streamlit as st
import sys
import os
from io import StringIO
import contextlib
import threading
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from hw import EnhancedForebetAnalyzer
except ImportError:
    st.error("⚠️ Football analyzer module not found. Please ensure hw.py is in the same directory.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Football Match Analyzer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    .league-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .league-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 Enhanced Football Match Analyzer</h1>', unsafe_allow_html=True)

# League Statistics
st.markdown("### 📊 League Performance Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Premier League", "50%", "Accuracy")
    st.caption("Draw Rate: 33% | Goals: 2.8")

with col2:
    st.metric("Champions League", "40%", "Accuracy") 
    st.caption("Draw Rate: 30% | Goals: 2.6")

with col3:
    st.metric("Europa League", "0%", "Draw Epidemic")
    st.caption("Draw Rate: 89% | Goals: 2.2")

with col4:
    st.metric("Conference League", "20%", "Accuracy")
    st.caption("Draw Rate: 60% | Goals: 1.0")

st.divider()

# Sidebar
with st.sidebar:
    st.header("🎯 Quick Guide")
    st.markdown("""
    **Analysis Mode:**
    - Paste Forebet URL
    - Get instant predictions
    
    **Learning Mode:**
    - Add actual result
    - Format: H 2-1, A 0-3, D 1-1
    
    **Supported Leagues:**
    - Premier League ⭐
    - Champions League 🏆
    - Europa League 🥈
    - Conference League 🥉
    - La Liga, Bundesliga, Serie A, Ligue 1
    """)
    
    st.header("🔥 Key Features")
    st.markdown("""
    - Emergency draw detection
    - League-specific learning
    - Goal market predictions
    - Real-time model updates
    """)

# Main interface
st.header("⚽ Match Analysis")

# Input form
with st.form("analyze_form"):
    url = st.text_input(
        "🔗 Forebet Match URL:",
        placeholder="https://www.forebet.com/en/football/matches/...",
        help="Paste the full Forebet match URL here"
    )
    
    actual_result = st.text_input(
        "📊 Actual Result (Optional - for learning):",
        placeholder="H 2-1, A 0-3, D 1-1, etc.",
        help="Add actual match result to improve the model"
    )
    
    submitted = st.form_submit_button("🚀 Analyze Match", use_container_width=True)

# Analysis execution
if submitted and url:
    if not url.startswith("https://www.forebet.com"):
        st.error("❌ Please enter a valid Forebet URL")
    else:
        with st.spinner("🔄 Analyzing match... This may take 30-60 seconds"):
            try:
                # Initialize analyzer
                analyzer = EnhancedForebetAnalyzer()
                
                # Capture output
                output = StringIO()
                result = {'output': '', 'error': None}
                
                def run_analysis():
                    try:
                        with contextlib.redirect_stdout(output):
                            analyzer.main(url, actual_result if actual_result else None)
                        result['output'] = output.getvalue()
                    except Exception as e:
                        result['error'] = str(e)
                
                # Run with timeout
                thread = threading.Thread(target=run_analysis)
                thread.start()
                thread.join(timeout=90)  # 90 second timeout for Streamlit
                
                if thread.is_alive():
                    st.error("⏰ Analysis timed out. Please try again.")
                elif result['error']:
                    st.error(f"❌ Error: {result['error']}")
                else:
                    st.success("✅ Analysis Complete!")
                    
                    # Display results
                    st.header("📋 Analysis Results")
                    st.text_area(
                        "Output:",
                        value=result['output'],
                        height=400,
                        help="Complete match analysis with predictions and learning insights"
                    )
                    
                    # Extract key info for display
                    output_lines = result['output'].split('\n')
                    
                    # Look for recommendation
                    for line in output_lines:
                        if "BET:" in line and ("WIN" in line or "DRAW" in line):
                            st.info(f"🎯 **Recommendation:** {line.strip()}")
                            break
                    
                    # Look for learning info
                    for line in output_lines:
                        if "Goal learning:" in line:
                            st.info(f"📚 **Learning:** {line.strip()}")
                            break
                            
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

elif submitted:
    st.warning("⚠️ Please enter a Forebet URL")

# Examples section
st.divider()
st.header("📝 Usage Examples")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Analysis Only")
    st.code("""
URL: https://www.forebet.com/en/football/matches/arsenal-chelsea-123456
Result: (leave empty)
    """)
    st.caption("Get predictions and analysis without learning")

with col2:
    st.subheader("📚 Learning Mode")
    st.code("""
URL: https://www.forebet.com/en/football/matches/arsenal-chelsea-123456
Result: H 2-1
    """)
    st.caption("Analyze + improve model with actual result")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #7f8c8d; margin-top: 2rem;'>
    <p>🔬 <strong>Enhanced Football Analyzer</strong> | League-Specific Learning | Emergency Draw Detection</p>
    <p>📊 Trained on 50+ matches across Premier League, Champions League, Europa League & Conference League</p>
</div>
""", unsafe_allow_html=True)
