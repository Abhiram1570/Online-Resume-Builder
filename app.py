from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

app = Flask(__name__)

# Ensure output folder exists
if not os.path.exists("generated_resumes"):
    os.makedirs("generated_resumes")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Get form data
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    skills = request.form["skills"]
    education = request.form["education"]
    experience = request.form["experience"]

    # Create PDF filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_path = f"generated_resumes/{name.replace(' ', '_')}_{timestamp}.pdf"

    # Generate PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, name)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Email: {email}")
    c.drawString(50, height - 100, f"Phone: {phone}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 140, "Skills")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, skills)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "Education")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, education)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 260, "Experience")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 280, experience)

    c.showPage()
    c.save()

    return render_template("success.html", filename=pdf_path)

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
