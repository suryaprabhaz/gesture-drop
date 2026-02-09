import sys
import traceback

print(f"Python executing: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    print("Attempting to import mediapipe...")
    import mediapipe as mp
    print(f"MediaPipe imported. Version: {getattr(mp, '__version__', 'unknown')}")
    
    print("Accessing mp.solutions...")
    mp_solutions = mp.solutions
    print(f"mp.solutions: {mp_solutions}")

    print("Accessing mp.solutions.hands...")
    mp_hands = mp.solutions.hands
    print(f"mp.solutions.hands: {mp_hands}")

    print("Initializing Hands...")
    hands = mp_hands.Hands(
        static_image_mode=False, 
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    print("Hands initialized successfully!")

except Exception:
    traceback.print_exc()
