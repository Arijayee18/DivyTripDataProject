import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import nbimporter
from divvyTripStatAnalysis.ipynb import TripAnalysis


def draw_plot(min_val, avg_val, max_val):
    """Receive min/avg/max and render the loading-bar box plot."""
    if not (min_val <= avg_val <= max_val):
        messagebox.showerror("Input Error", "Must satisfy: Min ≤ Average ≤ Max")
        return

    # --- Build box plot stats manually ---
    stats = [{
        'med':    avg_val,
        'q1':     avg_val - (avg_val - min_val) * 0.15,
        'q3':     avg_val + (max_val - avg_val) * 0.15,
        'whislo': min_val,
        'whishi': max_val,
        'fliers': []
    }]

    # --- Draw the plot ---
    ax.clear()
    bp = ax.bxp(
        stats,
        vert=False,
        widths=0.4,
        patch_artist=True,
        showfliers=False
    )

    # Style: fill box with a blue gradient look
    for patch in bp['boxes']:
        patch.set_facecolor('#4A90D9')
        patch.set_alpha(0.8)
    for whisker in bp['whiskers']:
        whisker.set(color='#2C3E50', linewidth=2, linestyle='-')
    for cap in bp['caps']:
        cap.set(color='#2C3E50', linewidth=3)
    for median in bp['medians']:
        median.set(color='white', linewidth=2)

    # Annotate min, avg, max
    y_pos = 1.28
    ax.text(min_val, y_pos, f"Min\n{min_val:.1f} min", ha='center', fontsize=9, color='#2C3E50')
    ax.text(avg_val, y_pos, f"Avg\n{avg_val:.1f} min", ha='center', fontsize=9, color='#4A90D9', fontweight='bold')
    ax.text(max_val, y_pos, f"Max\n{max_val:.1f} min", ha='center', fontsize=9, color='#2C3E50')

    # Clean up axes
    ax.set_title("Trip Time Distribution", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Time (minutes)")
    ax.set_yticks([])
    ax.set_xlim(min_val - (max_val - min_val) * 0.2,
                max_val + (max_val - min_val) * 0.2)
    ax.spines[['top', 'right', 'left']].set_visible(False)

    canvas.draw()


# ── GUI Layout ────────────────────────────────────────────────
root = tk.Tk()
root.title("Divvy Trip Time Estimate Visualizer")
root.configure(bg='#F5F6FA')

frame_inputs = tk.Frame(root, bg='#F5F6FA', pady=10)
frame_inputs.pack()

# ── Labels ────────────────────────────────────────────────────
labels = ["Start Distance (mi)", "Gender", "User Type", "Starting Hour (0-23)", "Dock Capacity"]
for col, label_text in enumerate(labels):
    tk.Label(frame_inputs, text=label_text, bg='#F5F6FA', font=('Arial', 10)).grid(row=0, column=col, padx=15)

# ── Inputs ────────────────────────────────────────────────────
entry_distance = tk.Entry(frame_inputs, width=10, font=('Arial', 11), justify='center')
entry_distance.insert(0, "1.5")
entry_distance.grid(row=1, column=0, padx=15, pady=5)

combo_gender = ttk.Combobox(frame_inputs, width=9, font=('Arial', 11), justify='center', state='readonly')
combo_gender['values'] = ("Male", "Female", "Null")
combo_gender.current(0)
combo_gender.grid(row=1, column=1, padx=15, pady=5)

combo_usertype = ttk.Combobox(frame_inputs, width=9, font=('Arial', 11), justify='center', state='readonly')
combo_usertype['values'] = ("Casual", "Member")
combo_usertype.current(0)
combo_usertype.grid(row=1, column=2, padx=15, pady=5)

entry_hour = tk.Entry(frame_inputs, width=10, font=('Arial', 11), justify='center')
entry_hour.insert(0, "8")
entry_hour.grid(row=1, column=3, padx=15, pady=5)

entry_capacity = tk.Entry(frame_inputs, width=10, font=('Arial', 11), justify='center')
entry_capacity.insert(0, "15")
entry_capacity.grid(row=1, column=4, padx=15, pady=5)


# ── Send to TripAnalysis ───────────────────────────────────────
def run_analysis():
    try:
        distance  = float(entry_distance.get())
        gender    = combo_gender.get()
        user_type = combo_usertype.get()
        hour      = int(entry_hour.get())
        capacity  = int(entry_capacity.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid values.")
        return

    if not (0 <= hour <= 23):
        messagebox.showerror("Input Error", "Hour must be between 0 and 23.")
        return

    if capacity < 1:
        messagebox.showerror("Input Error", "Dock capacity must be at least 1.")
        return

    # Send inputs to TripAnalysis
    analyzer = TripAnalysis(
        distance  = distance,
        gender    = gender,
        user_type = user_type,
        hour      = hour,
        capacity  = capacity
    )

    stats = analyzer.get_stats()

    # Feed stats into the plot
    draw_plot(stats["min"], stats["avg"], stats["max"])


# ── Plot Button ───────────────────────────────────────────────
tk.Button(
    root, text="▶  Generate Plot", command=run_analysis,
    bg='#4A90D9', fg='white', font=('Arial', 11, 'bold'),
    relief='flat', padx=12, pady=6
).pack(pady=8)

# ── Matplotlib canvas embedded in Tkinter ─────────────────────
fig, ax = plt.subplots(figsize=(7, 2.5))
fig.patch.set_facecolor('#F5F6FA')
ax.set_facecolor('#F5F6FA')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=20, pady=10)

draw_plot(10, 25, 55)   # placeholder values on startup until user clicks Generate
root.mainloop()
