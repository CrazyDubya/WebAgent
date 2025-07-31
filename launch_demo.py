#!/usr/bin/env python3
"""
WebAgent Demo Launcher
A simple script to launch different WebAgent demos and tools
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class WebAgentLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.demos = {
            "playground": {
                "name": "🎮 Interactive Playground",
                "description": "Comprehensive demo showcasing all WebAgent components",
                "script": "interactive_playground.py",
                "requirements": ["streamlit", "plotly", "pandas"]
            },
            "unified": {
                "name": "🤖 Unified Demo", 
                "description": "Single interface for all WebAgent components",
                "script": "unified_demo.py",
                "requirements": ["streamlit"]
            },
            "webwalker": {
                "name": "🚶 Enhanced WebWalker",
                "description": "Improved WebWalker with better error handling",
                "script": "enhanced_webwalker_demo.py", 
                "requirements": ["streamlit", "beautifulsoup4", "pillow"]
            },
            "webwalker_original": {
                "name": "🚶 Original WebWalker",
                "description": "Original WebWalker demo (fixed bugs)",
                "script": "WebWalker/src/app.py",
                "requirements": ["streamlit", "crawl4ai", "qwen-agent"]
            },
            "webdancer": {
                "name": "🕺 WebDancer GUI",
                "description": "WebDancer with Gradio interface",
                "script": "WebDancer/demos/assistant_qwq_chat.py",
                "requirements": ["qwen-agent", "gradio"]
            }
        }
    
    def check_dependencies(self, demo_key: str) -> bool:
        """Check if required dependencies are installed"""
        demo = self.demos[demo_key]
        missing_deps = []
        
        for requirement in demo["requirements"]:
            import_name = self.import_name_mapping.get(requirement, requirement.replace("-", "_"))
            try:
                __import__(import_name)
            except ImportError:
                missing_deps.append(requirement)
        
        if missing_deps:
            print(f"❌ Missing dependencies for {demo['name']}: {', '.join(missing_deps)}")
            print(f"Install with: pip install {' '.join(missing_deps)}")
            return False
        
        return True
    
    def list_demos(self):
        """List all available demos"""
        print("\n🚀 Available WebAgent Demos:")
        print("=" * 50)
        
        for key, demo in self.demos.items():
            print(f"\n{demo['name']}")
            print(f"Key: {key}")
            print(f"Description: {demo['description']}")
            print(f"Requirements: {', '.join(demo['requirements'])}")
    
    def launch_demo(self, demo_key: str, port: int = None):
        """Launch a specific demo"""
        if demo_key not in self.demos:
            print(f"❌ Demo '{demo_key}' not found. Use --list to see available demos.")
            return False
        
        demo = self.demos[demo_key]
        print(f"\n🚀 Launching {demo['name']}...")
        
        # Check dependencies
        if not self.check_dependencies(demo_key):
            return False
        
        # Prepare script path
        script_path = self.root_dir / demo["script"]
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        # Launch command
        cmd = ["streamlit", "run", str(script_path)]
        
        if port:
            cmd.extend(["--server.port", str(port)])
        
        # Add default settings for better UX
        cmd.extend([
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ])
        
        print(f"Running: {' '.join(cmd)}")
        print(f"📱 Demo will be available at: http://localhost:{port or 8501}")
        
        try:
            subprocess.run(cmd, cwd=self.root_dir)
        except KeyboardInterrupt:
            print("\n👋 Demo stopped by user")
        except Exception as e:
            print(f"❌ Error launching demo: {e}")
            return False
        
        return True
    
    def check_environment(self):
        """Check overall environment setup"""
        print("\n🔍 Environment Check:")
        print("=" * 30)
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (3.8+ required)")
        
        # Check key packages
        key_packages = ["streamlit", "openai", "requests"]
        for package in key_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} (not installed)")
        
        # Check API keys
        print("\n🔑 API Keys:")
        api_keys = {
            "OPENAI_API_KEY": "OpenAI GPT models",
            "DASHSCOPE_API_KEY": "Qwen models", 
            "GOOGLE_SEARCH_KEY": "Web search",
            "JINA_API_KEY": "Content extraction"
        }
        
        for key, description in api_keys.items():
            if os.getenv(key):
                print(f"✅ {key} ({description})")
            else:
                print(f"❌ {key} ({description}) - Optional")
        
        print("\n💡 Tip: Demos work in mock mode without API keys!")
    
    def install_requirements(self):
        """Install all requirements for demos"""
        print("\n📦 Installing WebAgent demo requirements...")
        
        all_requirements = set()
        for demo in self.demos.values():
            all_requirements.update(demo["requirements"])
        
        requirements_list = list(all_requirements)
        
        print(f"Installing: {', '.join(requirements_list)}")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + requirements_list, check=True)
            print("✅ All requirements installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing requirements: {e}")
            return False
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="WebAgent Demo Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    # List all available demos
  %(prog)s playground               # Launch interactive playground
  %(prog)s webwalker --port 8502    # Launch WebWalker on port 8502
  %(prog)s --check                  # Check environment setup
  %(prog)s --install                # Install all requirements
        """
    )
    
    parser.add_argument(
        "demo",
        nargs="?",
        help="Demo to launch (use --list to see options)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available demos"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port to run the demo on (default: 8501)"
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check environment setup"
    )
    
    parser.add_argument(
        "--install",
        action="store_true", 
        help="Install all demo requirements"
    )
    
    args = parser.parse_args()
    launcher = WebAgentLauncher()
    
    # Handle different actions
    if args.list:
        launcher.list_demos()
    elif args.check:
        launcher.check_environment()
    elif args.install:
        launcher.install_requirements()
    elif args.demo:
        launcher.launch_demo(args.demo, args.port)
    else:
        # No arguments - show help and list demos
        parser.print_help()
        launcher.list_demos()

if __name__ == "__main__":
    main()