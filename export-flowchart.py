import subprocess
import os
import re

def render_mermaid_to_png(input_file, output_file):
    """
    Reads a .mmd file containing a VS Code cell with a Mermaid diagram,
    extracts the diagram code, and renders it to a PNG file using mmdc.
    """
    try:
        # Read the content of the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract the Mermaid code from within the <VSCode.Cell> tag
        match = re.search(r'<VSCode.Cell.*?>(.*)</VSCode.Cell>', content, re.DOTALL)
        if not match:
            print(f"Error: Could not find Mermaid code within a <VSCode.Cell> tag in {input_file}")
            # As a fallback, assume the file contains only mermaid code
            mermaid_code = content.strip()
        else:
            mermaid_code = match.group(1).strip()

        if not mermaid_code:
            print(f"Error: Extracted Mermaid code is empty.")
            return

        print("Successfully extracted Mermaid code. Rendering to PNG...")

        # Command to execute. We pipe the code to mmdc's stdin.
        command = [
            'mmdc',
            '-o', output_file
        ]

        # Execute the command
        result = subprocess.run(
            command,
            input=mermaid_code,
            capture_output=True,
            text=True,
            encoding='utf-8',
            shell=True # Use shell=True on Windows for better path handling
        )

        if result.returncode == 0:
            print(f"Successfully created flowchart at: {os.path.abspath(output_file)}")
        else:
            print("Error generating flowchart.")
            print(f"mmdc stderr:\n{result.stderr}")

    except FileNotFoundError:
        print("Error: 'mmdc' command not found.")
        print("Please ensure Node.js and @mermaid-js/mermaid-cli are installed and in your system's PATH.")
        print("Installation command: npm install -g @mermaid-js/mermaid-cli")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    input_mmd_file = 'flowchart.mmd'
    output_png_file = 'flowchart.png'
    render_mermaid_to_png(input_mmd_file, output_png_file)