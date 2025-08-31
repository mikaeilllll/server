#!/usr/bin/env python3
import os
import sys
import pty
import termios
import tty
import fcntl
import select
import struct
import time
import random
import signal
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.box import SQUARE
from rich.text import Text
from rich.align import Align
from rich.live import Live

console = Console()

# Global variables for connection state
current_server_config = None
auto_reconnect = True
reconnection_attempts = 0
max_reconnection_attempts = 5

BASE_MODULE_FORMAT = '''[MODULE]
name=Module Name Here
id=module_id_here
version=v1.0
author=mikaeilllll
description=Module Description Here
path=/system/bin/module_binary

[FILES]
update-binary=#!/sbin/sh
TMPDIR=/dev/tmp
MOUNTPATH=/dev/magisk_img
MODPATH=$TMPDIR/mod
LATESTARTSERVICE=$MODPATH/service.sh
mkdir -p $MODPATH
unzip -o "$3" -d $MODPATH
set_perm_recursive $MODPATH 0 0 0755 0644
sh $LATESTARTSERVICE &

updater-script=#MAGISK

service.sh=#!/system/bin/sh;while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 1; done;echo "Module Service Started" > /dev/kmsg;# Add your commands here

main.sh=#!/system/bin/sh;chmod 644 /sys/your/target/path;# Add your permission commands here

[CONFIG]
minmagisk=20400
needramdisk=false
support_device=universal'''

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def clear():
    os.system('clear')

def create_cyber_frame(width):
    """ساخت فریم سایبرپانک"""
    if random.random() < 0.3:
        return f"0x{random.randint(0, 0xFFFFFFF):x}"
    
    chars = "░▒▓█▄▀▌▐⌠⌡"
    line = ' ' * width
    num_chars = random.randint(width // 10, width // 5)
    
    for _ in range(num_chars):
        pos = random.randint(0, width-1)
        char = random.choice(chars)
        line = line[:pos] + char + line[pos+1:]
    
    return line

def create_static_header() -> Text:
    header = Text()
    header.append("Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-08-29 16:25:02\n", style="bright_black")
    header.append("Current User's Login: mikaeilllll", style="bright_black")
    return header

def cyber_boot_sequence():
    width = os.get_terminal_size().columns
    clear()
    console.print(create_static_header())
    print()

    logo = """
    ╔═══════════════════════════════════╗
    ║  SEGFAULT SECURE PROXY SYSTEM     ║
    ║  Advanced Tunneling Protocol      ║
    ╚═══════════════════════════════════╝
    """
    for line in logo.split('\n'):
        console.print(f"[green]{line}[/]")
        time.sleep(0.02)

    boot_steps = [
        ("INITIALIZING KERNEL", 0.1),
        ("LOADING SECURITY MODULES", 0.08),
        ("ESTABLISHING SECURE CHANNEL", 0.1),
        ("CONFIGURING NETWORK PROTOCOLS", 0.08),
        ("STARTING PROXY SERVICES", 0.1)
    ]

    with console.status("[bold green]BOOTING SYSTEM[/]", spinner="line") as status:
        for step, duration in boot_steps:
            status.update(f"[bold green]{step}[/]")
            
            cyber_line = create_cyber_frame(width)
            console.print(f"[dim green]{cyber_line}[/]")
            time.sleep(0.02)
            
            console.print(f"[bright_black]{hex(random.randint(0, 0xFFFFFFFF))}[/]")
            time.sleep(duration)

    success_msg = "SYSTEM READY"
    padding = (width - len(success_msg)) // 2
    console.print(f"\n{'=' * width}")
    console.print(f"[bold green]{' ' * padding}{success_msg}[/]")
    console.print(f"{'=' * width}\n")
    time.sleep(0.2)

def create_header() -> Panel:
    header = Text()
    header.append("⚡ SEGFAULT PROXY MANAGER ⚡\n", style="bold green")
    header.append("UTC: 2025-08-29 16:25:02", style="bright_black")
    
    return Panel(
        Align.center(header),
        box=SQUARE,
        border_style="green",
        padding=(1, 2)
    )

def create_main_menu() -> Panel:
    menu_text = Text()
    
    menu_text.append("\n[1] ", style="bright_black")
    menu_text.append("SEGFAULT", style="green")
    menu_text.append(" Proxy Server Manager", style="bright_black")
    
    menu_text.append("\n[2] ", style="bright_black") 
    menu_text.append("MAGISK", style="green")
    menu_text.append(" Module Creator", style="bright_black")
    
    menu_text.append("\n[3] ", style="bright_black")
    menu_text.append("HELP", style="green") 
    menu_text.append(" Module Format Guide", style="bright_black")
    
    return Panel(
        menu_text,
        box=SQUARE,
        border_style="green",
        title="Main Menu",
        padding=(1, 2)
    )

def create_menu() -> Panel:
    menu_text = Text()
    for i, (name, config) in enumerate([
        ("DEFAULT", "-D 8080"),
        ("TOR", "-L8080:172.20.0.111:9050")
    ], 1):
        menu_text.append(f"\n[{i}] ", style="bright_black")
        menu_text.append(f"{name:<10}", style="green")
        menu_text.append(f" {config}", style="bright_black")
    
    return Panel(
        menu_text,
        box=SQUARE,
        border_style="green",
        title="Available Servers",
        padding=(1, 2)
    )

def connection_animation():
    width = os.get_terminal_size().columns
    clear()
    
    console.print(Panel(
        "[bold green]INITIATING SECURE CONNECTION[/]",
        border_style="green",
        box=SQUARE
    ))

    patterns = [
        "▀▄▀▄▀▄",
        "═══════",
        "▓▒░▒▓▒░",
        "■□■□■□■",
        "●○●○●○●"
    ]
    
    with console.status("", spinner="line") as status:
        for i in range(3):
            pattern = patterns[i]
            status.update(f"[bold green]Establishing Connection Layer {i+1}[/]")
            
            console.print(f"[dim green]{pattern * (width // len(pattern) + 1)}[/]")
            time.sleep(0.02)
            
            technical_info = [
                f"Protocol: Layer{i+1}_SEC_{random.randint(1000, 9999)}",
                f"Encryption: AES_{random.randint(128, 512)}",
                f"Channel: {random.randint(1, 99)}/{random.randint(100, 999)}",
                f"Status: ACTIVE_{random.randbytes(4).hex().upper()}"
            ]
            console.print(f"[bright_black]{' | '.join(technical_info)}[/]")
            time.sleep(0.1)
    
    console.print("\n[bold green]CONNECTION ESTABLISHED[/]")
    console.print(f"[bright_black]Session ID: {random.randbytes(8).hex().upper()}[/]\n")
    time.sleep(0.2)

def reconnection_animation(attempt):
    """انیمیشن اتصال مجدد"""
    width = os.get_terminal_size().columns
    
    console.print(f"\n[yellow]CONNECTION LOST - ATTEMPTING RECONNECTION ({attempt}/{max_reconnection_attempts})[/]")
    
    reconnect_patterns = ["⟳", "⟲", "↻", "↺"]
    
    for i in range(3):
        pattern = reconnect_patterns[i % len(reconnect_patterns)]
        console.print(f"[yellow]{pattern * (width // 10)} RECONNECTING... {pattern * (width // 10)}[/]")
        time.sleep(0.3)
    
    console.print(f"[green]Reconnecting to server with previous configuration...[/]")
    time.sleep(0.5)

def create_magisk_module(module_info):
    try:
        temp_dir = "/storage/emulated/0/Download/temp_module"
        os.makedirs(f"{temp_dir}/META-INF/com/google/android", exist_ok=True)
        os.makedirs(f"{temp_dir}/system/bin", exist_ok=True)

        info = {}
        section = None
        for line in module_info.split('\n'):
            if line.strip():
                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                    info[section] = {}
                elif '=' in line and section:
                    key, value = line.split('=', 1)
                    info[section][key.strip()] = value.strip()

        with open(f"{temp_dir}/module.prop", 'w') as f:
            f.write(f"""id={info['MODULE']['id']}
name={info['MODULE']['name']}
version={info['MODULE']['version']}
versionCode=1
author={info['MODULE']['author']}
description={info['MODULE']['description']}""")

        for file_name, content in info['FILES'].items():
            file_path = os.path.join(temp_dir, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)

        import shutil
        zip_path = f"/storage/emulated/0/Download/{info['MODULE']['id']}.zip"
        shutil.make_archive(zip_path[:-4], 'zip', temp_dir)
        
        shutil.rmtree(temp_dir)
        
        return True, zip_path
    except Exception as e:
        return False, str(e)

def show_help_guide():
    clear()
    cyber_boot_sequence()
    
    guide_text = Text()
    guide_text.append("\n📖 Module Format Guide\n\n", style="bold green")
    guide_text.append("1. [MODULE] Section:", style="bright_yellow")
    guide_text.append("\n   • name: Your module's display name", style="bright_black")
    guide_text.append("\n   • id: Unique identifier (no spaces)", style="bright_black")
    guide_text.append("\n   • version: Module version", style="bright_black")
    guide_text.append("\n   • description: Brief module description", style="bright_black")
    
    guide_text.append("\n\n2. [FILES] Section:", style="bright_yellow")
    guide_text.append("\n   • update-binary: Installation script", style="bright_black")
    guide_text.append("\n   • updater-script: Magisk identifier", style="bright_black")
    guide_text.append("\n   • service.sh: Runtime commands", style="bright_black")
    guide_text.append("\n   • main.sh: Permission settings", style="bright_black")
    
    guide_text.append("\n\n3. [CONFIG] Section:", style="bright_yellow")
    guide_text.append("\n   • minmagisk: Minimum Magisk version", style="bright_black")
    guide_text.append("\n   • support_device: Target device", style="bright_black")
    
    guide_text.append("\n\n💡 Tips:", style="bold green")
    guide_text.append("\n• Use semicolons (;) to separate commands in service.sh", style="bright_black")
    guide_text.append("\n• Avoid extra spaces in commands", style="bright_black")
    guide_text.append("\n• Type 'DONE' on a new line when finished", style="bright_black")
    
    guide_text.append("\n\n📝 Example Format:", style="bold green")
    guide_text.append(f"\n{BASE_MODULE_FORMAT}", style="bright_black")
    
    console.print(Panel(
        Align.center(guide_text),
        title="[bold green]Module Creation Guide[/]",
        border_style="green",
        box=SQUARE,
        padding=(1, 2)
    ))
    
    console.print("\n[green]Press Enter to return to main menu[/]")
    input()

def print_menu():
    clear()
    cyber_boot_sequence()
    console.print(create_header())
    console.print(create_menu())
    console.print("\n[bright_black][ [green]Q[/]uit | [green]C[/]lear | [green]R[/]econnect ][/]")

def shutdown_sequence():
    clear()
    width = os.get_terminal_size().columns
    
    console.print("[red]INITIATING SHUTDOWN SEQUENCE[/]")
    
    for i in range(3, 0, -1):
        console.print(f"[yellow]System shutdown in {i}...[/]")
        pattern = "▓▒░" * (width // 3)
        console.print(f"[dim red]{pattern}[/]")
        time.sleep(0.2)
    
    clear()
    console.print("[bold red]SYSTEM OFFLINE[/]")
    time.sleep(0.3)

def check_connection():
    """بررسی وضعیت اتصال"""
    try:
        import subprocess
        result = subprocess.run(['ping', '-c', '1', '-W', '2', 'google.com'], 
                              capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except:
        return False

def run_proxy(cmd):
    global current_server_config, reconnection_attempts, auto_reconnect
    
    current_server_config = cmd
    reconnection_attempts = 0
    
    while True:
        try:
            if reconnection_attempts == 0:
                clear()
                connection_animation()
            else:
                reconnection_animation(reconnection_attempts)
            
            # اجرای SSH با تعامل کامل
            import subprocess
            process = subprocess.Popen(
                f"ssh -tt segfault {cmd}",
                shell=True,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                preexec_fn=os.setsid
            )
            
            try:
                return_code = process.wait()
            except KeyboardInterrupt:
                console.print("\n[yellow]CONNECTION MANUALLY TERMINATED[/]")
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    process.wait(timeout=5)
                except:
                    try:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    except:
                        pass
                return
            
            if return_code != 0 and auto_reconnect and reconnection_attempts < max_reconnection_attempts:
                reconnection_attempts += 1
                
                if not check_connection():
                    console.print("\n[red]No internet connection detected. Waiting for connection...[/]")
                    while not check_connection():
                        time.sleep(2)
                    console.print("\n[green]Internet connection restored![/]")
                
                console.print(f"\n[yellow]Attempting reconnection {reconnection_attempts}/{max_reconnection_attempts}...[/]")
                time.sleep(2)
                continue
            elif return_code != 0 and reconnection_attempts >= max_reconnection_attempts:
                console.print(f"\n[red]Max reconnection attempts ({max_reconnection_attempts}) reached. Returning to menu.[/]")
                break
            else:
                break
                
        except Exception as e:
            console.print(f"\n[red]ERROR: {str(e)}[/]")
            if auto_reconnect and reconnection_attempts < max_reconnection_attempts:
                reconnection_attempts += 1
                console.print(f"\n[yellow]Attempting reconnection due to error... ({reconnection_attempts}/{max_reconnection_attempts})[/]")
                time.sleep(2)
                continue
            else:
                break
    
    current_server_config = None
    reconnection_attempts = 0

def main():
    global auto_reconnect, current_server_config
    
    proxies = {
        "1": "-D 8080",
        "2": "-L8080:172.20.0.111:9050"
    }
    
    while True:
        clear()
        cyber_boot_sequence()
        console.print(create_header())
        console.print(create_main_menu())
        
        reconnect_status = "[green]ON[/]" if auto_reconnect else "[red]OFF[/]"
        console.print(f"\n[bright_black]Auto-Reconnect: {reconnect_status} | [ [green]Q[/]uit | [green]C[/]lear | [green]A[/]uto-reconnect toggle ][/]")
        
        choice = get_key().lower()
        
        if choice == '1':  # SEGFAULT
            while True:
                print_menu()
                sub_choice = get_key().lower()
                
                if sub_choice in proxies:
                    run_proxy(proxies[sub_choice])
                    console.print("\n[green]Press Enter to return[/]")
                    input()
                elif sub_choice == 'r' and current_server_config:
                    console.print("\n[yellow]Manually reconnecting to last server...[/]")
                    run_proxy(current_server_config)
                    console.print("\n[green]Press Enter to return[/]")
                    input()
                elif sub_choice == 'q':
                    break
                elif sub_choice == 'c':
                    clear()
                    
        elif choice == '2':  # MAGISK
            clear()
            cyber_boot_sequence()
            console.print("[bold green]Enter Module Information (type 'DONE' on a new line to finish):[/]\n")
            
            try:
                module_info = ""
                while True:
                    line = input()
                    if line.strip() == "DONE":
                        break
                    module_info += line + "\n"
                
                if module_info.strip():
                    success, result = create_magisk_module(module_info)
                    if success:
                        console.print(f"\n[bold green]Module created successfully![/]")
                        console.print(f"[green]Path: {result}[/]")
                    else:
                        console.print(f"\n[bold red]Error creating module:[/]")
                        console.print(f"[red]{result}[/]")
                
                console.print("\n[green]Press Enter to return[/]")
                input()
                
            except KeyboardInterrupt:
                pass
                
        elif choice == '3':  # HELP
            show_help_guide()
            
        elif choice == 'a':
            auto_reconnect = not auto_reconnect
            status = "enabled" if auto_reconnect else "disabled"
            console.print(f"\n[yellow]Auto-reconnect {status}![/]")
            time.sleep(1)
            
        elif choice == 'q':
            shutdown_sequence()
            break
        elif choice == 'c':
            clear()

if __name__ == "__main__":
    import subprocess
    try:
        main()
    except KeyboardInterrupt:
        shutdown_sequence()
