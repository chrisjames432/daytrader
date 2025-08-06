#!/usr/bin/env python3
"""
Animal Rescue Day Trading Application v1.0
==========================================
AI-powered trading assistant to fund animal rescue operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import threading
import time
from PIL import Image, ImageTk
import pyttsx3

# Import existing modules
from make_chart import generate_bitx_chart
from ai_analyzer import analyze_image

class AnimalRescueTrader:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_tts()
        self.load_prompts()
        self.initialize_trading()  # Automatically start with first chart
        
    def initialize_trading(self):
        """Initialize the trading system with first chart"""
        # Add startup message
        self.add_to_feed("🚀 INITIALIZING TRADING SYSTEM...")
        self.add_to_feed("🐾 Loading first BITX analysis to start saving animals...")
        
        # Start first analysis in background thread
        def startup_analysis():
            time.sleep(1)  # Brief delay to let UI settle
            self.perform_single_analysis()
            
        threading.Thread(target=startup_analysis, daemon=True).start()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Animal Rescue Day Trading App v1.0 - Saving Lives Through Trading 🐾")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
    def setup_variables(self):
        """Initialize all tkinter variables"""
        self.auto_refresh = tk.BooleanVar(value=False)
        self.is_running = tk.BooleanVar(value=False)
        self.countdown_var = tk.StringVar(value="60")
        self.recommendation_var = tk.StringVar(value="WAIT")
        self.risk_level_var = tk.StringVar(value="MEDIUM")
        self.entry_price_var = tk.StringVar(value="--")
        self.stop_loss_var = tk.StringVar(value="--")
        self.take_profit_var = tk.StringVar(value="--")
        self.confidence_var = tk.StringVar(value="--")
        self.status_var = tk.StringVar(value="Ready to analyze BITX")
        
        # Initialize chart image storage
        self.chart_images = []
        
    def setup_ui(self):
        """Create the main user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.create_main_tab()
        self.create_system_prompt_tab()
        self.create_user_prompt_tab()
        self.create_debug_tab()
        
    def create_main_tab(self):
        """Create the main trading interface tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="🚀 Main Trading")
        
        # Top control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Start/Stop button
        self.start_button = tk.Button(
            control_frame, 
            text="🟢 START TRADING",
            command=self.toggle_trading,
            font=('Arial', 12, 'bold'),
            bg='green',
            fg='white',
            height=2,
            width=15
        )
        self.start_button.pack(side='left', padx=5)
        
        # Auto-refresh checkbox
        auto_check = tk.Checkbutton(
            control_frame,
            text="Auto-Refresh (1 min)",
            variable=self.auto_refresh,
            font=('Arial', 10)
        )
        auto_check.pack(side='left', padx=10)
        
        # Countdown timer
        countdown_label = tk.Label(
            control_frame,
            textvariable=self.countdown_var,
            font=('Arial', 14, 'bold'),
            bg='yellow',
            width=5
        )
        countdown_label.pack(side='left', padx=10)
        
        # Status
        status_label = tk.Label(
            control_frame,
            textvariable=self.status_var,
            font=('Arial', 10)
        )
        status_label.pack(side='right', padx=10)
        
        # Current stats panel (compact)
        stats_frame = ttk.LabelFrame(control_frame, text="Current Signal")
        stats_frame.pack(side='right', padx=10)
        
        # Compact stats display
        stats_row1 = tk.Frame(stats_frame)
        stats_row1.pack()
        
        tk.Label(stats_row1, text="Rec:", font=('Arial', 8)).pack(side='left')
        self.rec_mini = tk.Label(stats_row1, textvariable=self.recommendation_var, 
                                font=('Arial', 10, 'bold'), width=6)
        self.rec_mini.pack(side='left', padx=2)
        
        tk.Label(stats_row1, text="Risk:", font=('Arial', 8)).pack(side='left', padx=(10,0))
        self.risk_mini = tk.Label(stats_row1, textvariable=self.risk_level_var, 
                                 font=('Arial', 10, 'bold'), width=6)
        self.risk_mini.pack(side='left', padx=2)
        
        # Main scrollable trading feed
        feed_frame = ttk.LabelFrame(main_frame, text="🚀 Live Trading Feed - Every Analysis Helps Save Animals 🐾")
        feed_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollable text area for trading feed
        self.trading_feed = scrolledtext.ScrolledText(
            feed_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            height=30,
            bg='#001122',  # Dark blue background
            fg='#00ff00',  # Green text (terminal style)
            insertbackground='#00ff00'  # Green cursor
        )
        self.trading_feed.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add welcome message
        welcome_msg = """
🐾 ANIMAL RESCUE TRADING SYSTEM v1.0 🐾
=====================================
Mission: Generate consistent profits through AI-assisted BITX trading
Goal: Fund veterinary care, supplies, and rescue operations

Every BUY signal could mean another animal saved! 💙
Waiting for first analysis...

"""
        self.trading_feed.insert('1.0', welcome_msg)
        self.trading_feed.see(tk.END)
        
    def create_system_prompt_tab(self):
        """Create system prompt editing tab"""
        sys_frame = ttk.Frame(self.notebook)
        self.notebook.add(sys_frame, text="🤖 System Prompt")
        
        # Instructions
        instructions = tk.Label(
            sys_frame,
            text="Professional Day Trader AI System Prompt - Configure AI personality and expertise",
            font=('Arial', 12, 'bold')
        )
        instructions.pack(pady=10)
        
        # Text area for system prompt
        self.system_text = scrolledtext.ScrolledText(
            sys_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            height=25
        )
        self.system_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Save button
        save_sys_btn = tk.Button(
            sys_frame,
            text="💾 Save System Prompt",
            command=self.save_system_prompt,
            font=('Arial', 11, 'bold'),
            bg='blue',
            fg='white'
        )
        save_sys_btn.pack(pady=10)
        
    def create_user_prompt_tab(self):
        """Create user prompt editing tab"""
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="📊 User Prompt")
        
        # Instructions
        instructions = tk.Label(
            user_frame,
            text="Analysis Instructions - Configure what the AI should analyze in each chart",
            font=('Arial', 12, 'bold')
        )
        instructions.pack(pady=10)
        
        # Text area for user prompt
        self.user_text = scrolledtext.ScrolledText(
            user_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            height=25
        )
        self.user_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Save button
        save_user_btn = tk.Button(
            user_frame,
            text="💾 Save User Prompt",
            command=self.save_user_prompt,
            font=('Arial', 11, 'bold'),
            bg='blue',
            fg='white'
        )
        save_user_btn.pack(pady=10)
        
    def create_debug_tab(self):
        """Create debug output tab"""
        debug_frame = ttk.Frame(self.notebook)
        self.notebook.add(debug_frame, text="🔧 Debug")
        
        # Instructions
        instructions = tk.Label(
            debug_frame,
            text="Function Outputs & Error Logs - Monitor app performance and troubleshoot issues",
            font=('Arial', 12, 'bold')
        )
        instructions.pack(pady=5)
        
        # Debug output area
        self.debug_text = scrolledtext.ScrolledText(
            debug_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            height=30,
            bg='black',
            fg='green'
        )
        self.debug_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear debug button
        clear_btn = tk.Button(
            debug_frame,
            text="🗑️ Clear Debug Log",
            command=self.clear_debug,
            font=('Arial', 10)
        )
        clear_btn.pack(pady=5)
        
    def setup_tts(self):
        """Initialize text-to-speech for alerts"""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.log_debug("✅ Text-to-speech initialized successfully")
        except Exception as e:
            self.log_debug(f"❌ TTS initialization failed: {str(e)}")
            self.tts_engine = None
            
    def load_prompts(self):
        """Load default prompts into text areas"""
        # Default system prompt
        system_prompt = """You are a professional day trader with 20+ years of experience specializing in quick scalping trades. 

Your expertise includes:
- Identifying optimal entry/exit points for 0.10-0.50 cent moves
- EMA/SMA crossover strategies (5 EMA, 8 SMA)
- Daily pivot point analysis
- Risk assessment for short-term trades
- Stop loss and take profit targeting

Analyze the provided 1-minute BITX candlestick chart and provide:
1. RECOMMENDATION: "BUY" or "WAIT" 
2. RISK_LEVEL: "LOW", "MEDIUM", or "HIGH"
3. ENTRY_PRICE: Optimal entry point
4. STOP_LOSS: Maximum acceptable loss price
5. TAKE_PROFIT: Target profit-taking price
6. CONFIDENCE: Your confidence level (1-10)
7. REASONING: Brief explanation of your analysis

Focus on EMA5/SMA8 crossovers and daily pivot levels for scalping opportunities.
Remember: We're trading to save animal lives - precision and safety are paramount."""
        
        self.system_text.insert('1.0', system_prompt)
        
        # Default user prompt
        user_prompt = """Analyze this BITX 1-minute chart for day trading opportunities.

Current market conditions:
- Look for EMA5/SMA8 crossover signals
- Identify daily pivot point levels
- Assess volume and momentum
- Consider risk/reward ratio for quick scalp trades

Provide clear BUY or WAIT recommendation with specific entry, stop loss, and take profit prices.
Target profit: $0.10-$0.50 per share moves.

This analysis will help fund animal rescue operations - accuracy is critical for saving lives."""
        
        self.user_text.insert('1.0', user_prompt)
        
    def log_debug(self, message):
        """Add message to debug log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Display in UI
        self.debug_text.insert(tk.END, log_message)
        self.debug_text.see(tk.END)
        
        # Also write to debug.txt file
        try:
            with open('debug.txt', 'a', encoding='utf-8') as f:
                f.write(log_message)
        except Exception as e:
            # If we can't write to file, at least show in UI
            error_msg = f"[{timestamp}] ❌ Failed to write to debug.txt: {str(e)}\n"
            self.debug_text.insert(tk.END, error_msg)
        
    def clear_debug(self):
        """Clear the debug log"""
        self.debug_text.delete('1.0', tk.END)
        
        # Clear the debug file too
        try:
            with open('debug.txt', 'w', encoding='utf-8') as f:
                f.write("")  # Clear the file
            self.log_debug("Debug log and file cleared")
        except Exception as e:
            self.log_debug(f"❌ Failed to clear debug.txt: {str(e)}")
        
    def save_system_prompt(self):
        """Save system prompt to file"""
        try:
            with open('data/system_prompt.txt', 'w') as f:
                f.write(self.system_text.get('1.0', tk.END))
            self.log_debug("✅ System prompt saved successfully")
            messagebox.showinfo("Success", "System prompt saved!")
        except Exception as e:
            self.log_debug(f"❌ Failed to save system prompt: {str(e)}")
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            
    def save_user_prompt(self):
        """Save user prompt to file"""
        try:
            with open('data/user_prompt.txt', 'w') as f:
                f.write(self.user_text.get('1.0', tk.END))
            self.log_debug("✅ User prompt saved successfully")
            messagebox.showinfo("Success", "User prompt saved!")
        except Exception as e:
            self.log_debug(f"❌ Failed to save user prompt: {str(e)}")
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            
    def toggle_trading(self):
        """Start or stop the trading analysis"""
        if not self.is_running.get():
            # Start trading
            self.is_running.set(True)
            self.start_button.config(text="🔴 STOP TRADING", bg='red')
            self.log_debug("🚀 Trading analysis started - Ready to help save animals!")
            self.status_var.set("Analysis running...")
            
            # Start the analysis thread
            self.analysis_thread = threading.Thread(target=self.run_analysis_loop, daemon=True)
            self.analysis_thread.start()
            
        else:
            # Stop trading
            self.is_running.set(False)
            self.start_button.config(text="🟢 START TRADING", bg='green')
            self.log_debug("⏹️ Trading analysis stopped")
            self.status_var.set("Ready to analyze BITX")
            
    def run_analysis_loop(self):
        """Main analysis loop - runs in separate thread"""
        while self.is_running.get():
            try:
                if self.auto_refresh.get():
                    # Run full analysis
                    self.perform_analysis()
                    
                    # Countdown timer with feed updates
                    for i in range(60, 0, -1):
                        if not self.is_running.get():
                            break
                        self.countdown_var.set(str(i))
                        
                        # Update feed every 10 seconds with countdown
                        if i % 10 == 0 and i > 0:
                            self.root.after(0, lambda: self.add_to_feed(f"⏰ Next analysis in {i} seconds..."))
                        
                        time.sleep(1)
                else:
                    # Just update countdown without analysis
                    time.sleep(1)
                    
            except Exception as e:
                self.log_debug(f"❌ Error in analysis loop: {str(e)}")
                self.root.after(0, lambda: self.add_to_feed(f"❌ Analysis loop error: {str(e)}"))
                time.sleep(5)  # Wait before retrying
                
    def perform_single_analysis(self):
        """Perform a single analysis cycle (for startup or manual trigger)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Use thread-safe GUI updates
        self.root.after(0, lambda: self.add_to_feed(f"\n[{timestamp}] 🔄 STARTING BITX ANALYSIS CYCLE"))
        
        try:
            # Step 1: Generate BITX chart
            self.root.after(0, lambda: self.add_to_feed(f"[{timestamp}] 📊 Generating fresh candlestick chart..."))
            chart_data = generate_bitx_chart("BITX")
            
            # Use simple chart.png filename
            chart_path = "data/chart.png"
            
            # Step 2: Display chart in feed  
            self.root.after(0, lambda: self.display_chart_in_feed(chart_path))
            
            # Step 3: Run AI analysis
            self.root.after(0, lambda: self.add_to_feed(f"[{timestamp}] 🤖 Running AI analysis..."))
            
            def run_analysis():
                analysis_result = self.simulate_ai_analysis()
                # Update status after analysis
                self.root.after(0, lambda: self.status_var.set("Analysis complete"))
                
            # Run analysis in main thread using after
            self.root.after(100, run_analysis)
            
            self.log_debug("✅ Analysis cycle completed successfully")
            
        except Exception as e:
            error_msg = f"❌ Analysis error: {str(e)}"
            self.root.after(0, lambda: self.add_to_feed(f"[{timestamp}] {error_msg}"))
            self.log_debug(error_msg)
            
    def perform_analysis(self):
        """Perform complete chart generation and AI analysis"""
        # Delegate to single analysis method
        self.perform_single_analysis()
            
    def display_chart_in_feed(self, chart_path):
        """Add the generated chart to the trading feed with embedded image"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            # Convert to absolute path
            abs_chart_path = os.path.abspath(chart_path)
            
            # Check if chart file exists
            if not os.path.exists(abs_chart_path):
                self.add_to_feed(f"[{timestamp}] ❌ Chart generation failed - file not found")
                return
            
            # Get file size for verification
            file_size = os.path.getsize(abs_chart_path)
            
            # Add chart info to feed
            self.add_to_feed(f"\n[{timestamp}] 📊 NEW CHART GENERATED")
            self.add_to_feed(f"               Size: {file_size:,} bytes")
            self.add_to_feed(f"               Path: {chart_path}")
            
            # Load and resize image for embedding
            try:
                image = Image.open(abs_chart_path)
                
                # Resize to fit nicely in the text feed (smaller than before)
                max_width, max_height = 500, 300  # Smaller for text embedding
                ratio = min(max_width/image.width, max_height/image.height)
                new_width = int(image.width * ratio)
                new_height = int(image.height * ratio)
                
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Enable editing to insert image
                self.trading_feed.config(state='normal')
                
                # Insert the image directly into the text widget
                self.trading_feed.insert(tk.END, "\n               📈 LIVE CHART:\n")
                self.trading_feed.image_create(tk.END, image=photo)
                self.trading_feed.insert(tk.END, f"\n               Chart Size: {new_width}x{new_height}\n")
                
                # Store reference to prevent garbage collection
                if not hasattr(self, 'chart_images'):
                    self.chart_images = []
                self.chart_images.append(photo)
                
                # Keep only last 5 images to prevent memory issues
                if len(self.chart_images) > 5:
                    self.chart_images.pop(0)
                
                # Auto-scroll to show the new image
                self.trading_feed.see(tk.END)
                
                # Disable editing
                self.trading_feed.config(state='disabled')
                
                # Force update
                self.root.update_idletasks()
                
                self.add_to_feed(f"               🎯 Analyzing for trading opportunities...")
                
            except Exception as img_error:
                self.add_to_feed(f"               ❌ Image display error: {str(img_error)}")
                self.add_to_feed(f"               🎯 Continuing with analysis...")
                
        except Exception as e:
            self.add_to_feed(f"[{timestamp}] ❌ Chart display error: {str(e)}")
            
    def add_to_feed(self, message):
        """Add a message to the trading feed with auto-scroll"""
        # Enable editing
        self.trading_feed.config(state='normal')
        
        # Add the message
        self.trading_feed.insert(tk.END, message + "\n")
        
        # Auto-scroll to bottom
        self.trading_feed.see(tk.END)
        
        # Disable editing to prevent user changes
        self.trading_feed.config(state='disabled')
        
        # Force update
        self.root.update_idletasks()
            
    def simulate_ai_analysis(self):
        """Simulate AI analysis for testing (Phase 1)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # This is temporary - will be replaced with real AI in Phase 2
        import random
        
        recommendations = ["BUY", "WAIT", "STRONG BUY"]
        risk_levels = ["LOW", "MEDIUM", "HIGH"]
        entries = [24.45, 24.50, 24.55, 24.60, 24.65]
        
        rec = random.choice(recommendations)
        risk = random.choice(risk_levels)
        entry = random.choice(entries)
        
        # Update variables
        self.recommendation_var.set(rec)
        self.risk_level_var.set(risk)
        self.entry_price_var.set(f"${entry}")
        
        # Update colors for mini display
        if rec == "BUY" or rec == "STRONG BUY":
            self.rec_mini.config(bg='green', fg='white')
            # Play alert sound for BUY signals
            if self.tts_engine:
                threading.Thread(target=lambda: self.tts_engine.say("Trade opportunity detected"), daemon=True).start()
        else:
            self.rec_mini.config(bg='red', fg='white')
            
        # Update risk color
        risk_colors = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}
        self.risk_mini.config(bg=risk_colors.get(risk, "gray"), fg='black' if risk == 'MEDIUM' else 'white')
        
        # Add analysis results to feed
        self.add_to_feed(f"\n[{timestamp}] 🤖 AI ANALYSIS COMPLETE")
        self.add_to_feed(f"               🎯 SIGNAL: {rec}")
        self.add_to_feed(f"               ⚡ RISK: {risk}")
        self.add_to_feed(f"               💰 ENTRY: ${entry}")
        
        if rec == "BUY" or rec == "STRONG BUY":
            self.add_to_feed(f"               🚀 OPPORTUNITY DETECTED! Another chance to help animals! 🐾")
        else:
            self.add_to_feed(f"               ⏳ Waiting for better setup...")
            
        # Log for debug
        self.log_debug(f"🎯 Analysis: {rec} | Risk: {risk} | Entry: ${entry}")
        
        return {
            'recommendation': rec,
            'risk_level': risk, 
            'entry_price': f'${entry}',
            'confidence': random.randint(65, 95)
        }
        
        # Simulate prices
        base_price = 24.50
        self.entry_price_var.set(f"${base_price:.2f}")
        self.stop_loss_var.set(f"${base_price - 0.10:.2f}")
        self.take_profit_var.set(f"${base_price + 0.25:.2f}")
        self.confidence_var.set(f"{random.randint(6, 9)}/10")
        
        self.log_debug(f"🎯 Analysis: {rec} | Risk: {risk} | Entry: ${base_price:.2f}")

def main():
    """Main application entry point"""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Initialize debug file
    try:
        with open('debug.txt', 'a', encoding='utf-8') as f:
            startup_msg = f"\n{'='*50}\n🐾 Animal Rescue Trading App Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}\n"
            f.write(startup_msg)
    except Exception as e:
        print(f"Warning: Could not initialize debug.txt: {e}")
    
    # Create and run the application
    root = tk.Tk()
    app = AnimalRescueTrader(root)
    
    print("🐾 Animal Rescue Day Trading App v1.0")
    print("🚀 Starting application...")
    print("💙 Every trade helps save more animals!")
    print("📝 Debug output will be saved to debug.txt")
    
    root.mainloop()

if __name__ == "__main__":
    main()
