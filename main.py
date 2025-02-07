import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class WatermarkApp:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Image Watermark Tool")
        
        # Make the window size reasonable
        self.window.geometry("800x600")
        
        # Use a dyslexic-friendly color scheme
        # Light cream background is easier on the eyes
        self.window.configure(bg='#FFF4E6')
        
        # Initialize variables
        self.image_path = None
        self.current_image = None
        
        # Create the user interface
        self.setup_ui()
    
    def setup_ui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights to make the preview area expandable
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Style configuration for dyslexic-friendly reading
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))  # Clear, sans-serif font
        style.configure("TButton", font=("Arial", 12))
        
        # Upload button section
        self.upload_button = ttk.Button(
            main_frame,
            text="Upload Image",
            command=self.upload_image
        )
        self.upload_button.grid(row=0, column=0, pady=20)
        
        # Watermark text entry section
        self.watermark_label = ttk.Label(
            main_frame,
            text="Enter your watermark text:"
        )
        self.watermark_label.grid(row=1, column=0, pady=10)
        
        self.watermark_entry = ttk.Entry(
            main_frame,
            width=40,
            font=("Arial", 12)
        )
        self.watermark_entry.grid(row=2, column=0, pady=10)
        
        # Watermark options section
        self.create_watermark_options(main_frame)
        
        # Add image preview area
        self.preview_label = ttk.Label(main_frame)
        self.preview_label.grid(row=6, column=0, pady=10)
        
        # Apply watermark button
        self.apply_button = ttk.Button(
            main_frame,
            text="Apply Watermark",
            command=self.apply_watermark
        )
        self.apply_button.grid(row=4, column=0, pady=20)
        
        # Status message display
        self.status_label = ttk.Label(
            main_frame,
            text="",
            wraplength=500  # Prevent long text from extending window
        )
        self.status_label.grid(row=5, column=0, pady=10)
    
    def create_watermark_options(self, parent):
        # Options frame for watermark customization
        options_frame = ttk.LabelFrame(
            parent,
            text="Watermark Options",
            padding="10"
        )
        options_frame.grid(row=3, column=0, pady=20)
        
        # Opacity slider
        ttk.Label(options_frame, text="Opacity:").grid(row=0, column=0)
        self.opacity_var = tk.DoubleVar(value=50)
        self.opacity_slider = ttk.Scale(
            options_frame,
            from_=0,
            to=100,
            variable=self.opacity_var,
            orient="horizontal"
        )
        self.opacity_slider.grid(row=0, column=1)
    
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
            # Calculate preview size (max 400px width/height)
            preview_size = (400, 400)
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
            
            # Calculate position (centered)
            x = (watermarked.width - text_width) // 2
            y = (watermarked.height - text_height) // 2
            
            # Calculate opacity
            opacity = int(255 * (self.opacity_var.get() / 100))
            
            # Draw watermark text
            draw.text(
                (x, y),
                watermark_text,
                font=font,
                fill=(0, 0, 0, opacity)
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
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = WatermarkApp()
    app.run()
