"""
Marimo Magic Command for Jupyter Notebooks
==========================================

A custom IPython magic command to run marimo servers embedded in Jupyter notebooks,
similar to %tensorboard. Perfect for Google Colab integration.

Usage:
    %load_ext marimo_magic
    %marimo experiments/canine_ft.py
    %marimo experiments/canine_ft.py --port 8080 --height 800
"""

import os
import sys
import time
import subprocess
import threading
from IPython.core.magic import Magics, line_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import HTML, display
from IPython import get_ipython
import requests
import socket
from contextlib import closing
import signal
from typing import Optional, Dict, Any


@magics_class
class MarimoMagics(Magics):
    """Custom IPython magics for marimo integration"""

    def __init__(self, shell):
        super().__init__(shell)
        self.processes: Dict[int, subprocess.Popen] = {}
        self.used_ports: set = set()
        self.temp_notebooks: Dict[int, str] = {}  # Track temp notebooks by port

    def __del__(self):
        """Clean up any running processes when the magic is destroyed."""
        import os  # Add missing import

        for port, process in self.processes.items():
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass

            # Clean up temp notebook if exists
            if port in self.temp_notebooks:
                try:
                    os.unlink(self.temp_notebooks[port])
                except Exception:
                    pass

    def _find_free_port(self, start_port: int = 2718) -> int:
        """Find a free port starting from the given port."""
        for port in range(start_port, start_port + 100):
            if port not in self.used_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.bind(("127.0.0.1", port))
                        self.used_ports.add(port)
                        return port
                except OSError:
                    continue
        raise RuntimeError("No free ports available")

    def _is_colab(self) -> bool:
        """Check if running in Google Colab."""
        try:
            import google.colab

            return True
        except ImportError:
            return False

    def _get_colab_proxy_url(self, port: int) -> str:
        """Get the Colab proxy URL for the given port."""
        try:
            # First, try the modern approach using google.colab.output
            from google.colab.output import eval_js

            # This JavaScript call returns the proper proxy URL that bypasses restrictions
            proxy_url = eval_js(f"google.colab.kernel.proxyPort({port})")
            if proxy_url:
                return proxy_url

        except Exception as e:
            print(f"⚠️ Colab eval_js method failed: {e}")

        try:
            # Fallback: Try the alternative format
            from google.colab import output
            import google.colab

            # Get the colab proxy URL in the expected format
            proxy_url = f"https://{port}-dot-colab.googleusercontent.com/"
            return proxy_url

        except Exception as e:
            print(f"⚠️ Colab proxy fallback failed: {e}")

        # Final fallback for testing
        return f"http://localhost:{port}"

    def _wait_for_server(
        self, port: int, timeout: int = 30, debug: bool = False
    ) -> bool:
        """Wait for the marimo server to start."""
        if debug:
            print(f"⏳ Waiting for marimo server on port {port}...")

        start_time = time.time()
        dependency_warning_shown = False

        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex(("127.0.0.1", port))
                    if result == 0:
                        if debug:
                            print(f"✅ Server is responding on port {port}")
                        return True
            except Exception as e:
                if debug:
                    print(f"Connection attempt failed: {e}")

            # Show dependency installation warning after 10 seconds
            if not dependency_warning_shown and time.time() - start_time > 10:
                if debug:
                    print("📦 Server taking longer than expected...")
                    print("    This may be due to inline dependency installation")
                    print("    Heavy packages like torch can take several minutes")
                dependency_warning_shown = True

            time.sleep(0.5)

        if debug:
            print(f"❌ Server failed to start on port {port} within {timeout} seconds")
        return False

    def _test_connection(self, port: int) -> None:
        """Test connection to the marimo server with detailed diagnostics."""
        print(f"🔍 Testing connection to marimo server on port {port}...")

        # Test 1: Check if port is open
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                result = sock.connect_ex(("127.0.0.1", port))
                if result == 0:
                    print(f"✅ Port {port} is open and accepting connections")
                else:
                    print(
                        f"❌ Port {port} is not accepting connections (error code: {result})"
                    )
                    return
        except Exception as e:
            print(f"❌ Socket connection failed: {e}")

        # Test 2: Try HTTP request
        try:
            import urllib.request

            url = f"http://127.0.0.1:{port}/"
            print(f"🌐 Testing HTTP request to {url}")

            with urllib.request.urlopen(url, timeout=5) as response:
                content = response.read().decode("utf-8")[:200]
                print(
                    f"✅ HTTP request successful, content preview: {content[:100]}..."
                )
        except Exception as e:
            print(f"❌ HTTP request failed: {e}")

        # Test 3: Show process status
        if port in self.processes:
            process = self.processes[port]
            if process.poll() is None:
                print(f"✅ Marimo process is running (PID: {process.pid})")
            else:
                print(
                    f"❌ Marimo process has terminated with return code: {process.returncode}"
                )
        else:
            print(f"❌ No process record found for port {port}")

    def _display_for_colab(
        self, port: int, height: int, width: str, debug: bool, edit_mode: bool = False
    ) -> None:
        """Display marimo in Google Colab using the proxy system."""
        proxy_url = self._get_colab_proxy_url(port)

        if debug:
            print(f"🔗 Colab proxy URL: {proxy_url}")

        mode_text = "📝 EDIT MODE" if edit_mode else "▶️ RUN MODE"
        mode_description = (
            "You can modify and edit the notebook"
            if edit_mode
            else "Interactive read-only mode"
        )

        # Build mode-specific tips
        if edit_mode:
            mode_tips = """
                    <li>🖊️ Edit mode: You can modify cells and add new ones</li>
                    <li>💾 Your changes are automatically saved</li>
                    <li>🔄 Use Ctrl+S to manually save or Ctrl+R to restart kernel</li>"""
        else:
            mode_tips = """
                    <li>▶️ Run mode: You can interact with widgets and run cells</li>
                    <li>📊 Perfect for demos and interactive presentations</li>
                    <li>🔍 Use this mode to explore results without editing code</li>"""

        # Create enhanced display for Colab with both iframe and link fallback
        html_content = f"""
        <div style="border: 2px solid #4285f4; border-radius: 8px; padding: 20px; margin: 10px 0; background: #f8f9fa;">
            <h3 style="color: #1a73e8; margin-top: 0;">🎯 Marimo Notebook Ready! <span style="font-size: 14px; background: #e8f5e8; color: #137333; padding: 4px 8px; border-radius: 4px;">{mode_text}</span></h3>
            <p style="font-size: 14px; color: #666; margin: 5px 0;">{mode_description}</p>
            
            <!-- Try iframe first -->
            <div id="marimo-iframe-container">
                <iframe 
                    id="marimo-iframe"
                    src="{proxy_url}" 
                    width="{width}" 
                    height="{height}px"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox allow-downloads"
                    style="border-radius: 4px; display: block;">
                </iframe>
            </div>
            
            <!-- Fallback link (always visible) -->
            <div style="margin-top: 15px; text-align: center;">
                <p style="font-size: 16px; margin: 10px 0;">
                    <strong>📱 If the notebook doesn't load above, click here:</strong>
                </p>
                <p style="margin: 15px 0;">
                    <a href="{proxy_url}" target="_blank" style="
                        display: inline-block;
                        background: #1a73e8;
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 16px;
                    ">🚀 Open Marimo Notebook</a>
                </p>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #e8f5e8; border-radius: 4px;">
                <p style="margin: 0; color: #137333;"><strong>✨ Pro Tips:</strong></p>
                <ul style="margin: 10px 0; color: #137333;">
                    <li>The notebook should load in the iframe above</li>
                    <li>If it doesn't load, try the "Open Marimo Notebook" button</li>{mode_tips}
                </ul>
            </div>
            
            <details style="margin-top: 15px;">
                <summary style="cursor: pointer; color: #1a73e8; font-weight: bold;">🔧 Advanced Options</summary>
                <div style="margin-top: 10px; font-family: monospace; background: #f1f3f4; padding: 10px; border-radius: 4px;">
                    <p><strong>Proxy URL:</strong> <code>{proxy_url}</code></p>
                    <p><strong>Local Port:</strong> <code>{port}</code></p>
                    <button onclick="document.getElementById('marimo-iframe').src = document.getElementById('marimo-iframe').src" style="
                        background: #34a853;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-right: 10px;
                    ">🔄 Reload iframe</button>
                    <button onclick="navigator.clipboard.writeText('{proxy_url}')" style="
                        background: #34a853;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                    ">📋 Copy URL</button>
                </div>
            </details>
        </div>
        
        <script>
        // Enhanced iframe handling for Colab
        (function() {{
            const iframe = document.getElementById('marimo-iframe');
            const container = document.getElementById('marimo-iframe-container');
            let loadTimeout;
            
            // Set a timeout to detect if iframe fails to load
            loadTimeout = setTimeout(() => {{
                console.log('⚠️ Iframe loading timeout - this is normal in some Colab configurations');
                // Don't hide the iframe, just add a note
                if (container) {{
                    const note = document.createElement('div');
                    note.style.cssText = 'color: #856404; background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 4px; font-size: 14px;';
                    note.innerHTML = '⚠️ <strong>Note:</strong> If the iframe appears empty, please use the "Open Marimo Notebook" button below for direct access.';
                    container.appendChild(note);
                }}
            }}, 8000);
            
            // Clear timeout if iframe loads successfully
            iframe.onload = function() {{
                clearTimeout(loadTimeout);
                console.log('✅ Marimo iframe loaded successfully');
            }};
            
            // Handle iframe errors
            iframe.onerror = function() {{
                clearTimeout(loadTimeout);
                console.log('❌ Iframe failed to load - using fallback');
                if (container) {{
                    const error = document.createElement('div');
                    error.style.cssText = 'color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; margin: 10px 0; border-radius: 4px; font-size: 14px;';
                    error.innerHTML = '⚠️ <strong>Iframe embedding restricted.</strong> Please use the "Open Marimo Notebook" button below.';
                    container.appendChild(error);
                }}
            }};
            
            // Auto-open in new tab for Colab environment (optional)
            if (typeof google !== 'undefined' && google.colab && window.location.hostname.includes('colab')) {{
                // Delay the auto-open to let user see the interface first
                setTimeout(() => {{
                    // Only auto-open if iframe hasn't loaded
                    if (!iframe.contentDocument && !iframe.contentWindow) {{
                        console.log('🚀 Auto-opening marimo in new tab');
                        window.open('{proxy_url}', '_blank');
                    }}
                }}, 3000);
            }}
        }})();
        </script>
        """

        display(HTML(html_content))

    def _display_for_regular_jupyter(
        self, port: int, height: int, width: str, debug: bool, edit_mode: bool = False
    ) -> None:
        """Display marimo in regular Jupyter using iframe."""
        mode_text = "📝 EDIT MODE" if edit_mode else "▶️ RUN MODE"
        mode_description = (
            "You can modify and edit the notebook"
            if edit_mode
            else "Interactive read-only mode"
        )

        iframe_html = f"""
        <div style="border: 2px solid #4285f4; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h3 style="color: #1a73e8; margin-top: 0;">🎯 Marimo Notebook <span style="font-size: 14px; background: #e8f5e8; color: #137333; padding: 4px 8px; border-radius: 4px;">{mode_text}</span></h3>
            <p style="font-size: 14px; color: #666; margin: 5px 0 15px 0;">{mode_description}</p>
            <iframe 
                src="http://127.0.0.1:{port}" 
                width="{width}" 
                height="{height}px"
                frameborder="0"
                style="border-radius: 4px;">
            </iframe>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                <strong>Direct URL:</strong> <a href="http://127.0.0.1:{port}" target="_blank">http://127.0.0.1:{port}</a>
            </div>
        </div>
        """
        display(HTML(iframe_html))

    def _test_marimo_url(
        self, port: int, is_edit_mode: bool = False, debug: bool = False
    ) -> bool:
        """Test if the marimo server is responding correctly on the given port."""
        try:
            import urllib.request
            import urllib.error

            url = f"http://127.0.0.1:{port}/"
            if debug:
                print(f"🌐 Testing marimo URL: {url}")

            # Test basic HTTP connection
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    content = response.read().decode("utf-8")
                    status_code = response.getcode()

                    if debug:
                        print(f"✅ HTTP {status_code}: {len(content)} bytes received")
                        print(f"Content preview: {content[:200]}...")

                    # Check if it looks like a marimo server
                    if (
                        "marimo" in content.lower()
                        or "<!doctype html>" in content.lower()
                    ):
                        if debug:
                            print("✅ Marimo server content detected")
                        return True
                    else:
                        if debug:
                            print("⚠️ Response doesn't look like marimo server")
                        return False

            except urllib.error.HTTPError as e:
                if debug:
                    print(f"❌ HTTP Error {e.code}: {e.reason}")
                return False
            except urllib.error.URLError as e:
                if debug:
                    print(f"❌ URL Error: {e.reason}")
                return False

        except Exception as e:
            if debug:
                print(f"❌ URL test failed: {e}")
            return False

    def _run_diagnostics(self, args) -> None:
        """Run comprehensive diagnostics for troubleshooting."""
        print("🔍 Running Marimo Magic Diagnostics")
        print("=" * 50)

        # Test 1: Environment check
        print("\n1️⃣ Environment Check:")

        # Check UV availability
        uv_available = False
        try:
            result = subprocess.run(
                ["uv", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                uv_available = True
                print(f"✅ UV available: {result.stdout.strip()}")
            else:
                print("❌ UV not available")
        except Exception as e:
            print(f"❌ UV not available: {e}")

        # Check marimo availability
        print("\n📦 Marimo availability:")
        for cmd_prefix in (["uv", "run"] if uv_available else [], ["python", "-m"]):
            try:
                test_cmd = cmd_prefix + ["marimo", "--version"]
                result = subprocess.run(
                    test_cmd, capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    print(f"✅ {' '.join(cmd_prefix)} marimo: {result.stdout.strip()}")
                else:
                    print(f"❌ {' '.join(cmd_prefix)} marimo failed: {result.stderr}")
            except Exception as e:
                print(f"❌ {' '.join(cmd_prefix)} marimo failed: {e}")

        # Test 2: Port allocation
        print("\n2️⃣ Port Allocation Test:")
        try:
            test_port = self._find_free_port()
            print(f"✅ Found free port: {test_port}")
        except Exception as e:
            print(f"❌ Port allocation failed: {e}")
            return

        # Test 3: Server startup tests
        print("\n3️⃣ Server Startup Tests:")

        # Test run mode
        print("\n▶️ Testing RUN mode:")
        self._test_mode("run", test_port, uv_available, debug=True)

        # Test edit mode
        print("\n📝 Testing EDIT mode:")
        self._test_mode("edit", test_port + 1, uv_available, debug=True)

        # Test 4: Colab environment
        print("\n4️⃣ Environment Detection:")
        if self._is_colab():
            print("✅ Google Colab environment detected")
            try:
                proxy_url = self._get_colab_proxy_url(test_port)
                print(f"✅ Colab proxy URL: {proxy_url}")
            except Exception as e:
                print(f"❌ Colab proxy URL failed: {e}")
        else:
            print("✅ Regular Jupyter environment detected")

        print("\n" + "=" * 50)
        print("🏁 Diagnostics complete!")
        print("💡 If issues persist, try: %marimo --debug --edit")

    def _test_mode(
        self, mode: str, port: int, uv_available: bool, debug: bool = False
    ) -> None:
        """Test a specific marimo mode (run or edit)."""
        import os  # Add missing import

        # Build command
        if uv_available:
            cmd = ["uv", "run", "marimo", mode]
        else:
            cmd = ["python", "-m", "marimo", mode]

        # Add temporary notebook for run mode testing
        temp_notebook = None
        if mode == "run":
            temp_notebook = self._create_temp_notebook()
            cmd.append(temp_notebook)

        cmd.extend(
            ["--host", "127.0.0.1", "--port", str(port), "--headless", "--no-token"]
        )

        # Add sandbox flag for files with inline dependencies to avoid terminal interaction
        if temp_notebook and self._has_inline_dependencies(temp_notebook):
            cmd.append("--sandbox")
            if debug:
                print("📦 Adding --sandbox flag for inline dependencies")

        print(f"   Command: {' '.join(cmd)}")

        try:
            # Start process
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            env["MPLBACKEND"] = (
                "Agg"  # Fix matplotlib backend for headless environments (Lightning compatibility)
            )

            if debug:
                print("🔧 Environment variables set:")
                print("   PYTHONUNBUFFERED=1")
                print("   MPLBACKEND=Agg (for matplotlib/Lightning compatibility)")

            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True
            )

            print(f"   Process PID: {process.pid}")

            # Wait for startup
            if self._wait_for_server(port, timeout=20, debug=False):
                print("   ✅ Server started successfully")

                # Test URL
                if self._test_marimo_url(
                    port, is_edit_mode=(mode == "edit"), debug=False
                ):
                    print("   ✅ URL validation successful")
                else:
                    print("   ⚠️ URL validation failed")

                # Clean up
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print("   ✅ Server stopped cleanly")
                except Exception:
                    try:
                        process.kill()
                        print("   ⚠️ Server force-killed")
                    except Exception:
                        print("   ❌ Failed to stop server")
            else:
                print("   ❌ Server failed to start")

                # Show error output
                try:
                    stdout, stderr = process.communicate(timeout=2)
                    if stderr:
                        print(f"   STDERR: {stderr[:200]}...")
                except Exception:
                    pass

                # Clean up
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    try:
                        process.kill()
                    except Exception:
                        pass

        except Exception as e:
            print(f"   ❌ Test failed: {e}")

        # Clean up temporary file
        if temp_notebook:
            try:
                import os

                os.unlink(temp_notebook)
            except Exception:
                pass

        # Clean up port
        self.used_ports.discard(port)

    @line_magic
    @magic_arguments()
    @argument(
        "notebook_path",
        nargs="?",
        default=None,
        help="Path to the marimo notebook file",
    )
    @argument(
        "--port",
        type=int,
        default=None,
        help="Port for the marimo server, auto-assigned if not specified",
    )
    @argument(
        "--height",
        type=int,
        default=600,
        help="Height of the embedded iframe in pixels, default is 600",
    )
    @argument(
        "--width",
        type=str,
        default="100%",
        help="Width of the embedded iframe, default is 100 percent",
    )
    @argument(
        "--stop",
        type=int,
        default=None,
        help="Stop the marimo server on the specified port",
    )
    @argument("--debug", action="store_true", help="Enable debug output")
    @argument(
        "--test-connection",
        action="store_true",
        help="Test connection to marimo server",
    )
    @argument(
        "--edit",
        action="store_true",
        help="Run marimo in edit mode instead of run mode",
    )
    @argument(
        "--diagnose",
        action="store_true",
        help="Run comprehensive diagnostics for troubleshooting",
    )
    def marimo(self, line):
        """
        Start a marimo server and display it in the notebook.

        Usage examples:
            %marimo                              - Start with default settings
            %marimo notebook.py                  - Start with specific notebook
            %marimo --port 2718                  - Use specific port
            %marimo --height 800                 - Custom height
            %marimo --stop 2718                  - Stop server on port 2718
            %marimo --debug                      - Enable debug output
            %marimo --test-connection            - Test server connection
            %marimo --edit                       - Run in edit mode instead of run mode
            %marimo --diagnose                   - Run comprehensive diagnostics
        """
        import os  # Add missing import

        args = parse_argstring(self.marimo, line)

        # Handle stopping a server
        if args.stop:
            if args.stop in self.processes:
                process = self.processes[args.stop]
                try:
                    if process.poll() is None:
                        process.terminate()
                        process.wait(timeout=5)
                    del self.processes[args.stop]
                    self.used_ports.discard(args.stop)

                    # Clean up temp notebook if exists
                    if args.stop in self.temp_notebooks:
                        try:
                            os.unlink(self.temp_notebooks[args.stop])
                            del self.temp_notebooks[args.stop]
                            if args.debug:
                                print(f"🗑️ Cleaned up temporary notebook")
                        except Exception as e:
                            if args.debug:
                                print(f"⚠️ Failed to clean up temp notebook: {e}")

                    print(f"✅ Stopped marimo server on port {args.stop}")
                except Exception as e:
                    print(f"❌ Error stopping server on port {args.stop}: {e}")
            else:
                print(f"❌ No server found on port {args.stop}")
            return

        # Handle connection testing
        if args.test_connection:
            if args.port:
                self._test_connection(args.port)
            else:
                print("❌ Please specify a port with --port for connection testing")
            return

        # Handle diagnostics
        if args.diagnose:
            self._run_diagnostics(args)
            return

        # Determine port
        port = args.port if args.port else self._find_free_port()

        # Check if UV is available
        uv_available = False
        try:
            result = subprocess.run(
                ["uv", "--version"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                uv_available = True
                if args.debug:
                    print(f"✅ UV available: {result.stdout.strip()}")
        except Exception as e:
            if args.debug:
                print(f"⚠️ UV not available: {e}")

        # Build command
        if uv_available:
            cmd = ["uv", "run", "marimo"]
            if args.edit:
                cmd.append("edit")
                if args.debug:
                    print(
                        "📝 Using UV to run marimo in EDIT mode (enables script dependencies)"
                    )
            else:
                cmd.append("run")
                if args.debug:
                    print(
                        "📦 Using UV to run marimo in RUN mode (enables script dependencies)"
                    )
        else:
            cmd = ["python", "-m", "marimo"]
            if args.edit:
                cmd.append("edit")
                if args.debug:
                    print("📝 Using python -m marimo edit")
            else:
                cmd.append("run")
                if args.debug:
                    print("🐍 Using python -m marimo run")

        # Add notebook path if provided, or create default for run mode
        if args.notebook_path:
            cmd.append(args.notebook_path)
        elif not args.edit:
            # Run mode requires a file - create a minimal temporary notebook
            temp_notebook = self._create_temp_notebook()
            cmd.append(temp_notebook)
            self.temp_notebooks[port] = temp_notebook  # Track for cleanup
            if args.debug:
                print(f"📝 Created temporary notebook: {temp_notebook}")

        # Add server options
        cmd.extend(
            ["--host", "127.0.0.1", "--port", str(port), "--headless", "--no-token"]
        )

        # Add sandbox flag for files with inline dependencies to avoid terminal interaction
        if args.notebook_path and self._has_inline_dependencies(args.notebook_path):
            cmd.append("--sandbox")
            if args.debug:
                print("📦 Adding --sandbox flag for inline dependencies")

        if args.debug:
            print(f"🚀 Starting marimo with command: {' '.join(cmd)}")

        # Start the marimo server
        try:
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"  # Ensure output is not buffered
            env["MPLBACKEND"] = (
                "Agg"  # Fix matplotlib backend for headless environments (Lightning compatibility)
            )

            if args.debug:
                print("🔧 Environment variables set:")
                print("   PYTHONUNBUFFERED=1")
                print("   MPLBACKEND=Agg (for matplotlib/Lightning compatibility)")

            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True
            )

            self.processes[port] = process

            if args.debug:
                print(f"📊 Process started with PID: {process.pid}")

        except Exception as e:
            print(f"❌ Failed to start marimo server: {e}")
            return

        # Wait for server to start
        recommended_timeout = self._get_recommended_timeout(args.notebook_path)
        if args.notebook_path and self._has_inline_dependencies(args.notebook_path):
            print(
                f"📦 Notebook has inline dependencies - using extended timeout ({recommended_timeout}s)"
            )
            if args.debug:
                print(
                    "    Heavy packages like torch/transformers may take 3-5 minutes to install"
                )

        if not self._wait_for_server(
            port, timeout=recommended_timeout, debug=args.debug
        ):
            print(f"❌ Failed to start marimo server on port {port}")

            # Enhanced debugging for edit mode
            if args.edit:
                print("🔍 Edit mode specific debugging:")
                print(f"   Command used: {' '.join(cmd)}")
                print("   Edit mode may take longer to start...")

                # Try waiting a bit longer for edit mode
                print("⏳ Waiting additional time for edit mode startup...")
                if self._wait_for_server(port, timeout=15, debug=True):
                    print("✅ Edit mode server started after extended wait")

                    # Validate the URL is working
                    if self._test_marimo_url(port, is_edit_mode=True, debug=args.debug):
                        print("✅ Edit mode URL validation successful")
                    else:
                        print(
                            "⚠️ Edit mode URL validation failed - server may not be ready"
                        )

                    # Continue with display
                    if self._is_colab():
                        self._display_for_colab(
                            port, args.height, args.width, args.debug, args.edit
                        )
                    else:
                        self._display_for_regular_jupyter(
                            port, args.height, args.width, args.debug, args.edit
                        )

                    mode = "EDIT" if args.edit else "RUN"
                    print(
                        f"🎉 Marimo server started successfully on port {port} in {mode} mode"
                    )
                    if args.debug:
                        print(f"💡 Use '%marimo --stop {port}' to stop this server")
                    return

            # Clean up the failed process
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
            except Exception:
                pass

            # Show process output for debugging
            try:
                stdout, stderr = process.communicate(timeout=1)
                if stdout:
                    print(f"STDOUT: {stdout}")
                if stderr:
                    print(f"STDERR: {stderr}")
            except Exception:
                pass

            if port in self.processes:
                del self.processes[port]
            self.used_ports.discard(port)
            return

        # Server started successfully - validate URL
        if args.edit and args.debug:
            print("🔍 Validating edit mode URL...")
            if not self._test_marimo_url(port, is_edit_mode=True, debug=True):
                print("⚠️ Warning: URL validation failed but server is running")
        elif args.debug:
            print("🔍 Validating run mode URL...")
            if not self._test_marimo_url(port, is_edit_mode=False, debug=True):
                print("⚠️ Warning: URL validation failed but server is running")

        # Display appropriate UI based on context
        if self._is_colab():
            self._display_for_colab(
                port, args.height, args.width, args.debug, args.edit
            )
        else:
            self._display_for_regular_jupyter(
                port, args.height, args.width, args.debug, args.edit
            )

        mode = "EDIT" if args.edit else "RUN"
        print(f"🎉 Marimo server started successfully on port {port} in {mode} mode")
        if args.debug:
            print(f"💡 Use '%marimo --stop {port}' to stop this server")

    def _create_temp_notebook(self) -> str:
        """Create a minimal temporary marimo notebook for run mode."""
        import tempfile
        import os

        # Create a temporary file with marimo notebook content
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"marimo_temp_{os.getpid()}.py")

        # Minimal marimo notebook content
        notebook_content = '''import marimo

__generated_with = "0.14.9"
app = marimo.App()

@app.cell
def __():
    import marimo as mo
    return mo,

@app.cell
def __(mo):
    mo.md("""
    # 🎯 Welcome to Marimo!
    
    This is a temporary notebook created by the Marimo Magic command.
    
    **Features:**
    - Interactive Python notebooks
    - Reactive execution
    - Beautiful UI components
    
    **Next steps:**
    - Create your own notebook file
    - Use `%marimo my_notebook.py` to load it
    - Use `%marimo --edit` to create new notebooks
    """)
    return

@app.cell
def __(mo):
    mo.md("**Try editing this cell!** Add some Python code below:")
    return

@app.cell
def __():
    # Add your code here
    print("Hello from Marimo! 🎉")
    return

if __name__ == "__main__":
    app.run()
'''

        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(notebook_content)
            return temp_path
        except Exception as e:
            # Fallback to a simpler approach
            print(f"⚠️ Failed to create temp notebook: {e}")
            # Return a simple Python file
            simple_path = os.path.join(temp_dir, f"simple_marimo_{os.getpid()}.py")
            with open(simple_path, "w", encoding="utf-8") as f:
                f.write('print("Hello from Marimo Magic!")')
            return simple_path

    def _has_inline_dependencies(self, file_path: str) -> bool:
        """Check if a file has inline dependencies (PEP 723)."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(500)  # Check first 500 chars
                return "# /// script" in content and "dependencies" in content
        except Exception:
            return False

    def _get_recommended_timeout(self, file_path: str = None) -> int:
        """Get recommended timeout based on whether file has inline dependencies."""
        if file_path and self._has_inline_dependencies(file_path):
            return 300  # 5 minutes for files with inline dependencies
        return 30  # 30 seconds for regular files


def load_ipython_extension(ipython):
    """Load the marimo magic extension."""
    magic_instance = MarimoMagics(ipython)
    ipython.register_magic_function(magic_instance.marimo, "line", "marimo")
    ipython._marimo_magic_instance = magic_instance


def unload_ipython_extension(ipython):
    """Unload the marimo magic extension."""
    # Clean up any running processes
    if hasattr(ipython, "_marimo_magic_instance"):
        del ipython._marimo_magic_instance


# For direct import usage
def register_marimo_magic():
    """Register marimo magic in current IPython session"""
    try:
        ipython = get_ipython()
        if ipython:
            load_ipython_extension(ipython)
        else:
            print("❌ Not in an IPython environment")
    except Exception as e:
        print(f"❌ Failed to register marimo magic: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    register_marimo_magic()
