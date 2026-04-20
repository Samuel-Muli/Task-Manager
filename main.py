import curses
import psutil
import time


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_color_pair(value):
    if value < 50:
        return 1  # Green
    elif value < 80:
        return 2  # Yellow
    return 3      # Red


def safe_addstr(stdscr, y, x, text, color=0):
    height, width = stdscr.getmaxyx()

    if y < 0 or y >= height:
        return
    if x < 0 or x >= width:
        return

    max_len = width - x - 1
    if max_len <= 0:
        return

    text = text[:max_len]

    try:
        stdscr.addstr(y, x, text, color)
    except curses.error:
        pass


def draw_bar(stdscr, y, x, total_width, label, value):
    value = clamp(value, 0, 100)
    color = curses.color_pair(get_color_pair(value))

    label_text = f"{label}: "
    percent_text = f"{value:6.2f}%"

    bar_space = total_width - len(label_text) - len(percent_text) - 4
    if bar_space < 5:
        safe_addstr(stdscr, y, x, f"{label_text}{value:.1f}%", color)
        return

    filled = int((value / 100) * bar_space)
    empty = bar_space - filled

    bar_text = "[" + "#" * filled + " " * empty + "]"

    safe_addstr(stdscr, y, x, label_text, curses.color_pair(1))
    safe_addstr(stdscr, y, x + len(label_text), bar_text, color)
    safe_addstr(stdscr, y, x + len(label_text) + len(bar_text) + 1, percent_text, color)


def get_cpu_temp():
    """
    Returns CPU temperature in Celsius if available.
    On Windows, this often returns None.
    """
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None

        for name, entries in temps.items():
            for entry in entries:
                if entry.current is not None:
                    return entry.current

        return None
    except Exception:
        return None


def draw_monitor(stdscr):
    try:
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(200)

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_RED, -1)

        # For network speed calculation
        last_net = psutil.net_io_counters()
        last_time = time.time()

        while True:
            stdscr.erase()
            height, width = stdscr.getmaxyx()
            content_width = max(20, width - 4)

            # Metrics
            cpu_total = psutil.cpu_percent(interval=None)
            cpu_cores = psutil.cpu_percent(interval=None, percpu=True)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent

            temp = get_cpu_temp()

            net = psutil.net_io_counters()
            now = time.time()
            dt = max(now - last_time, 0.001)

            sent_per_sec = (net.bytes_sent - last_net.bytes_sent) / dt
            recv_per_sec = (net.bytes_recv - last_net.bytes_recv) / dt

            sent_mb_s = sent_per_sec / (1024 * 1024)
            recv_mb_s = recv_per_sec / (1024 * 1024)

            last_net = net
            last_time = now

            # Header
            safe_addstr(stdscr, 0, 2, "🖥️  Livestream Monitor (Auto-Scaling)", curses.color_pair(1))
            safe_addstr(stdscr, 1, 2, "-" * (width - 4), curses.color_pair(1))

            y = 3

            # Main system bars
            draw_bar(stdscr, y, 2, content_width, "CPU Total", cpu_total)
            y += 2

            draw_bar(stdscr, y, 2, content_width, "RAM", ram)
            y += 2

            draw_bar(stdscr, y, 2, content_width, "Disk", disk)
            y += 2

            # Temperature line
            if temp is None:
                temp_text = "CPU Temp: N/A (Windows often blocks this)"
            else:
                temp_text = f"CPU Temp: {temp:.1f}°C"

            safe_addstr(stdscr, y, 2, temp_text, curses.color_pair(2))
            y += 2

            # Network speed
            safe_addstr(
                stdscr, y, 2,
                f"NET Speed  ↑ {sent_mb_s:.2f} MB/s   ↓ {recv_mb_s:.2f} MB/s",
                curses.color_pair(3)
            )
            y += 1

            safe_addstr(
                stdscr, y, 2,
                f"NET Total  Sent: {net.bytes_sent / (1024 * 1024):.2f} MB   "
                f"Recv: {net.bytes_recv / (1024 * 1024):.2f} MB",
                curses.color_pair(3)
            )
            y += 2

            # Per-core CPU section
            safe_addstr(stdscr, y, 2, "Per-Core CPU Usage:", curses.color_pair(1))
            y += 1

            # Draw per-core bars until we run out of space
            for i, core_val in enumerate(cpu_cores):
                if y >= height - 3:
                    safe_addstr(stdscr, y, 2, "... (resize terminal to see more cores)", curses.color_pair(2))
                    break

                draw_bar(stdscr, y, 2, content_width, f"Core {i}", core_val)
                y += 1

            # Footer
            safe_addstr(stdscr, height - 2, 2, "Press 'q' to quit | Ctrl+C also works", curses.color_pair(2))

            stdscr.refresh()

            key = stdscr.getch()
            if key == ord("q"):
                break

            time.sleep(0.2)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(draw_monitor)