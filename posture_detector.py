import cv2
import mediapipe as mp
import numpy as np
import winsound
import time
import math
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PostureApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("AI Posture Monitor")
        self.geometry("800x700")
        self.minsize(800, 700)
        
        # AI & State Variables
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.last_beep_time = 0
        self.beep_cooldown = 2.0
        self.is_running = False

        # UI Layout
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E24")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="AI Posture Monitor", 
                                        font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(self.main_frame, text="Press Start to Begin", 
                                         font=ctk.CTkFont(family="Helvetica", size=18))
        self.status_label.pack(pady=(0, 15))

        self.video_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="black")
        self.video_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(self.video_frame, width=640, height=480, bg="black", highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)

        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_start = ctk.CTkButton(self.btn_frame, text="▶ Start Camera", width=160, height=40, 
                                       corner_radius=20, fg_color="#27AE60", hover_color="#219A52",
                                       font=ctk.CTkFont(size=14, weight="bold"), command=self.start_camera)
        self.btn_start.grid(row=0, column=0, padx=15)

        self.btn_stop = ctk.CTkButton(self.btn_frame, text="⏹ Stop Camera", width=160, height=40, 
                                      corner_radius=20, fg_color="#E74C3C", hover_color="#C0392B",
                                      font=ctk.CTkFont(size=14, weight="bold"), command=self.stop_camera, 
                                      state="disabled")
        self.btn_stop.grid(row=0, column=1, padx=15)

        self.cap = cv2.VideoCapture(0)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status_label.configure(text="Initializing...", text_color="white")
        self.update_frame()

    def stop_camera(self):
        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_label.configure(text="Camera Stopped", text_color="white")
        self.canvas.delete("all") 

    def update_frame(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose.process(image)
            image.flags.writeable = True

            try:
                landmarks = results.pose_landmarks.landmark
                
                # Math: Posture Ratio Calculation
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

                # Draw Visual Guide
                shoulder_px = tuple(np.multiply(mid_shoulder, [640, 480]).astype(int))
                ear_px = tuple(np.multiply(mid_ear, [640, 480]).astype(int))
                cv2.line(image, ear_px, shoulder_px, (255, 255, 0), 2)
                cv2.putText(image, f"Ratio: {int(posture_ratio)}", (shoulder_px[0] + 20, shoulder_px[1]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

                # Status Updates & Alerts
                if is_slouching:
                    self.status_label.configure(text="⚠️ SLOUCHING DETECTED", text_color="#E74C3C")
                    
                    current_time = time.time()
                    if current_time - self.last_beep_time > self.beep_cooldown:
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
                        self.last_beep_time = current_time
                else:
                    self.status_label.configure(text="✅ GOOD POSTURE", text_color="#27AE60")

            except Exception:
                pass 

            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            # Render to Canvas
            img_pil = Image.fromarray(image)
            self.photo = ImageTk.PhotoImage(image=img_pil)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        # Loop processing
        if self.is_running:
            self.after(15, self.update_frame)

    def on_closing(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = PostureApp()
    app.mainloop()