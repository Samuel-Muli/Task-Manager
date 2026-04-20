🖥️ Task Manager (Terminal System Monitor)

A terminal-based Task Manager / System Monitor built with Python, using curses for a clean UI and psutil for system statistics.

It displays:

✅ CPU Total Usage
✅ Per-Core CPU Usage Bars
✅ RAM Usage
✅ Disk Usage
✅ Network Speed (Upload/Download MB/s)
✅ Network Total Sent/Received
⚠️ CPU Temperature (only if supported by OS)
📌 Features
Auto-scaling UI (adapts to terminal resizing)
Colored performance bars:
Green = Low usage
Yellow = Medium usage
Red = High usage
Real-time updates
Safe rendering (won’t crash if terminal is small)
Quit anytime by pressing q
🛠️ Requirements
Python 3.8+
psutil
curses (Linux/Mac default)
windows-curses (Windows only)
📦 Installation
1. Clone the Repository
git clone https://github.com/your-username/Task-Manager.git
cd Task-Manager
2. Create a Virtual Environment
python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Linux/Mac

source venv/bin/activate
3. Install Dependencies
pip install psutil

If you're on Windows, also install:

pip install windows-curses
▶️ Run the Program
python main.py
🎮 Controls
Key	Action
q	Quit program
Ctrl + C	Force quit (safe exit supported)
📊 Output Preview

The monitor shows:

CPU Total bar
RAM bar
Disk usage bar
CPU temperature line (if available)
Network upload/download speed
Per-core CPU usage bars
⚠️ CPU Temperature Support

CPU temperature is not always available, especially on Windows.
Most Windows systems will show:

CPU Temp: N/A (Windows often blocks this)

For accurate temperature readings on Windows, you may need tools like:

LibreHardwareMonitor
OpenHardwareMonitor
📁 Project Structure
Task-Manager/
│── main.py
│── README.md
│── venv/
🚀 Future Improvements (Ideas)
GPU usage + GPU temperature
Process list viewer (like real Task Manager)
Sorting by CPU/RAM usage
Kill process support
Cross-platform temperature support
📜 License

This project is licensed under the MIT License.
Feel free to use and modify it.