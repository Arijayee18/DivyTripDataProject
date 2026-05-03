import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_plot():
    """Read inputs, validate, and render the loading-bar box plot."""
    try:
        min_val = float(entry_min.get())
        avg_val = float(entry_avg.get())
        max_val = float(entry_max.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    if not (min_val <= avg_val <= max_val):
        messagebox.showerror("Input Error", "Must satisfy: Min ≤ Average ≤ Max")
        return

    # --- Build box plot stats manually ---
    stats = [{
        'med':    avg_val,
        'q1':     avg_val - (avg_val - min_val) * 0.15,  # slight box width around avg
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
        patch_artist=True,          # lets us fill the box with color
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
root.title("Trip Time Plotter")
root.configure(bg='#F5F6FA')

frame_inputs = tk.Frame(root, bg='#F5F6FA', pady=10)
frame_inputs.pack()

for col, (label_text, default) in enumerate([("Min (min)", "10"), ("Avg (min)", "25"), ("Max (min)", "55")]):
    tk.Label(frame_inputs, text=label_text, bg='#F5F6FA', font=('Arial', 10)).grid(row=0, column=col, padx=15)

entry_min = tk.Entry(frame_inputs, width=8, font=('Arial', 11), justify='center')
entry_avg = tk.Entry(frame_inputs, width=8, font=('Arial', 11), justify='center')
entry_max = tk.Entry(frame_inputs, width=8, font=('Arial', 11), justify='center')

for col, (entry, default) in enumerate([(entry_min, "10"), (entry_avg, "25"), (entry_max, "55")]):
    entry.insert(0, default)
    entry.grid(row=1, column=col, padx=15, pady=5)

tk.Button(
    root, text="▶  Generate Plot", command=draw_plot,
    bg='#4A90D9', fg='white', font=('Arial', 11, 'bold'),
    relief='flat', padx=12, pady=6
).pack(pady=8)

# ── Matplotlib canvas embedded in Tkinter ─────────────────────
fig, ax = plt.subplots(figsize=(7, 2.5))
fig.patch.set_facecolor('#F5F6FA')
ax.set_facecolor('#F5F6FA')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=20, pady=10)

draw_plot()       # render with defaults on startup
root.mainloop()
