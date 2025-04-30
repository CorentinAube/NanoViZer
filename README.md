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
- **Broad Viral Family Compatibility:** Proven to work with multiple viral families, including HIV, SARS-CoV-2, HSV, and HDV.
- **User-Friendly Interface:** Simple command-line activation and web-browser-based analysis.
- **Data Privacy:** All data remains local and is never uploaded to an external server.
- **No Heavy Computational Requirements:** Only an internet connection is needed.

## Ease of Use

NanoViZer is designed to be user-friendly, requiring minimal computational expertise. After installing a few necessary tools, users can activate NanoViZer with a simple command-line interface. All subsequent analyses are conducted via a web browser, such as Google Chrome. Your data remains local and is never uploaded to an external server, ensuring data privacy and security. Only an internet connection is required to run NanoViZer effectively.

## Demonstration

NanoViZer has been successfully demonstrated to analyze data from various viral families, including:

- HIV
- SARS-CoV-2
- HSV
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
### 3.1 For non-bioinformaticians
If there are any issues, does not hesitate to contact us.

#### 3.1.1. For Linux or MacOS user
- In a first time download NanoViZer by clicking on the green button "<> Code" and by choosing "Download ZIP".  
- Then unzip the file and move it on your Documents.  
- Open the application Terminal already installed on your computer.  
- Write these command lines to install requierements if you are using MacOS Silicon:  
```bash
cd Documents/NanoViZer/ #Then press enter on your laptop
chmod +x install_packages.sh #Then press enter on your laptop
bash install_packages.sh #Then press enter on your laptop
```

#### 3.1.2. For Windows user
- Please first install WSL by finding any tutorial on the net.
- Navigate to ubuntu by tiping "pwd" to check your actual localisation in your Terminal application and "cd followin_folder" to go inside a folder that is inside your current folder.
Navigate to go inside of the NanoViZer folder and the write these following commande lines:
```bash
sudo apt update #Then press enter on your laptop and follow instructions
sudo apt install python3-pip #Then press enter on your laptop and follow instructions
cd Documents/NanoViZer/ #Then press enter on your laptop
chmod +x install_packages.sh #Then press enter on your laptop
bash install_packages.sh #Then press enter on your laptop
```

### 3.2 For bioinformaticians
NanoViZer folder does not need to be in the Documents folder, it is just to facilitate explanations.  
Choose your own way to install these requierements (pip, conda, ...). 

## 4. Usage
After have install requierements (section 3.), write the following command line:
```bash
python3 NanoViZer.py
```
This kind of text should be appear:
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
Keep your Terminal application open for use NanoViZer.  
After, open Google Chrome go to this website:
```bash
https://nanovizer-aoz.piksail.com/
```
Indicate at least the File name (bam file), the name of your genome use for the mapping and the size of your genome.  
Others parameters are optionnal.

## 5. Citation

