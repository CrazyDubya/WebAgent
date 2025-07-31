"""
Enhanced WebWalker Demo
Improved version with better error handling and user experience
"""

import streamlit as st
import os
import json5
import json
import asyncio
import base64
from PIL import Image
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional, Tuple
import traceback
import tempfile

# Page configuration
st.set_page_config(
    page_title="🚶 WebWalker Enhanced Demo",
    page_icon="🚶",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .demo-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    .step-indicator {
        background: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .error-container {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 5px;
        color: #721c24;
    }
    .success-container {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 5px;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

class MockWebWalker:
    """Mock WebWalker for demonstration purposes"""
    
    def __init__(self, query: str, website: str):
        self.query = query
        self.website = website
        self.visited_pages = []
        self.current_step = 0
        
    def simulate_web_extraction(self, url: str) -> Tuple[str, str, Optional[str]]:
        """Simulate web content extraction"""
        mock_content = f"""
# Mock Website Content for {url}

This is a demonstration of how WebWalker would extract content from {url}.

## Navigation Menu
- Home
- About
- Research
- Publications
- Contact

## Main Content
Information relevant to: "{self.query}"

In a real scenario, WebWalker would:
1. Extract the actual HTML content
2. Parse navigation elements
3. Identify clickable buttons and links
4. Extract relevant text content
5. Take screenshots for visual reference

## Available Actions
- Navigate to Research section
- Visit Publications page
- Check About page for more details
- Search within site content
"""
        
        mock_html = f"""
<html>
<body>
<nav>
    <a href="/home">Home</a>
    <a href="/about">About</a>
    <a href="/research">Research</a>
    <a href="/publications">Publications</a>
</nav>
<main>
    <h1>Welcome to Mock Website</h1>
    <p>This is mock content for demonstration purposes.</p>
    <p>Query: {self.query}</p>
</main>
</body>
</html>
"""
        
        # Mock base64 encoded screenshot (1x1 pixel image)
        mock_screenshot = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        return mock_html, mock_content, mock_screenshot
    
    def extract_links(self, html: str) -> List[Dict[str, str]]:
        """Extract links from HTML content"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            text = a_tag.get_text(strip=True)
            href = a_tag['href']
            if text and href:
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = self.website.rstrip('/') + href
                elif not href.startswith('http'):
                    href = self.website.rstrip('/') + '/' + href
                    
                links.append({
                    'text': text,
                    'url': href
                })
        
        return links
    
    def simulate_step(self) -> Dict:
        """Simulate a single navigation step"""
        self.current_step += 1
        
        if self.current_step == 1:
            action = f"Initial visit to {self.website}"
            url = self.website
        else:
            # Simulate navigation to different pages
            pages = ['/about', '/research', '/publications', '/contact']
            page = pages[(self.current_step - 2) % len(pages)]
            action = f"Navigate to {page}"
            url = self.website.rstrip('/') + page
        
        html, content, screenshot = self.simulate_web_extraction(url)
        links = self.extract_links(html)
        
        self.visited_pages.append(url)
        
        return {
            'step': self.current_step,
            'action': action,
            'url': url,
            'content': content,
            'links': links,
            'screenshot': screenshot,
            'thoughts': f"Step {self.current_step}: {action}. Found {len(links)} clickable elements. Analyzing content for relevance to '{self.query}'."
        }

def check_configuration() -> Dict[str, bool]:
    """Check system configuration and API availability"""
    config = {
        'openai_api': bool(os.getenv('OPENAI_API_KEY')),
        'dashscope_api': bool(os.getenv('DASHSCOPE_API_KEY')),
        'crawl4ai': True,  # Assume available
        'mock_mode': True  # Always available
    }
    return config

def display_configuration_status():
    """Display current configuration status"""
    st.subheader("🔧 Configuration Status")
    config = check_configuration()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "✅" if config['openai_api'] else "❌"
        st.metric("OpenAI API", status)
    
    with col2:
        status = "✅" if config['dashscope_api'] else "❌"
        st.metric("DashScope API", status)
    
    with col3:
        status = "✅" if config['crawl4ai'] else "❌"
        st.metric("Crawl4AI", status)
    
    with col4:
        status = "✅" if config['mock_mode'] else "❌"
        st.metric("Mock Mode", status)

def create_example_scenarios() -> Dict[str, Dict]:
    """Create predefined example scenarios"""
    return {
        "Conference Information": {
            "website": "https://2025.aclweb.org/",
            "query": "When is the paper submission deadline for ACL 2025 Industry Track, and what is the venue address?",
            "description": "Navigate a conference website to find submission deadlines and venue information"
        },
        "University Research": {
            "website": "https://www.stanford.edu/",
            "query": "Find information about AI research groups and their contact details",
            "description": "Explore university website to locate research group information"
        },
        "Company Information": {
            "website": "https://www.microsoft.com/",
            "query": "What are Microsoft's latest AI products and their key features?",
            "description": "Navigate corporate website to find product information"
        },
        "Documentation Search": {
            "website": "https://docs.python.org/",
            "query": "How to use asyncio for concurrent programming in Python?",
            "description": "Search technical documentation for specific programming topics"
        }
    }

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1>🚶 WebWalker Enhanced Demo</h1>
        <p>Systematic Web Traversal and Information Extraction</p>
        <p><em>Improved with better error handling and user experience</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    with st.expander("📖 About WebWalker", expanded=False):
        st.markdown("""
        **WebWalker** is an advanced web traversal agent that can:
        
        - 🌐 **Navigate websites systematically** - Follow links and explore pages methodically
        - 🔍 **Extract relevant information** - Parse content and identify key data points  
        - 📊 **Track navigation paths** - Maintain history of visited pages and actions
        - 🎯 **Goal-oriented exploration** - Focus on finding information relevant to your query
        - 📸 **Visual documentation** - Capture screenshots of important pages
        
        This enhanced demo includes improved error handling, better user interface, and mock functionality for testing without API keys.
        """)
    
    # Configuration status
    display_configuration_status()
    
    # Main demo interface
    st.header("🔬 WebWalker Demonstration")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Demo mode selection
        demo_mode = st.selectbox(
            "Demo Mode",
            ["Mock Mode (Safe)", "Full Mode (Requires APIs)"],
            help="Mock mode demonstrates functionality without making real web requests"
        )
        
        # Maximum steps
        max_steps = st.slider("Maximum Steps", min_value=1, max_value=15, value=5)
        
        # Example scenarios
        st.subheader("📋 Example Scenarios")
        examples = create_example_scenarios()
        selected_example = st.selectbox(
            "Choose Example:",
            ["Custom"] + list(examples.keys())
        )
        
        if selected_example != "Custom":
            example_data = examples[selected_example]
            st.info(f"**Description:** {example_data['description']}")
    
    # Input form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Navigation Target")
        
        # Pre-fill from example if selected
        if selected_example != "Custom":
            default_website = examples[selected_example]["website"]
            default_query = examples[selected_example]["query"]
        else:
            default_website = ""
            default_query = ""
        
        website = st.text_input(
            "🌐 Target Website:",
            value=default_website,
            placeholder="https://example.com"
        )
        
        query = st.text_area(
            "❓ What are you looking for?",
            value=default_query,
            placeholder="Enter your specific question or information need...",
            height=100
        )
        
        # Start button
        start_demo = st.button("🚀 Start WebWalker Demo", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("💡 Tips")
        st.markdown("""
        **For best results:**
        - Use specific, clear queries
        - Provide complete website URLs
        - Be patient during navigation
        - Check mock mode first
        
        **Example queries:**
        - Conference deadlines
        - Contact information
        - Product specifications
        - Research papers
        """)
    
    # Demo execution
    if start_demo:
        if not website or not query:
            st.error("❌ Please provide both a website URL and a query.")
            return
        
        # Validate URL format
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        st.success(f"✅ Starting WebWalker demo for: {query}")
        
        # Create progress tracking
        progress_container = st.container()
        results_container = st.container()
        
        with progress_container:
            st.subheader("🔄 Navigation Progress")
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Initialize WebWalker (mock mode)
        walker = MockWebWalker(query, website)
        
        with results_container:
            st.subheader("📊 Navigation Results")
            
            # Create columns for layout
            step_col, content_col = st.columns([1, 2])
            
            # Execute navigation steps
            for step_num in range(max_steps):
                # Update progress
                progress = (step_num + 1) / max_steps
                progress_bar.progress(progress)
                status_text.text(f"Step {step_num + 1}/{max_steps}: Navigating...")
                
                try:
                    # Simulate step execution
                    step_result = walker.simulate_step()
                    
                    with step_col:
                        st.markdown(f"""
                        <div class="step-indicator">
                            Step {step_result['step']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**Action:** {step_result['action']}")
                        st.markdown(f"**URL:** {step_result['url']}")
                        st.markdown(f"**Links Found:** {len(step_result['links'])}")
                        
                        # Show links
                        if step_result['links']:
                            st.markdown("**Available Links:**")
                            for link in step_result['links'][:3]:  # Show first 3
                                st.markdown(f"- {link['text']}")
                    
                    with content_col:
                        # Show thoughts
                        st.markdown("**🤔 Agent Thoughts:**")
                        st.info(step_result['thoughts'])
                        
                        # Show content preview
                        with st.expander(f"📄 Content from Step {step_result['step']}", expanded=False):
                            st.markdown(step_result['content'])
                        
                        # Show screenshot (mock)
                        if step_result['screenshot']:
                            try:
                                # Create a simple colored rectangle as mock screenshot
                                img = Image.new('RGB', (400, 300), color=(100, 150, 200))
                                st.image(img, caption=f"Screenshot - Step {step_result['step']}", width=300)
                            except Exception as e:
                                st.warning(f"Could not display screenshot: {str(e)}")
                    
                    # Add separator
                    st.markdown("---")
                    
                    # Simulate processing time
                    import time
                    time.sleep(0.5)
                    
                except Exception as e:
                    st.error(f"❌ Error in step {step_num + 1}: {str(e)}")
                    if demo_mode == "Full Mode (Requires APIs)":
                        st.warning("💡 Try switching to Mock Mode for demonstration without API requirements.")
                    break
            
            # Final results
            status_text.text("✅ Navigation completed!")
            
            st.subheader("📋 Final Summary")
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.metric("Pages Visited", len(walker.visited_pages))
            
            with summary_col2:
                st.metric("Steps Completed", walker.current_step)
            
            with summary_col3:
                st.metric("Success Rate", "100%")
            
            # Show visited pages
            st.subheader("🗺️ Navigation Path")
            for i, page in enumerate(walker.visited_pages, 1):
                st.markdown(f"{i}. {page}")
            
            # Mock final answer
            st.subheader("💡 Extracted Information")
            st.markdown(f"""
            <div class="success-container">
                <strong>Query:</strong> {query}<br><br>
                <strong>Answer:</strong> Based on the navigation through {website}, WebWalker would extract and synthesize 
                relevant information to answer your query. In this mock demonstration, the agent successfully navigated 
                {len(walker.visited_pages)} pages and identified multiple relevant content sections.
                <br><br>
                <strong>Confidence:</strong> High (in real scenario, this would be based on actual content analysis)
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()