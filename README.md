<!-- Bandeau image -->
<p align="center">
  <img src="https://nanovizer-aoz.piksail.com/assets/nanovizer-light-theme.a92c964a.svg" alt="Bandeau" width="100%" />
</p>

<!-- NanoViZer -->
<h1 align="center"><strong>NanoViZer</strong></h1>

---

## 1. Introduction

**NanoViZer (Nanopore Virus analyZER)** is a powerful bioinformatics tool designed to study deletions in viral RNA and genomes through full-length Nanopore sequencing.

## Features

- **Annotation-Free Analysis:** Enables the study of viral deletions without prior genomic knowledge.
- **Broad Viral Family Compatibility:** Proven to work with multiple viral families, including HIV-1, SARS-CoV-2, HSV-1, and HDV.
- **User-Friendly Interface:** Simple command-line activation and web-browser-based analysis.
- **Data Privacy:** All data remains local and is never uploaded to an external server.
- **No Heavy Computational Requirements:** Only an internet connection is needed.

## Ease of Use

NanoViZer is designed to be user-friendly, requiring minimal computational expertise. After installing a few necessary tools, users can activate NanoViZer with a simple command-line interface. All subsequent analyses are conducted via a web browser, such as Google Chrome. Your data remains local and is never uploaded to an external server, ensuring data privacy and security. Only an internet connection is required to run NanoViZer effectively.

## Demonstration

NanoViZer has been successfully demonstrated to analyze data from various viral families, including:

- HIV-1
- SARS-CoV-2
- HSV-1
- HDV

## How to Use

1. **Install Required Tools:** Follow the installation instructions to set up the necessary tools.
2. **Activate NanoViZer:** Use the provided command-line interface to activate NanoViZer.
3. **Conduct Analysis:** Open a web browser (e.g., Google Chrome) and follow the on-screen instructions to perform your analysis.

---

NanoViZer is an invaluable resource for researchers in the field of virology, providing a streamlined and effective way to analyze viral genome deletions using full-length Nanopore sequencing data.

---

## 2. Requierement
- Python >= 3.7
- Flask
- flask-cors
- pysam  
For installation, check the following section.

## 3. Installation

### 3.1 For Non-Bioinformaticians

If there are any issues, do not hesitate to contact us or ask to an IA!

#### 3.1.1 For Linux or macOS Users
1. First, download NanoViZer by clicking on the green "<> Code" button and choosing "Download ZIP".  
2. Then, unzip the file and move it to your Documents folder.  
3. Open the Terminal application already installed on your computer.  
4. If you are using macOS Silicon, use the following commands to install requirements :  
```bash
cd Documents/NanoViZer/ #Then press enter on your laptop
chmod +x install_packages.sh #Then press enter on your laptop
bash install_packages.sh #Then press enter on your laptop
```
5. If you are using macOS Intel, refer to section 3.1.2, point 5.

#### 3.1.2 For Windows Users

1. First, install WSL by following any tutorial you find online.  
2. Navigate to the Ubuntu environment.  
3. Type `pwd` to check your current location in your Terminal application.  
4. Use `cd following_folder` to navigate inside a folder that is inside your current folder (replace `following_folder` with the actual folder name).  

5. Navigate to the NanoViZer folder and then run the following commands:  
```bash
sudo apt update #Then press enter on your laptop and follow instructions
sudo apt install python3-pip #Then press enter on your laptop and follow instructions
cd Documents/NanoViZer/ #Then press enter on your laptop
chmod +x install_packages.sh #Then press enter on your laptop
bash install_packages.sh #Then press enter on your laptop
```
If the pip installation does not work, you can search forums by indicating the error message from your terminal, ask an AI for help, or, as a last resort, contact us.  

### 3.2 For Bioinformaticians

The NanoViZer folder does not need to be in the Documents folder; this is just to facilitate explanations. Choose your own method to install these requirements (e.g., pip, conda, etc.).
The install_packages.sh file allows you to download all the required packages through pip3.

## 4. Usage

After installing the requirements (see section 3), run the following command:
```bash
python3 NanoViZer.py
```
This kind of text should appear:
```bash
 * Serving Flask app 'test_api'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.140:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-194-444
```
Keep your Terminal application open to use NanoViZer.  
After that, open Google Chrome and go to this website:
```bash
https://nanovizer-aoz.piksail.com/
```
Indicate at least the File name (bam file), the name of your genome use for mapping and the size of your genome.  
Other parameters are optional.

## 5. Citation

