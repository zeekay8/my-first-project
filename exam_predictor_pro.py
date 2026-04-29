import pandas as pd
import numpy as np
import random
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ModernExamPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Exam Predictor Pro")
        self.root.geometry("1200x700")
        
        # Set modern color scheme
        self.bg_color = '#f8f9fa'
        self.primary_color = '#4361ee'
        self.secondary_color = '#3f37c9'
        self.success_color = '#4cc9f0'
        self.warning_color = '#f72585'
        self.card_bg = '#ffffff'
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize data
        self.all_topics = [
            "Algebra", "Calculus", "Geometry", "Trigonometry", 
            "Statistics", "Probability", "Linear Algebra", "Vectors",
            "Mechanics", "Thermodynamics", "Electromagnetism", "Optics", 
            "Quantum Physics", "Waves", "Nuclear Physics",
            "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
            "Chemical Bonding", "Periodic Table", "Chemical Kinetics", "Electrochemistry",
            "Data Structures", "Algorithms", "Programming Fundamentals",
            "OOP", "Database", "Networks", "OS", "Web Dev"
        ]
        
        self.repeated_topics = [
            "Algebra", "Calculus", "Mechanics", "Organic Chemistry",
            "Data Structures", "Statistics", "Algorithms", "Probability"
        ]
        
        self.years = [2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019]
        self.dataset = None
        self.create_modern_ui()
        
    def create_modern_ui(self):
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill='x')
        
        title_label = tk.Label(header_frame, 
                               text="🤖 AI EXAM PREDICTOR PRO",
                               font=('Segoe UI', 24, 'bold'),
                               bg=self.primary_color, fg='white')
        title_label.pack(pady=20)
        
        subtitle = tk.Label(header_frame,
                           text="Predict next year's exam topics using machine learning",
                           font=('Segoe UI', 10),
                           bg=self.primary_color, fg='#e0e0e0')
        subtitle.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg=self.card_bg, relief='flat', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Control buttons with modern styling
        control_title = tk.Label(left_panel, text="CONTROLS",
                                font=('Segoe UI', 14, 'bold'),
                                bg=self.card_bg, fg=self.primary_color)
        control_title.pack(pady=(20, 10), padx=20)
        
        # Button frame
        btn_frame = tk.Frame(left_panel, bg=self.card_bg)
        btn_frame.pack(pady=10, padx=20)
        
        self.create_btn = self.create_modern_button(btn_frame, "📊 1. GENERATE DATA", 
                                                    self.create_dataset, self.primary_color)
        self.create_btn.pack(fill='x', pady=5)
        
        self.save_btn = self.create_modern_button(btn_frame, "💾 2. EXPORT CSV", 
                                                  self.save_csv, self.secondary_color, state='disabled')
        self.save_btn.pack(fill='x', pady=5)
        
        self.analyze_btn = self.create_modern_button(btn_frame, "📈 3. ANALYZE DATA", 
                                                     self.analyze_data, self.success_color, state='disabled')
        self.analyze_btn.pack(fill='x', pady=5)
        
        self.predict_btn = self.create_modern_button(btn_frame, "🔮 4. PREDICT 2020", 
                                                     self.predict_topics, self.warning_color, state='disabled')
        self.predict_btn.pack(fill='x', pady=5)
        
        self.clear_btn = self.create_modern_button(btn_frame, "🗑️ CLEAR", 
                                                   self.clear_output, '#6c757d')
        self.clear_btn.pack(fill='x', pady=(20, 5))
        
        # Stats panel
        stats_frame = tk.Frame(left_panel, bg=self.card_bg)
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        self.stats_label = tk.Label(stats_frame, text="STATISTICS",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=self.card_bg, fg=self.secondary_color)
        self.stats_label.pack(anchor='w')
        
        self.stats_text = tk.Text(stats_frame, height=8, width=25,
                                  font=('Consolas', 9),
                                  bg='#f1f3f5', fg='#212529',
                                  relief='flat', bd=0)
        self.stats_text.pack(pady=10, fill='x')
        self.stats_text.insert('1.0', "No data yet.\nClick GENERATE DATA to start.")
        self.stats_text.config(state='disabled')
        
        # Right panel - Main content
        right_panel = tk.Frame(main_container, bg=self.card_bg)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', 
                       background='#e9ecef',
                       foreground='#495057',
                       padding=[15, 5],
                       font=('Segoe UI', 10))
        style.map('TNotebook.Tab',
                 background=[('selected', self.primary_color)],
                 foreground=[('selected', 'white')])
        
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Output Tab
        self.output_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.output_frame, text="📋 RESULTS")
        
        # Output text with modern styling
        self.output_text = tk.Text(self.output_frame,
                                   wrap=tk.WORD,
                                   font=('Consolas', 11),
                                   bg='white',
                                   fg='#212529',
                                   relief='flat',
                                   bd=1,
                                   padx=10,
                                   pady=10)
        self.output_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configure tags for colored text
        self.output_text.tag_configure('success', foreground='#4cc9f0', font=('Consolas', 11, 'bold'))
        self.output_text.tag_configure('warning', foreground='#f72585', font=('Consolas', 11, 'bold'))
        self.output_text.tag_configure('info', foreground='#4361ee', font=('Consolas', 11, 'bold'))
        
        # Data Preview Tab
        self.preview_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.preview_frame, text="📊 DATA PREVIEW")
        
        # Treeview for data with modern styling
        style = ttk.Style()
        style.configure("Treeview",
                       background="white",
                       foreground="#212529",
                       rowheight=25,
                       fieldbackground="white",
                       font=('Segoe UI', 10))
        style.configure("Treeview.Heading",
                       background=self.primary_color,
                       foreground="white",
                       relief="flat",
                       font=('Segoe UI', 10, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', self.secondary_color)])
        
        self.tree = ttk.Treeview(self.preview_frame, style="Treeview", height=15)
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.preview_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, 
                                   text="✅ Ready to start",
                                   bg='#e9ecef',
                                   fg='#495057',
                                   font=('Segoe UI', 10),
                                   anchor='w',
                                   padx=20)
        self.status_bar.pack(fill='x', side='bottom')
        
    def create_modern_button(self, parent, text, command, color, state='normal'):
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=color,
                       fg='white',
                       font=('Segoe UI', 11, 'bold'),
                       padx=15,
                       pady=10,
                       relief='flat',
                       bd=0,
                       cursor='hand2',
                       state=state)
        
        # Hover effects
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn['bg'] = self.darken_color(color)
        
        def on_leave(e):
            if btn['state'] != 'disabled':
                btn['bg'] = color
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def darken_color(self, color):
        # Simple color darkening
        if color == self.primary_color:
            return self.secondary_color
        elif color == self.secondary_color:
            return '#2b2b6e'
        elif color == self.success_color:
 return '#3aa8c4'
        elif color == self.warning_color:
            return '#c91b6b'
        return '#5a6268'
    
    def create_dataset(self):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('end', "📚 GENERATING DATASET...\n", 'info')
        self.output_text.insert('end', "═"*50 + "\n")
        self.root.update()
        
        data = []
        for year in self.years:
            num_topics = random.randint(10, 12)
            year_topics = []
            
            num_repeated = random.randint(4, 6)
            repeated_selected = random.sample(self.repeated_topics, 
                                            min(num_repeated, len(self.repeated_topics)))
            year_topics.extend(repeated_selected)
            
            remaining = num_topics - len(year_topics)
            if remaining > 0:
                other_topics = [t for t in self.all_topics if t not in year_topics]
                sample_size = min(remaining, len(other_topics))
                if sample_size > 0:
                    random_topics = random.sample(other_topics, sample_size)
                    year_topics.extend(random_topics)
            
            for topic in year_topics:
                data.append({'Year': year, 'Topic': topic})
        
        self.dataset = pd.DataFrame(data)
        
        self.output_text.insert('end', f"✅ Dataset generated successfully!\n", 'success')
        self.output_text.insert('end', f"📊 Total entries: {len(self.dataset)}\n")
        self.output_text.insert('end', f"📅 Years: {self.years[0]} to {self.years[-1]}\n")
        self.output_text.insert('end', f"📚 Unique topics: {self.dataset['Topic'].nunique()}\n\n")
        
        # Update stats
        self.update_stats()
        
        # Enable buttons
        self.save_btn.config(state='normal')
        self.analyze_btn.config(state='normal')
        self.predict_btn.config(state='normal')
        
        self.status_bar.config(text="✅ Dataset ready")
        self.update_preview()
    
    def update_stats(self):
        if self.dataset is not None:
            self.stats_text.config(state='normal')
            self.stats_text.delete('1.0', tk.END)
            
            freq = self.dataset['Topic'].value_counts()
            top_topics = freq.head(5)
            
            stats = "📈 TOP 5 TOPICS:\n"
            stats += "─"*20 + "\n"
            for topic, count in top_topics.items():
                stats += f"{topic[:15]:15} : {count} times\n"
            
            stats += f"\n📊 TOTAL: {len(self.dataset)} records"
            stats += f"\n📚 UNIQUE: {self.dataset['Topic'].nunique()} topics"
            stats += f"\n📅 YEARS: 10 years"
            
            self.stats_text.insert('1.0', stats)
            self.stats_text.config(state='disabled')
    
    def update_preview(self):
        if self.dataset is not None:
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            self.tree['columns'] = ('Year', 'Topic')
            self.tree.column('#0', width=0, stretch=False)
            self.tree.column('Year', width=100, anchor='center')
            self.tree.column('Topic', width=400, anchor='w')
            
            self.tree.heading('Year', text='Year')
            self.tree.heading('Topic', text='Topic')
            
            for _, row in self.dataset.head(20).iterrows():
                self.tree.insert('', 'end', values=(row['Year'], row['Topic']))
    
    def save_csv(self):
        if self.dataset is not None:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="exam_predictions.csv"
            )
            
            if filename:
                self.dataset.to_csv(filename, index=False)
                self.output_text.insert('end', f"✅ File saved to:\n   {filename}\n\n", 'success')
                self.status_bar.config(text=f"✅ Saved to {os.path.basename(filename)}")
    
    def analyze_data(self):
        if self.dataset is None:
            return
        
        self.output_text.insert('end', "\n" + "═"*50 + "\n", 'info')
        self.output_text.insert('end', "📊 DATA ANALYSIS\n", 'info')
        self.output_text.insert('end', "═"*50 + "\n")
        
        freq = self.dataset['Topic'].value_counts()
        meets_requirement = 0
        
        self.output_text.insert('end', "\n📈 TOPIC FREQUENCY:\n")
        self.output_text.insert('end', "─"*40 + "\n")
        
        for topic, count in freq.head(15).items():
            mark = "✓" if 3 <= count <= 4 else " "
            if 3 <= count <= 4:
                meets_requirement += 1
            self.output_text.insert('end', f"  {topic:25} : {count:2} times {mark}\n")
        
        self.output_text.insert('end', f"\n✅ Topics appearing 3-4 times: {meets_requirement}\n")
        self.output_text.insert('end', "─"*40 + "\n")
        self.status_bar.config(text="✅ Analysis complete")
    
    def predict_topics(self):
        if self.dataset is None:
            return
        
        self.output_text.insert('end', "\n" + "═"*50 + "\n", 'warning')
        self.output_text.insert('end', "🔮 PREDICTIONS FOR 2020\n", 'warning')
        self.output_text.insert('end', "═"*50 + "\n")
        
        topic_counts = self.dataset['Topic'].value_counts()
        predictions = topic_counts.head(10).index.tolist()
        
        self.output_text.insert('end', "\n📋 TOP 10 PREDICTED TOPICS:\n")
        self.output_text.insert('end', "─"*40 + "\n")
        
        for i, topic in enumerate(predictions, 1):
            frequency = topic_counts[topic]
            confidence = "★" * min(frequency, 5) + "☆" * (5 - min(frequency, 5))
            self.output_text.insert('end', f"{i:2}. {topic:25} [{confidence}] {frequency} times\n")
        
        self.output_text.insert('end', "\n✅ Based on 10 years of historical data\n")
        self.output_text.insert('end', "📊 Higher frequency = higher probability\n")
        self.status_bar.config(text="✅ Predictions generated")
    
    def clear_output(self):
        self.output_text.delete('1.0', tk.END)
        self.status_bar.config(text="✅ Output cleared")




if __name__ == "__main__":
    root = tk.Tk()
    app = ModernExamPredictor(root)
    root.mainloop()