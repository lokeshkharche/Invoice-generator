import os
import subprocess
import sys
import shutil
import platform

# ==========================================================
#  📝 CONFIGURATION (Edit this section for each new invoice)
# ==========================================================

# 1. Clinic & Therapist Info
CLINIC_NAME = "MoveWell"
CLINIC_WEB = "Mrunmayeepitale23@gmail.com"
CLINIC_PHONE = "8669969792"
CLINIC_ADDRESS = "Suvarna Park,Bavdhan"
THERAPIST_NAME = "Dr Mrunmayee Pitale"
REGISTRATION_NO = "4372"
SIGNATORY_NAME = "Dr Mrunmayee Pitale"
SIGNATURE_IMG = "1787139977.png"  # MUST be in the same folder as this script!

# 2. Patient & Invoice Info
INVOICE_NO = "INV-820"
BILL_DATE = "19/08/2026"
BILLED_NAME = "Mr Abhinav Srivastava"
BILLED_ADDRESS = "Blueridge Township Pune"
BILLED_CONTACT = "9711204628"
SESSION_PERIOD = "19/08/2026 - 19/08/2026"
CONDITION_TREATED = "Lower Body"

# 3. Treatments Provided
TREATMENTS = [
    "Strength and conditioning for lower body",
    "Sciatica treatment",
    "Exercise for bilateral knee"
]

# 4. Billing Calculation
TOTAL_SESSIONS = 1
PER_SESSION_CHARGE = 800.00
DISCOUNT_PERCENT = 0

# ==========================================================
#  ⚙️ GENERATOR & COMPILER LOGIC
# ==========================================================

# Auto-calculate totals
sub_total = TOTAL_SESSIONS * PER_SESSION_CHARGE
discount_amount = sub_total * (DISCOUNT_PERCENT / 100)
grand_total = sub_total - discount_amount

# Format treatments for LaTeX
treatments_latex = "\\textbf{Treatments provided:}\\newline\n" + \
                   "\\newline\n".join([f"-- {t}" for t in TREATMENTS])

# LaTeX Template
LATEX_TEMPLATE = r"""% !TEX program = xelatex
\documentclass[11pt]{article}
\usepackage[a4paper,margin=15mm]{geometry}
\usepackage[table]{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{tabularx}
\usepackage{array}
\usepackage{ragged2e}
\usepackage{graphicx}
\usepackage{fontspec} % Required for XeLaTeX to render symbols like ₹ properly
\pagestyle{empty}
\setlength{\parindent}{0pt}
\definecolor{physioteal}{HTML}{15A398}
\definecolor{darktext}{HTML}{2B2B2B}
\definecolor{graytext}{HTML}{5F5F5F}
\definecolor{bordergray}{HTML}{DADADA}

\begin{document}
\thispagestyle{empty}

\begin{tcolorbox}[
  enhanced,
  colback=white,
  colframe=bordergray,
  boxrule=0.6pt,
  arc=3pt,
  drop shadow={black!35},
  width=\textwidth,
  left=30pt, right=30pt, top=26pt, bottom=24pt
]

\begin{center}
  {\fontsize{30}{34}\selectfont\bfseries\color{physioteal}__CLINIC_NAME__}\\[7pt]
  {\color{darktext}__CLINIC_WEB__\quad|\quad Ph: __CLINIC_PHONE__}\\[3pt]
  {\color{darktext}__CLINIC_ADDRESS__}
\end{center}

\vspace{10pt}
{\color{physioteal}\rule{\linewidth}{2.2pt}}
\vspace{18pt}

\noindent
\begin{minipage}[t]{0.52\linewidth}
\textbf{Billed To:} __BILLED_NAME__\\[4pt]
Address: __BILLED_ADDRESS__\\[4pt]
Contact: __BILLED_CONTACT__
\end{minipage}%
\begin{minipage}[t]{0.48\linewidth}
\raggedleft
\textbf{INVOICE / BILL NO:} __INVOICE_NO__\\[4pt]
\textbf{BILL DATE:} __BILL_DATE__\\[4pt]
Therapist Name: __THERAPIST_NAME__\\[4pt]
Registration No: __REGISTRATION_NO__\\[4pt]
Session Period: __SESSION_PERIOD__\\[4pt]
Condition Treated: __CONDITION_TREATED__
\end{minipage}

\vspace{24pt}

\renewcommand{\arraystretch}{1.5}
\small
\begin{tabularx}{\linewidth}{|>{\raggedright\arraybackslash}X|>{\centering\arraybackslash}p{1.8cm}|>{\centering\arraybackslash}p{2.6cm}|>{\centering\arraybackslash}p{1.8cm}|>{\centering\arraybackslash}p{1.8cm}|}
\hline
\rowcolor{black!5}
\textbf{Description} & \textbf{No. of Sessions} & \textbf{Per Session Charges (₹)} & \textbf{Discount (0\%)} & \textbf{Total (₹)}\\
\hline
__TREATMENTS_LATEX__
& __TOTAL_SESSIONS__ & __PER_SESSION_CHARGE__ & __DISCOUNT_PERCENT__\% & __SUB_TOTAL__\\
\hline
\multicolumn{4}{|r|}{\textbf{Sub Total:}} & \textbf{₹__SUB_TOTAL__}\\
\hline
\multicolumn{4}{|r|}{\textbf{Discount:}} & \textbf{₹__DISCOUNT_AMOUNT__}\\
\hline
\rowcolor{physioteal!8}
\multicolumn{4}{|r|}{\textbf{GRAND TOTAL:}} & \textbf{₹__GRAND_TOTAL__}\\
\hline
\end{tabularx}
\normalsize

\vspace{50pt}

\begin{flushright}
\begin{minipage}{0.42\linewidth}
\raggedleft
\includegraphics[height=1.5cm, keepaspectratio]{__SIGNATURE_IMG__}\\[2pt]
\rule{\linewidth}{0.5pt}\\[5pt]
__SIGNATORY_NAME__
\end{minipage}
\end{flushright}

\vspace{26pt}

{\itshape\color{graytext}Committed to providing the best home physiotherapy service with care.}

\end{tcolorbox}

\end{document}
"""

# Replace placeholders
replacements = {
    "__CLINIC_NAME__": CLINIC_NAME, "__CLINIC_WEB__": CLINIC_WEB,
    "__CLINIC_PHONE__": CLINIC_PHONE, "__CLINIC_ADDRESS__": CLINIC_ADDRESS,
    "__BILLED_NAME__": BILLED_NAME, "__BILLED_ADDRESS__": BILLED_ADDRESS,
    "__BILLED_CONTACT__": BILLED_CONTACT, "__INVOICE_NO__": INVOICE_NO,
    "__BILL_DATE__": BILL_DATE, "__THERAPIST_NAME__": THERAPIST_NAME,
    "__REGISTRATION_NO__": REGISTRATION_NO, "__SESSION_PERIOD__": SESSION_PERIOD,
    "__CONDITION_TREATED__": CONDITION_TREATED, "__TREATMENTS_LATEX__": treatments_latex,
    "__TOTAL_SESSIONS__": str(TOTAL_SESSIONS),
    "__PER_SESSION_CHARGE__": f"{PER_SESSION_CHARGE:.2f}",
    "__DISCOUNT_PERCENT__": str(DISCOUNT_PERCENT),
    "__SUB_TOTAL__": f"{sub_total:.2f}",
    "__DISCOUNT_AMOUNT__": f"{discount_amount:.2f}",
    "__GRAND_TOTAL__": f"{grand_total:.2f}",
    "__SIGNATURE_IMG__": SIGNATURE_IMG, "__SIGNATORY_NAME__": SIGNATORY_NAME,
}

output_tex = LATEX_TEMPLATE
for key, val in replacements.items():
    output_tex = output_tex.replace(key, val)

safe_name = BILLED_NAME.replace(' ', '_')
filename = f"{INVOICE_NO.replace('/', '-')}_{safe_name}.tex"
pdf_name = filename.replace('.tex', '.pdf')

# Save .tex file
with open(filename, "w", encoding="utf-8") as f:
    f.write(output_tex)
print(f"✅ Generated {filename}")


# --- AUTO-COMPILATION ENGINE ---
def find_xelatex():
    path = shutil.which("xelatex")
    if path: return path
    if platform.system() == "Windows":
        common = [
            r"C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe",
            r"C:\Users\{}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe".format(os.getlogin()),
            r"C:\texlive\2023\bin\windows\xelatex.exe",
            r"C:\texlive\2024\bin\windows\xelatex.exe"
        ]
        for p in common:
            if os.path.exists(p): return p
    if platform.system() == "Darwin":
        if os.path.exists("/Library/TeX/texbin/xelatex"): return "/Library/TeX/texbin/xelatex"
    return None


xelatex_path = find_xelatex()

if not xelatex_path:
    print("❌ ERROR: Could not find 'xelatex' on your computer.")
    print("👉 Please install MiKTeX (Windows) or MacTeX (Mac) to compile locally.")
else:
    if not os.path.exists(SIGNATURE_IMG):
        print(
            f"⚠️ WARNING: '{SIGNATURE_IMG}' not found in this folder. PDF compilation might fail or show a missing image box.")

    print("🔄 Compiling PDF locally... (this takes a few seconds)")
    # Run xelatex silently
    result = subprocess.run([xelatex_path, "-interaction=nonstopmode", filename], stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

    if result.returncode == 0 and os.path.exists(pdf_name):
        print(f"🎉 SUCCESS! Opening {pdf_name}...")
        # Clean up messy auxiliary files
        for ext in ['.aux', '.log', '.out']:
            try:
                os.remove(filename.replace('.tex', ext))
            except:
                pass

        # Automatically open the PDF
        if platform.system() == 'Windows':
            os.startfile(pdf_name)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', pdf_name])
        else:
            subprocess.run(['xdg-open', pdf_name])
    else:
        print("⚠️ Compilation failed. Check if your signature image is in the folder.")