import cv2
import mediapipe as mp
import numpy as np
import winsound
import time
import math
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# --- CustomTkinter Global Settings ---
ctk.set_appearance_mode("dark")        # Modes: "system", "light", "dark"
ctk.set_default_color_theme("blue")    # Themes: "blue", "green", "dark-blue"

class PostureApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("AI Posture Monitor")
        self.geometry("800x700")
        self.minsize(800, 700)
        
        # --- AI Variables ---
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.last_beep_time = 0
        self.beep_cooldown = 2.0
        self.is_running = False

        # --- UI Layout Design ---
        # Main Container to hold everything centered
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E24")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Header Text
        self.title_label = ctk.CTkLabel(self.main_frame, text="AI Posture Monitor", 
                                        font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # Status Label (The text that turns Green or Red)
        self.status_label = ctk.CTkLabel(self.main_frame, text="Press Start to Begin", 
                                         font=ctk.CTkFont(family="Helvetica", size=18))
        self.status_label.pack(pady=(0, 15))

        # Video Panel (Tkinter Canvas inside a CustomTkinter frame for nice borders)
        self.video_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="black")
        self.video_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480, bg="black", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)

        # Buttons Container
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        # Beautiful Rounded Start Button
        self.btn_start = ctk.CTkButton(self.btn_frame, text="▶ Start Camera", width=160, height=40, 
                                       corner_radius=20, fg_color="#27AE60", hover_color="#219A52",
                                       font=ctk.CTkFont(size=14, weight="bold"), command=self.start_camera)
        self.btn_start.grid(row=0, column=0, padx=15)

        # Beautiful Rounded Stop Button
        self.btn_stop = ctk.CTkButton(self.btn_frame, text="⏹ Stop Camera", width=160, height=40, 
                                      corner_radius=20, fg_color="#E74C3C", hover_color="#C0392B",
                                      font=ctk.CTkFont(size=14, weight="bold"), command=self.stop_camera, 
                                      state="disabled")
        self.btn_stop.grid(row=0, column=1, padx=15)

        # Camera Initialization
        self.cap = cv2.VideoCapture(0)
        
        # Graceful exit
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        """Activates the video feed loop."""
        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_label.configure(text="Initializing...", text_color="white")
        self.update_frame()

    def stop_camera(self):
        """Pauses the video feed."""
        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_label.configure(text="Camera Stopped", text_color="white")
        self.canvas.delete("all") 

    def update_frame(self):
        """Reads a frame, processes AI, and updates the UI."""
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            # OpenCV & MediaPipe AI Processing
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose.process(image)
            image.flags.writeable = True

            try:
                landmarks = results.pose_landmarks.landmark
                
                # Math: Calculate Posture Ratio
                l_ear = [landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].y]
                r_ear = [landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].y]
                mid_ear = [(l_ear[0] + r_ear[0]) / 2, (l_ear[1] + r_ear[1]) / 2]

                l_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                r_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                mid_shoulder = [(l_shoulder[0] + r_shoulder[0]) / 2, (l_shoulder[1] + r_shoulder[1]) / 2]

                neck_height = abs(mid_shoulder[1] - mid_ear[1])
                shoulder_width = math.dist(l_shoulder, r_shoulder)
                posture_ratio = (neck_height / shoulder_width) * 100
                
                is_slouching = posture_ratio < 35 

                # Draw Visual Math Lines
                shoulder_px = tuple(np.multiply(mid_shoulder, [640, 480]).astype(int))
                ear_px = tuple(np.multiply(mid_ear, [640, 480]).astype(int))
                cv2.line(image, ear_px, shoulder_px, (255, 255, 0), 2)
                cv2.putText(image, f"Ratio: {int(posture_ratio)}", (shoulder_px[0] + 20, shoulder_px[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

                # Modern UI Status Updates
                if is_slouching:
                    self.status_label.configure(text="⚠️ SLOUCHING DETECTED", text_color="#E74C3C") # Soft Red
                    
                    current_time = time.time()
                    if current_time - self.last_beep_time > self.beep_cooldown:
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        self.last_beep_time = current_time
                else:
                    self.status_label.configure(text="✅ GOOD POSTURE", text_color="#27AE60") # Soft Green

            except Exception as e:
                pass 

            # Draw AI Skeleton
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            # Render to Tkinter Canvas
            img_pil = Image.fromarray(image)
            self.photo = ImageTk.PhotoImage(image=img_pil)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Loop at ~60 FPS
        if self.is_running:
            self.after(15, self.update_frame)

    def on_closing(self):
        """Cleans up resources when closing."""
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

# Run Application
if __name__ == "__main__":
    app = PostureApp()
    app.mainloop()