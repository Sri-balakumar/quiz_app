import tkinter as tk
import random  
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from quiz_data import quiz_data
from database import QuizDatabase
import hashlib
from PIL import ImageGrab  # Add this import at the top
import os
from datetime import datetime

class QuizApp:
    def __init__(self, root, quiz_data):
        self.root = root
        self.root.title("✨ Amazing Quiz App ✨")
        self.original_quiz_data = quiz_data.copy()
        self.quiz_data = self.shuffle_questions(quiz_data.copy())
        self.quiz_data = quiz_data
        self.current_question = 0
        self.score = 0
        self.unanswered_questions = []
        self.answered_questions = set()
        self.retry_mode = False
        self.is_retry = False
        self.user_name = ""
        self.timer = None
        self.time_left = 15
        self.question_times = {}
        self.logged_username = ""
        if self.timer:
            self.root.after_cancel(self.timer)
        
            self.db.save_score(self.user_name, self.score, len(self.quiz_data))
        
        # Initialize database
        self.db = QuizDatabase()
        
        # Use a modern, dark theme with accent colors
        self.style = Style(theme="darkly")
        self.root.geometry("1700x900")

        # Custom button styles with modern colors
        self.style.configure("success.TButton", 
                           foreground="white",
                           background="#2ecc71")  # Fresh green
        self.style.configure("danger.TButton", 
                           foreground="white",
                           background="#e74c3c")  # Soft red
        self.style.configure("primary.TButton", 
                           foreground="white",
                           background="#3498db")  # Sky blue
        self.style.configure("warning.TButton", 
                           foreground="white",
                           background="#f1c40f")  # Warm yellow
        
        # Custom label styles
        self.style.configure("timer.TLabel",
                           foreground="#e74c3c",  # Red for timer
                           font=("Helvetica", 16, "bold"))
        
        self.style.configure("score.TLabel",
                           foreground="#2ecc71",  # Green for score
                           font=("Helvetica", 12, "bold"))
        
        # Custom progress bar style
        self.style.configure("custom.Horizontal.TProgressbar",
                           troughcolor="#2c3e50",  # Dark background
                           background="#3498db",   # Blue progress
                           bordercolor="#34495e")  # Dark border

        self.show_login_page()

    def shuffle_questions(self, quiz_data):
        random.shuffle(quiz_data)
        return quiz_data

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_page(self):
        self.login_container = ttk.Frame(self.root, padding=40)
        self.login_container.pack(expand=True, fill="both")

        # Welcome Label
        welcome_label = ttk.Label(
            self.login_container,
            text="🎯 Quiz App Login 🎯",
            font=("Helvetica", 24, "bold"),
            anchor="center"
        )
        welcome_label.pack(pady=(0, 20))

        # Login Frame
        login_frame = ttk.LabelFrame(self.login_container, text="Login", padding=15)
        login_frame.pack(fill="x", pady=20)

        # Username
        username_label = ttk.Label(
            login_frame,
            text="Username:",
            font=("Helvetica", 12)
        )
        username_label.pack(pady=(0, 5))

        self.username_entry = ttk.Entry(
            login_frame,
            font=("Helvetica", 12),
            width=30
        )
        self.username_entry.pack(pady=(0, 10))

        # Password
        password_label = ttk.Label(
            login_frame,
            text="Password:",
            font=("Helvetica", 12)
        )
        password_label.pack(pady=(0, 5))

        self.password_entry = ttk.Entry(
            login_frame,
            font=("Helvetica", 12),
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=(0, 20))

        # Buttons Frame
        buttons_frame = ttk.Frame(login_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))

        login_btn = ttk.Button(
            buttons_frame,
            text="Login",
            command=self.login,
            style="success.TButton",
            width=15
        )
        login_btn.pack(side="left", padx=5, expand=True)

        signup_btn = ttk.Button(
            buttons_frame,
            text="Sign Up",
            command=self.show_signup_page,
            style="primary.TButton",
            width=15
        )
        signup_btn.pack(side="left", padx=5, expand=True)

     # Password Security Rules
        rules_frame = ttk.LabelFrame(self.login_container, text="Password Security Rules", padding=15)
        rules_frame.pack(fill="x", pady=10)

        rules_text = (
            "FOR YOUR SECURITY REASON (PASSWORD)"
            "\n""\n"
            "1. Minimum 6 characters long.\n"
            "2. Must contain at least one uppercase letter.\n"
            "3. Must contain at least one lowercase letter.\n"
            "4. Must contain at least one number.\n"
            "5. Must contain at least one special character (e.g., !@#$%^&*).\n"
        )

        rules_label = ttk.Label(
            rules_frame,
            text=rules_text,
            font=("Helvetica", 12),
            justify="left",
            wraplength=600
        )
        rules_label.pack(pady=10)

        # GitHub Link Frame
        github_frame = ttk.Frame(self.login_container)
        github_frame.pack(fill="x", pady=10)

        github_label = ttk.Label(
            github_frame,
            text="🔗 Visit my GitHub repository:",
            font=("Helvetica", 10),
            foreground="#3498db"
        )
        github_label.pack(pady=(5, 0))

        github_link = ttk.Label(
            github_frame,
            text="Sri Balakumar",
            font=("Helvetica", 10, "underline"),
            foreground="#3498db",
            cursor="hand2"
        )
        github_link.pack()

        # Bind click event to open the link
        github_link.bind("<Button-1>", lambda e: self.open_github_link())

    def open_github_link(self):
        import webbrowser
        webbrowser.open("https://github.com/Sri-balakumar")

    def show_signup_page(self):
        # Clear login page
        self.login_container.destroy()

        self.signup_container = ttk.Frame(self.root, padding=40)
        self.signup_container.pack(expand=True, fill="both")

        # Sign Up Label
        signup_label = ttk.Label(
            self.signup_container,
            text="📝 Create Account 📝",
            font=("Helvetica", 24, "bold"),
            anchor="center"
        )
        signup_label.pack(pady=(0, 20))

        # Sign Up Frame
        signup_frame = ttk.LabelFrame(self.signup_container, text="Sign Up", padding=15)
        signup_frame.pack(fill="x", pady=20)

        # Username
        username_label = ttk.Label(
            signup_frame,
            text="Username:",
            font=("Helvetica", 12)
        )
        username_label.pack(pady=(0, 5))

        self.new_username_entry = ttk.Entry(
            signup_frame,
            font=("Helvetica", 12),
            width=30
        )
        self.new_username_entry.pack(pady=(0, 10))

        # Password
        password_label = ttk.Label(
            signup_frame,
            text="Password:",
            font=("Helvetica", 12)
        )
        password_label.pack(pady=(0, 5))

        self.new_password_entry = ttk.Entry(
            signup_frame,
            font=("Helvetica", 12),
            width=30,
            show="*"
        )
        self.new_password_entry.pack(pady=(0, 10))

        # Confirm Password
        confirm_password_label = ttk.Label(
            signup_frame,
            text="Confirm Password:",
            font=("Helvetica", 12)
        )
        confirm_password_label.pack(pady=(0, 5))

        self.confirm_password_entry = ttk.Entry(
            signup_frame,
            font=("Helvetica", 12),
            width=30,
            show="*"
        )
        self.confirm_password_entry.pack(pady=(0, 20))

        # Buttons Frame
        buttons_frame = ttk.Frame(signup_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))

        create_account_btn = ttk.Button(
            buttons_frame,
            text="Create Account",
            command=self.create_account,
            style="success.TButton",
            width=15
        )
        create_account_btn.pack(side="left", padx=5, expand=True)

        back_btn = ttk.Button(
            buttons_frame,
            text="Back to Login",
            command=self.back_to_login,
            style="primary.TButton",
            width=15
        )
        back_btn.pack(side="left", padx=5, expand=True)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
    
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        hashed_password = self.hash_password(password)
        if self.db.verify_user(username, hashed_password):
            self.user_name = username
            # Show success message with username
            messagebox.showinfo("Success", f"Successfully logged in as {username}! 🎉")
            # Clear leaderboard when logging in
            self.db.clear_leaderboard()
            self.login_container.destroy()
            self.show_name_entry()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_account(self):
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
            
        hashed_password = self.hash_password(password)
        if self.db.create_user(username, hashed_password):
            self.user_name = username
            # Shuffle questions on successful login
            self.quiz_data = self.shuffle_questions(self.original_quiz_data.copy())
            # Clear leaderboard when creating new account
            self.db.clear_leaderboard()
            messagebox.showinfo("Success", "Account created successfully!")
            self.back_to_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    def back_to_login(self):
        self.signup_container.destroy()
        self.show_login_page()

    # ... (rest of the existing QuizApp code remains the same)

    def show_name_entry(self):
        self.name_container = ttk.Frame(self.root, padding=40)
        self.name_container.pack(expand=True, fill="both")

        # Welcome Label
        welcome_label = ttk.Label(
            self.name_container,
            text="👋 Welcome to the Quiz! 👋",
            font=("Helvetica", 24, "bold"),
            anchor="center"
        )
        welcome_label.pack(pady=(0, 20))

        # Rules Frame
        rules_frame = ttk.LabelFrame(self.name_container, text="Rules & Regulations", padding=15)
        rules_frame.pack(fill="x", pady=20)

        rules_text = (
            "1. You will have 15 seconds to answer each question.\n"
            "2. You can skip any question, but you will lose time.\n"
            "3. Each correct answer earns you 1 point.\n"
            "4. You can retry unanswered questions after the first round.\n"
            "5. At the end, your performance will be evaluated.\n"
            "6. Have fun and do your best!"
        )

        rules_label = ttk.Label(
            rules_frame,
            text=rules_text,
            font=("Helvetica", 12),
            justify="left",
            wraplength=600
        )
        rules_label.pack(pady=10)

        # Name Entry Frame
        entry_frame = ttk.Frame(self.name_container)
        entry_frame.pack(pady=20)

        name_label = ttk.Label(
            entry_frame,
            text="Please enter your name:",
            font=("Helvetica", 14)
        )
        name_label.pack(pady=(0, 10))

        self.name_entry = ttk.Entry(
            entry_frame,
            font=("Helvetica", 12),
            width=30
        )
        self.name_entry.pack(pady=10)

        start_btn = ttk.Button(
            entry_frame,
            text="Start Quiz ▶️",
            command=self.start_quiz,
            style="success.TButton",
            width=20
        )
        start_btn.pack(pady=20)

        self.name_entry.bind('<Return>', lambda e: self.start_quiz())
        self.name_entry.focus()

    def start_quiz(self):
        name = self.name_entry.get().strip()
        if not name:
            return

        self.user_name = name
        self.quiz_data = self.shuffle_questions(self.original_quiz_data.copy())
        
        for widget in self.root.winfo_children():
            widget.destroy()

        self.initialize_quiz_interface()
        self.show_question()

    def initialize_quiz_interface(self):
        self.main_container = ttk.Frame(self.root, padding=20)
        self.main_container.pack(fill="both", expand=True)

        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.title_label = ttk.Label(
            self.header_frame,
            text=f"🌟 Good luck, {self.user_name}! 🌟",
            font=("Helvetica", 24, "bold"),
            anchor="center"
        )
        self.title_label.pack()

        # Add timer label
        self.timer_label = ttk.Label(
            self.header_frame,
            text="Time left: 15s",
            font=("Helvetica", 16),
            foreground="white"
        )
        self.timer_label.pack(pady=5)

        self.question_frame = ttk.Frame(self.main_container, padding=20)
        self.question_frame.pack(fill="x", pady=10)

        self.choice_frame = ttk.Frame(self.main_container, padding=20)
        self.choice_frame.pack(fill="x", pady=10)

        self.feedback_frame = ttk.Frame(self.main_container, padding=10)
        self.feedback_frame.pack(fill="x", pady=10)

        self.control_frame = ttk.Frame(self.main_container, padding=5)
        self.control_frame.pack(fill="x", pady=5)

        self.progress_label = ttk.Label(
            self.control_frame,
            text="Progress:",
            font=("Helvetica", 12)
        )
        self.progress_label.grid(row=0, column=0, padx=5, pady=2, columnspan=3)
        
        self.progress = ttk.Progressbar(
            self.control_frame,
            orient="horizontal",
            length=600,
            mode="determinate"
        )
        self.progress.grid(row=1, column=0, columnspan=3, pady=5)
        self.progress["maximum"] = len(self.quiz_data)

        self.qs_label = ttk.Label(
            self.question_frame,
            text="",
            anchor="center",
            wraplength=700,
            font=("Helvetica", 18),
            justify="center"
        )
        self.qs_label.pack(pady=20)

        self.choice_btns = []
        for i in range(4):
            btn = ttk.Button(
                self.choice_frame,
                text="",
                command=lambda x=i: self.check_answer(x),
                style="success.TButton",
                width=40
            )
            btn.pack(pady=8)
            self.choice_btns.append(btn)

        button_frame = ttk.Frame(self.control_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=2)

        self.next_btn = ttk.Button(
            button_frame,
            text="Next ➡️",
            command=self.next_question,
            state="disabled",
            style="primary.TButton",
            width=15
        )
        self.next_btn.pack(side="left", padx=5)

        self.skip_btn = ttk.Button(
            button_frame,
            text="Skip ⏭️",
            command=self.skip_question,
            style="warning.TButton",
            width=15
        )
        self.skip_btn.pack(side="left", padx=5)

        self.exit_btn = ttk.Button(
            button_frame,
            text="👋 Exit",
            command=self.root.destroy,
            style="danger.TButton",
            width=15
        )
        self.exit_btn.pack(side="left", padx=5)

        self.score_label = ttk.Label(
            self.control_frame,
            text=f"Score: {self.score}/{len(self.quiz_data)}",
            font=("Helvetica", 12, "bold")
        )
        self.score_label.grid(row=3, column=0, columnspan=3, pady=5)

        for i in range(3):
            self.control_frame.grid_columnconfigure(i, weight=1)

    def start_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        
        # Get stored time for skipped questions, otherwise start at 15 seconds
        self.time_left = self.question_times.get(self.current_question, 15)
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        
        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.root.after(1000, self.update_timer)
        else:
            self.time_out()

    def time_out(self):
        if self.current_question not in self.answered_questions:
            # Mark all buttons as wrong and highlight the correct answer
            question = self.quiz_data[self.current_question]
            for i, btn in enumerate(self.choice_btns):
                if btn.cget("text") == question["answer"]:
                    btn.configure(style="success.TButton", text=f"✔️ {btn.cget('text')}")
                else:
                    btn.configure(style="danger.TButton", text=f"❌ {btn.cget('text')}")
                btn.config(state="disabled")
            
            self.answered_questions.add(self.current_question)
            self.next_btn.config(state="normal")
            
        self.root.after(1000, self.next_question)

    def show_question(self):
        if self.retry_mode:
            self.unanswered_questions = [q for q in self.unanswered_questions 
                                       if q not in self.answered_questions]
            
            if not self.unanswered_questions:
                self.show_final_score()
                return
                
            question_index = self.unanswered_questions[0]
        else:
            question_index = self.current_question
        
        self.current_question = question_index
        question = self.quiz_data[question_index]
        self.qs_label.config(text=f"Question {question_index + 1}: {question['question']}")

        shuffled_choices = question["choices"][:]
        random.shuffle(shuffled_choices)

        for i, choice in enumerate(shuffled_choices):
            self.choice_btns[i].config(
                text=choice,
                state="normal", 
                style="success.TButton"
            )

        self.next_btn.config(state="disabled")
        
        self.progress["value"] = len(self.answered_questions)
        self.score_label.config(text=f"Score: {self.score}/{len(self.quiz_data)}")
        
        progress_percent = (len(self.answered_questions) / len(self.quiz_data)) * 100
        self.progress_label.config(text=f"Progress: {progress_percent:.0f}%")

        # Start the timer for the question
        self.start_timer()

    def check_answer(self, choice):
        # Cancel the timer when an answer is selected
        if self.timer:
            self.root.after_cancel(self.timer)

        question = self.quiz_data[self.current_question]
        selected_choice = self.choice_btns[choice].cget("text")

        for i, btn in enumerate(self.choice_btns):
            if i == choice:
                if selected_choice == question["answer"]:
                    btn.configure(style="success.TButton", text=f"✔️ {selected_choice}")
                else:
                    btn.configure(style="danger.TButton", text=f"❌ {selected_choice}")
            else:
                if self.choice_btns[i].cget("text") == question["answer"]:
                    btn.configure(style="success.TButton", text=f"✔️ {btn.cget('text')}")
                else:
                    btn.configure(style="danger.TButton", text=f"❌ {btn.cget('text')}")
            btn.config(state="disabled")

        if selected_choice == question["answer"]:
            self.score += 1

        self.answered_questions.add(self.current_question)
        self.next_btn.config(state="normal")
        self.score_label.config(text=f"Score: {self.score}/{len(self.quiz_data)}")

    def skip_question(self):
        # Store remaining time for the skipped question
        self.question_times[self.current_question] = self.time_left
        
        if self.timer:
            self.root.after_cancel(self.timer)
        
        if self.current_question not in self.answered_questions:
            if self.current_question not in self.unanswered_questions:
                self.unanswered_questions.append(self.current_question)
        self.next_question()

    def next_question(self):
        if self.timer:
            self.root.after_cancel(self.timer)

        if self.retry_mode:
            if self.unanswered_questions:
                self.unanswered_questions.pop(0)
            self.show_question()
        else:
            self.current_question += 1
            if self.current_question < len(self.quiz_data):
                self.show_question()
            else:
                self.unanswered_questions = [q for q in self.unanswered_questions 
                                           if q not in self.answered_questions]
                if self.unanswered_questions:
                    self.retry_mode = True
                    self.show_question()
                else:
                    self.show_final_score()

    def clear_leaderboard(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the leaderboard? This action cannot be undone."):
            self.db.clear_leaderboard()
            messagebox.showinfo("Success", "Leaderboard has been cleared!")
            self.show_final_score()  # Refresh the final score screen

    def capture_screenshot(self, frame):
        # Create screenshots directory if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/quiz_score_{self.user_name}_{timestamp}.png"
        
        # Get frame coordinates
        x = frame.winfo_rootx()
        y = frame.winfo_rooty()
        width = frame.winfo_width()
        height = frame.winfo_height()
        
        # Capture the screenshot
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
            screenshot.save(filename)
            messagebox.showinfo("Success", f"Screenshot saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot:\n{str(e)}")

    def show_final_score(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            
        self.db.save_score(self.user_name, self.score, len(self.quiz_data))
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        final_frame = ttk.Frame(self.root, padding=40)
        final_frame.pack(expand=True, fill="both")

        score_percentage = (self.score / len(self.quiz_data)) * 100
        if score_percentage >= 80:
            emoji = "🏆"
            message = "Excellent work"
        elif score_percentage >= 60:
            emoji = "🌟"
            message = "Good job"
        else:
            emoji = "💪"
            message = "Nice try"

    # Score display
        final_label = ttk.Label(
            final_frame,
            text=f"{emoji} Quiz Completed! {emoji}\n\n{message}, {self.user_name}!\n\nFinal Score: {self.score}/{len(self.quiz_data)}\n({score_percentage:.1f}%)",
            font=("Helvetica", 20, "bold"),
            anchor="center",
            justify="center"
        )
        final_label.pack(pady=20)

        # Leaderboard
        leaderboard_frame = ttk.LabelFrame(final_frame, text="🏆 Leaderboard 🏆", padding=15)
        leaderboard_frame.pack(fill="x", pady=20)

        columns = ('Rank', 'Name', 'Score', 'Percentage', 'Date')
        tree = ttk.Treeview(leaderboard_frame, columns=columns, show='headings', height=5)
    
        for col, width in zip(columns, [50, 100, 50, 80, 180]):
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Set column headings
            tree.heading('Rank', text='Rank')
            tree.heading('Name', text='Name')
            tree.heading('Score', text='Score')
            tree.heading('Percentage', text='Percentage')
            tree.heading('Date', text='Date/time')
        
            # Set column widths
            tree.column('Rank', width=50)
            tree.column('Name', width=100)
            tree.column('Score', width=50)
            tree.column('Percentage', width=80)
            tree.column('Date', width=180)

        # Get and insert top scores
        top_scores = self.db.get_top_scores()
        for i, score in enumerate(top_scores, 1):
            name, score_val, total, percentage, date = score
            # Handle date formatting - check if date is string or datetime
            date_str = date if isinstance(date, str) else date.strftime("%Y-%m-%d %H:%M")
            tree.insert('', 'end', values=(
                f"#{i}",
                name,
                f"{score_val}/{total}",
                f"{percentage:.1f}%",
                date_str
            ))

        tree.pack(pady=10)

    # Player history
        history_frame = ttk.LabelFrame(final_frame, text=f"📊 {self.user_name}'s History 📊", padding=15)
        history_frame.pack(fill="x", pady=20)

        history_columns = ('Date', 'Score', 'Percentage')
        history_tree = ttk.Treeview(history_frame, columns=history_columns, show='headings', height=3)
    
        for col, width in zip(history_columns, [180, 100, 100]):
            history_tree.heading(col, text=col)
            history_tree.column(col, width=width)
            
        # Set column headings
            tree.heading('Date', text='Date/time')
            tree.heading('Score', text='Score')
            tree.heading('Percentage', text='Percentage')

        player_history = self.db.get_player_history(self.user_name)
        for score_data in player_history:
            score_val, total, percentage, date = score_data
            # Handle date formatting - check if date is string or datetime
            date_str = date if isinstance(date, str) else date.strftime("%Y-%m-%d %H:%M")
            history_tree.insert('', 'end', values=(
                date_str,
                f"{score_val}/{total}",
                f"{percentage:.1f}%"
            ))

        history_tree.pack(pady=10)

        button_frame = ttk.Frame(final_frame)
        button_frame.pack(pady=20)

        # Screenshot button
        screenshot_btn = ttk.Button(
            button_frame,
            text="📸 Take Screenshot",
            command=lambda: self.capture_screenshot(final_frame),
            style="primary.TButton",
            width=20
        )
        screenshot_btn.pack(side="left", padx=10)

        # Add View Questions button
        view_questions_btn = ttk.Button(
            button_frame,
            text="📝 View Questions",
            command=self.show_questions_review,
            style="primary.TButton",
            width=20
        )
        view_questions_btn.pack(side="left", padx=10)

        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Leaderboard",
            command=self.clear_leaderboard,
            style="danger.TButton",
            width=20
        )
        clear_btn.pack(side="left", padx=10)

        restart_btn = ttk.Button(
            button_frame,
            text="🔄 Try Again",
            command=self.restart_quiz,
            style="success.TButton",
            width=20
        )
        restart_btn.pack(side="left", padx=10)


        exit_btn = ttk.Button(
            button_frame,
            text="👋 Exit",
            command=self.root.destroy,
            style="danger.TButton",
            width=20
        )
        exit_btn.pack(side="left", padx=10)

    def clear_leaderboard(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the leaderboard? This action cannot be undone."):
            self.db.clear_leaderboard()
            messagebox.showinfo("Success", "Leaderboard has been cleared!")
            self.show_final_score()  # Refresh the final score screen


    def cleanup_and_exit(self):
        self.db.close()
        self.root.destroy()

    def show_questions_review(self):
        # Create a new top-level window
        review_window = tk.Toplevel(self.root)
        review_window.title("Quiz Questions Review")
        review_window.geometry("800x600")
        
        # Add a scrolled frame
        container = ttk.Frame(review_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a canvas with scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(
            scrollable_frame,
            text="📚 Questions and Answers 📚",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Display each question and its answer
        for i, question_data in enumerate(self.quiz_data, 1):
            question_frame = ttk.LabelFrame(
                scrollable_frame,
                text=f"Question {i}",
                padding=10
            )
            question_frame.pack(fill="x", pady=10, padx=5)
            
            # Question text
            question_label = ttk.Label(
                question_frame,
                text=question_data["question"],
                font=("Helvetica", 12),
                wraplength=700
            )
            question_label.pack(anchor="w", pady=(0, 10))
            
            # Correct answer
            answer_label = ttk.Label(
                question_frame,
                text=f"Correct Answer: {question_data['answer']}",
                font=("Helvetica", 12, "bold"),
                foreground="green"
            )
            answer_label.pack(anchor="w")
            
            # All choices
            choices_label = ttk.Label(
                question_frame,
                text="All choices:\n" + "\n".join([f"• {choice}" for choice in question_data["choices"]]),
                font=("Helvetica", 11),
                justify="left"
            )
            choices_label.pack(anchor="w", pady=(5, 0))
        
        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = ttk.Button(
            review_window,
            text="Close",
            command=review_window.destroy,
            style="danger.TButton",
            width=20
        )
        close_btn.pack(pady=20)
        
        # Make the window modal
        review_window.transient(self.root)
        review_window.grab_set()
        
        # Center the window on screen
        review_window.update_idletasks()
        width = review_window.winfo_width()
        height = review_window.winfo_height()
        x = (review_window.winfo_screenwidth() // 2) - (width // 2)
        y = (review_window.winfo_screenheight() // 2) - (height // 2)
        review_window.geometry(f'{width}x{height}+{x}+{y}')

    def restart_quiz(self):
        if self.timer:
            self.root.after_cancel(self.timer)
       
        self.quiz_data = self.shuffle_questions(self.original_quiz_data.copy())    
        self.current_question = 0
        self.score = 0
        self.unanswered_questions = []
        self.answered_questions = set()
        self.retry_mode = False
        self.is_retry = True
        self.user_name = ""
        self.question_times = {} 

        for widget in self.root.winfo_children():
            widget.destroy()

        self.show_name_entry()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, quiz_data)
    root.mainloop()