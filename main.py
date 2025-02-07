import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class WatermarkApp:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Image Watermark Tool")
        self.window.geometry("1200x900")  # Slightly wider for better spacing
        
        # Use a modern color scheme
        self.bg_color = '#F0F4F8'  # Light blue-grey background
        self.accent_color = '#1A73E8'  # Google blue
        self.window.configure(bg=self.bg_color)
        
        # Configure the style
        self.setup_styles()
        
        # Initialize variables
        self.image_path = None
        self.current_image = None
        
        # Create the user interface
        self.setup_ui()
    
    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.configure(
            "Custom.TFrame",
            background=self.bg_color
        )
        
        # Modern button style
        style.configure(
            "Custom.TButton",
            font=("Arial", 11),
            padding=10,
            background=self.accent_color
        )
        
        # Label style
        style.configure(
            "Custom.TLabel",
            font=("Arial", 11),
            background=self.bg_color,
            padding=5
        )
        
        # Entry style
        style.configure(
            "Custom.TEntry",
            padding=8
        )
        
        # Options frame style
        style.configure(
            "Custom.TLabelframe",
            background=self.bg_color,
            padding=15
        )
        
        style.configure(
            "Custom.TLabelframe.Label",
            font=("Arial", 11, "bold"),
            background=self.bg_color,
            foreground=self.accent_color
        )
        
        # Scale style
        style.configure(
            "Custom.Horizontal.TScale",
            background=self.bg_color
        )
    
    def setup_ui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.window, padding="30", style="Custom.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create left frame for controls with a border
        controls_frame = ttk.Frame(
            main_frame,
            padding="25",
            style="Custom.TFrame"
        )
        controls_frame.grid(row=0, column=0, sticky="n", padx=(0, 30))
        
        # Upload button section
        self.upload_button = ttk.Button(
            controls_frame,
            text="Upload Image",
            command=self.upload_image,
            style="Custom.TButton"
        )
        self.upload_button.grid(row=0, column=0, pady=(0, 25), sticky="ew")
        
        # Watermark text entry section
        self.watermark_label = ttk.Label(
            controls_frame,
            text="Enter your watermark text:",
            style="Custom.TLabel"
        )
        self.watermark_label.grid(row=1, column=0, pady=(0, 5), sticky="w")
        
        self.watermark_entry = ttk.Entry(
            controls_frame,
            width=35,
            font=("Arial", 11),
            style="Custom.TEntry"
        )
        self.watermark_entry.grid(row=2, column=0, pady=(0, 25), sticky="ew")
        
        # Watermark options section
        self.create_watermark_options(controls_frame)
        
        # Apply watermark button
        self.apply_button = ttk.Button(
            controls_frame,
            text="Apply Watermark",
            command=self.apply_watermark,
            style="Custom.TButton"
        )
        self.apply_button.grid(row=4, column=0, pady=25, sticky="ew")
        
        # Status message display
        self.status_label = ttk.Label(
            controls_frame,
            text="",
            wraplength=400,
            style="Custom.TLabel"
        )
        self.status_label.grid(row=5, column=0, pady=10)
        
        # Create right frame for preview with a subtle border
        preview_frame = ttk.Frame(
            main_frame,
            padding="2",
            style="Custom.TFrame"
        )
        preview_frame.grid(row=0, column=1, sticky="nsew")
        
        # Add image preview area with a placeholder message
        self.preview_label = ttk.Label(
            preview_frame,
            text="Preview will appear here",
            style="Custom.TLabel"
        )
        self.preview_label.grid(row=0, column=0, sticky="nsew")
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
    
    def create_watermark_options(self, parent):
        # Options frame for watermark customization
        options_frame = ttk.LabelFrame(
            parent,
            text="Watermark Options",
            padding="20",
            style="Custom.TLabelframe"
        )
        options_frame.grid(row=3, column=0, pady=(0, 20), sticky="ew")
        
        # Opacity slider
        ttk.Label(
            options_frame,
            text="Opacity:",
            style="Custom.TLabel"
        ).grid(row=0, column=0, padx=5, sticky="w")
        
        self.opacity_var = tk.DoubleVar(value=50)
        self.opacity_slider = ttk.Scale(
            options_frame,
            from_=0,
            to=100,
            variable=self.opacity_var,
            orient="horizontal",
            style="Custom.Horizontal.TScale"
        )
        self.opacity_slider.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Color picker section
        ttk.Label(
            options_frame,
            text="Color:",
            style="Custom.TLabel"
        ).grid(row=1, column=0, padx=5, pady=15, sticky="w")
        
        color_frame = ttk.Frame(options_frame, style="Custom.TFrame")
        color_frame.grid(row=1, column=1, pady=15, sticky="w")
        
        self.color_preview = tk.Label(
            color_frame,
            width=3,
            height=1,
            bg='black',
            relief="solid",
            borderwidth=1
        )
        self.color_preview.grid(row=0, column=0, padx=5)
        
        self.color_button = ttk.Button(
            color_frame,
            text="Choose Color",
            command=self.choose_color,
            style="Custom.TButton"
        )
        self.color_button.grid(row=0, column=1, padx=5)
        
        # Store the current color (default: black)
        self.current_color = '#000000'
        
        # Position selector
        ttk.Label(
            options_frame,
            text="Position:",
            style="Custom.TLabel"
        ).grid(row=2, column=0, padx=5, pady=(15,5), sticky="w")
        
        # Position frame
        position_frame = ttk.Frame(options_frame)
        position_frame.grid(row=2, column=1, pady=10)
        
        # Position radio buttons
        self.position_var = tk.StringVar(value="center")
        positions = [
            ("Center", "center"),
            ("Top Left", "top_left"),
            ("Top Right", "top_right"),
            ("Bottom Left", "bottom_left"),
            ("Bottom Right", "bottom_right"),
            ("Custom", "custom")
        ]
        
        # Create radio buttons in a grid layout
        for i, (text, value) in enumerate(positions):
            rb = ttk.Radiobutton(
                position_frame,
                text=text,
                value=value,
                variable=self.position_var,
                command=self.toggle_custom_position
            )
            rb.grid(row=i//2, column=i%2, padx=5, pady=2, sticky="w")
        
        # Custom position frame (initially hidden)
        self.custom_pos_frame = ttk.Frame(options_frame)
        self.custom_pos_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        # X position
        ttk.Label(self.custom_pos_frame, text="X (%):").grid(row=0, column=0, padx=5)
        self.x_pos_var = tk.StringVar(value="50")
        self.x_pos_entry = ttk.Entry(
            self.custom_pos_frame,
            textvariable=self.x_pos_var,
            width=5
        )
        self.x_pos_entry.grid(row=0, column=1, padx=5)
        
        # Y position
        ttk.Label(self.custom_pos_frame, text="Y (%):").grid(row=0, column=2, padx=5)
        self.y_pos_var = tk.StringVar(value="50")
        self.y_pos_entry = ttk.Entry(
            self.custom_pos_frame,
            textvariable=self.y_pos_var,
            width=5
        )
        self.y_pos_entry.grid(row=0, column=3, padx=5)
        
        # Initially hide custom position inputs
        self.custom_pos_frame.grid_remove()
    
    def choose_color(self):
        """Open color picker dialog and update preview"""
        color = colorchooser.askcolor(
            title="Choose Watermark Color",
            color=self.current_color
        )
        
        if color[1]:  # If a color was chosen (not cancelled)
            self.current_color = color[1]
            self.color_preview.configure(bg=self.current_color)
            
            # Update status
            self.status_label.config(
                text=f"Color updated to {self.current_color}",
                foreground="green"
            )
    
    def upload_image(self):
        """Handle image upload functionality"""
        file_types = [
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        ]
        
        # Open file dialog for image selection
        self.image_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=file_types
        )
        
        if self.image_path:
            try:
                # Open and store the image
                self.current_image = Image.open(self.image_path)
                
                # Create preview
                self.update_preview()
                
                # Update status
                self.status_label.config(
                    text="Image uploaded successfully!",
                    foreground="green"
                )
            except Exception as e:
                self.status_label.config(
                    text=f"Error loading image: {str(e)}",
                    foreground="red"
                )
    
    def update_preview(self):
        """Update the preview of the image"""
        if self.current_image:
            # Calculate preview size (max 800px width/height)
            preview_size = (800, 800)
            preview_image = self.current_image.copy()
            preview_image.thumbnail(preview_size)
            
            # Convert to PhotoImage for display
            preview_photo = ImageTk.PhotoImage(preview_image)
            
            # Update preview label
            self.preview_label.configure(image=preview_photo)
            self.preview_label.image = preview_photo  # Keep a reference
    
    def apply_watermark(self):
        """Apply watermark to the uploaded image"""
        if not self.current_image:
            self.status_label.config(
                text="Please upload an image first!",
                foreground="red"
            )
            return
        
        watermark_text = self.watermark_entry.get().strip()
        if not watermark_text:
            self.status_label.config(
                text="Please enter watermark text!",
                foreground="red"
            )
            return
        
        try:
            # Create a copy of the original image
            watermarked = self.current_image.copy()
            
            # Create drawing context
            draw = ImageDraw.Draw(watermarked, 'RGBA')
            
            # Calculate font size (proportional to image size)
            font_size = min(watermarked.size) // 20
            font = ImageFont.truetype("arial.ttf", font_size)
            
            # Get text size
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Get position based on user selection
            x, y = self.get_watermark_position(
                text_width,
                text_height,
                watermarked.width,
                watermarked.height
            )
            
            # Convert hex color to RGB and add opacity
            r, g, b = tuple(int(self.current_color[1:][i:i+2], 16) for i in (0, 2, 4))
            opacity = int(255 * (self.opacity_var.get() / 100))
            
            # Draw watermark text with selected color
            draw.text(
                (x, y),
                watermark_text,
                font=font,
                fill=(r, g, b, opacity)
            )
            
            # Save the watermarked image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile="watermarked_image.png"
            )
            
            if save_path:
                watermarked.save(save_path)
                self.status_label.config(
                    text="Watermark applied and image saved successfully!",
                    foreground="green"
                )
                
                # Update preview with watermarked image
                self.current_image = watermarked
                self.update_preview()
                
        except Exception as e:
            self.status_label.config(
                text=f"Error applying watermark: {str(e)}",
                foreground="red"
            )
    
    def toggle_custom_position(self):
        """Show/hide custom position inputs based on selection"""
        if self.position_var.get() == "custom":
            self.custom_pos_frame.grid()
        else:
            self.custom_pos_frame.grid_remove()
    
    def get_watermark_position(self, text_width, text_height, image_width, image_height):
        """Calculate watermark position based on selected option"""
        position = self.position_var.get()
        padding = 20  # Padding from edges
        
        try:
            if position == "custom":
                # Get percentage values and convert to actual positions
                x_percent = float(self.x_pos_var.get())
                y_percent = float(self.y_pos_var.get())
                
                # Clamp values between 0 and 100
                x_percent = max(0, min(100, x_percent))
                y_percent = max(0, min(100, y_percent))
                
                x = int((image_width - text_width) * (x_percent / 100))
                y = int((image_height - text_height) * (y_percent / 100))
            else:
                positions = {
                    "center": (
                        (image_width - text_width) // 2,
                        (image_height - text_height) // 2
                    ),
                    "top_left": (
                        padding,
                        padding
                    ),
                    "top_right": (
                        image_width - text_width - padding,
                        padding
                    ),
                    "bottom_left": (
                        padding,
                        image_height - text_height - padding
                    ),
                    "bottom_right": (
                        image_width - text_width - padding,
                        image_height - text_height - padding
                    )
                }
                x, y = positions[position]
            
            return x, y
            
        except ValueError:
            # If there's an error parsing custom values, default to center
            return (image_width - text_width) // 2, (image_height - text_height) // 2
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = WatermarkApp()
    app.run()
