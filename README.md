<!-- Bandeau image -->
<p align="center">
  <img src="https://nanovizer-aoz.piksail.com/assets/nanovizer-light-theme.a92c964a.svg" alt="Bandeau" width="100%" />
</p>

<!-- NanoViZer -->
<h1 align="center"><strong>NanoViZer</strong></h1>

---

## 1. Introduction

*(Un petit texte qui explique en quelques lignes ce qu'est ton projet.)*

---

## 2. Requierement
- Python >= 3.7
- Flask
- flask-cors
- pysam

## 3. Installation
### 3.1 For non-bioinformaticians
#### 3.1.1. For Linux or MacOs user
In a first time download NanoViZer by clicking on the green button "<> Code" and by choosing "Download ZIP".  
Then unzip the file and move it on your Documents.  
Open the application Terminal already installed on your computer.  
Write these command lines to install requierements:  
```bash
cd Documents/NanoViZer/ #Then press enter on your laptop
chmod +x install_packages.sh #Then press enter on your laptop
bash install_packages.sh #Then press enter on your laptop
```
#### 3.1.2. For Windows user

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

