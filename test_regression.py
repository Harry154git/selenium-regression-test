import pytest
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# --- KONFIGURASI URL ---
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="function")
def driver():
    """Setup browser sebelum test dijalankan"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

def do_login(driver, email, password):
    """Fungsi helper untuk proses login berdasarkan login.blade.php"""
    driver.get(f"{BASE_URL}/login")
    
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "email").send_keys(email)
    
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

# ==============================================================================
# SKENARIO PENGUJIAN REGRESI (RG-01 - RG-20)
# ==============================================================================

def test_rg_01_login_pemilik_rumah(driver):
    """RG-01: Login sebagai Pemilik Rumah"""
    do_login(driver, "pemilik@example.com", "password")
    WebDriverWait(driver, 10).until(EC.url_contains("/pemilik/dashboard"))
    assert "/pemilik/dashboard" in driver.current_url

def test_rg_02_login_kontraktor(driver):
    """RG-02: Login sebagai Kontraktor"""
    do_login(driver, "kontraktor@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url

def test_rg_03_login_teknisi_lapangan(driver):
    """RG-03: Login sebagai Teknisi Lapangan"""
    do_login(driver, "teknisi@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url

def test_rg_04_login_petugas_lab(driver):
    """RG-04: Login sebagai Petugas Laboratorium"""
    do_login(driver, "lab@example.com", "password")
    WebDriverWait(driver, 10).until(EC.url_contains("/petugas_lab/dashboard"))
    assert "/petugas_lab/dashboard" in driver.current_url

import time

def test_rg_05_buat_proyek_baru(driver):
    """RG-05: Membuat proyek baru (Pemilik)"""
    do_login(driver, "pemilik@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/pemilik/dashboard"))
    
    driver.get(f"{BASE_URL}/pemilik/proyek/create")
    
    nama_proyek = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "nama_proyek")))
    lokasi = driver.find_element(By.NAME, "lokasi")
    
    driver.execute_script("arguments[0].value = 'Proyek Perumahan Mawar';", nama_proyek)
    driver.execute_script("arguments[0].value = 'Banjarmasin';", lokasi)
    
    simpan_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    driver.execute_script("arguments[0].click();", simpan_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("/pemilik/dashboard"))
    
    assert "Proyek Perumahan Mawar" in driver.page_source

def test_rg_06_ajukan_sondir(driver):
    """RG-06: Mengajukan pengujian Sondir (Kontraktor)"""
    do_login(driver, "kontraktor@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    driver.get(f"{BASE_URL}/kontraktor/pengajuan/buat")
    
    proyek_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "proyek_id")))
    Select(proyek_select).select_by_index(1)
    
    Select(driver.find_element(By.NAME, "jenis_pengujian")).select_by_value("Sondir")
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Ajukan Jadwal')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("/kontraktor/pengajuan"))

def test_rg_07_ajukan_boring(driver):
    """RG-07: Mengajukan pengujian Boring (Kontraktor)"""
    do_login(driver, "kontraktor@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    driver.get(f"{BASE_URL}/kontraktor/pengajuan/buat")
    
    proyek_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "proyek_id")))
    Select(proyek_select).select_by_index(1)
    
    Select(driver.find_element(By.NAME, "jenis_pengujian")).select_by_value("Boring")
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Ajukan Jadwal')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("/kontraktor/pengajuan"))

def test_rg_08_tentukan_titik_gps(driver):
    """RG-08: Menentukan titik GPS (Petugas Lapangan)"""
    do_login(driver, "petugas@example.com", "password")
    # Asumsikan ID SoilTest = 1
    driver.get(f"{BASE_URL}/petugas_lapangan/lokasi/1/buat")
    
    driver.find_element(By.NAME, "latitude").send_keys("-3.316694")
    driver.find_element(By.NAME, "longitude").send_keys("114.590111")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("/petugas_lapangan/lokasi"))
    assert "-3.316694" in driver.page_source

def test_rg_09_input_qc_fs(driver):
    """RG-09: Menginput nilai QC dan FS (Teknisi Sondir)"""
    do_login(driver, "teknisi@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    driver.get(f"{BASE_URL}/teknisi/sondir")
    
    try:
        input_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Input')]"))
        )
        driver.execute_script("arguments[0].click();", input_btn)
    except:
        pytest.fail("Tabel kosong! Pastikan seeder berstatus 'Terjadwal'.")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/input"))
    
    qc_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "nilai_qc")))
    fs_input = driver.find_element(By.NAME, "nilai_fs")
    
    driver.execute_script("arguments[0].value = '25';", qc_input)
    driver.execute_script("arguments[0].value = '120';", fs_input)
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Simpan Hasil Sondir')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("/teknisi/sondir"))

def test_rg_10_verifikasi_dan_upload_sertifikat(driver):
    """RG-10: Upload sertifikat (Petugas Lab)"""
    do_login(driver, "lab@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("petugas_lab") or EC.url_contains("dashboard"))
    
    driver.get(f"{BASE_URL}/lab/certificate/1/upload")
    
    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sertifikat_uji")))
    
    test_file_path = os.path.abspath("sertifikat_dummy.png")
    if not os.path.exists(test_file_path):
        # Ini adalah kode hex dari gambar PNG kosong ukuran 1x1 pixel
        png_content = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
        with open(test_file_path, "wb") as f:
            f.write(png_content)
            
    file_input.send_keys(test_file_path)
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Upload Sertifikat')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("petugas_lab"))

def test_rg_11_login_invalid(driver):
    """RG-11: Login dengan akun tidak valid"""
   
    do_login(driver, "salah_email@example.com", "password_salah")
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "bg-red-100")))
    error_msg = driver.find_element(By.CLASS_NAME, "bg-red-100").text
    
    assert "salah" in error_msg.lower() or "not match" in error_msg.lower() or "failed" in error_msg.lower()
    assert "/login" in driver.current_url

def test_rg_12_buat_proyek_kosong(driver):
    """RG-12: Membuat proyek tanpa mengisi data"""
    do_login(driver, "pemilik@example.com", "password")
    driver.get(f"{BASE_URL}/pemilik/proyek/create")
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    nama_field = driver.find_element(By.NAME, "nama_proyek")
    is_required = nama_field.get_attribute("required")
    assert is_required == "true" or "wajib diisi" in driver.page_source.lower()

def test_rg_13_ajukan_tanpa_jenis_pengujian(driver):
    """RG-13: Mengajukan pengujian tanpa memilih jenis"""
    do_login(driver, "kontraktor@example.com", "password")
    driver.get(f"{BASE_URL}/kontraktor/pengajuan/buat")
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    select_field = driver.find_element(By.NAME, "jenis_pengujian")
    assert select_field.get_attribute("required") == "true" or "pilih jenis" in driver.page_source.lower()

def test_rg_14_input_gps_tidak_valid(driver):
    """RG-14: Menginput koordinat GPS di luar rentang"""
    do_login(driver, "petugas@example.com", "password")
    driver.get(f"{BASE_URL}/petugas_lapangan/lokasi/1/buat")
    
    driver.find_element(By.NAME, "latitude").send_keys("900")
    driver.find_element(By.NAME, "longitude").send_keys("1000")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    assert "invalid" in driver.page_source.lower() or "di luar rentang" in driver.page_source.lower()

def test_rg_15_input_qc_fs_kosong(driver):
    """RG-15: Menginput QC dan FS kosong"""
    do_login(driver, "teknisi@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    driver.get(f"{BASE_URL}/teknisi/sondir/1/input")
    
    qc_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "nilai_qc")))
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Simpan Hasil Sondir')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    is_required = qc_field.get_attribute("required")
    assert is_required == "true" or "wajib diisi" in driver.page_source.lower()

def test_rg_16_upload_sertifikat_format_salah(driver):
    """RG-16: Upload sertifikat format tidak didukung (.exe)"""
    do_login(driver, "lab@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("petugas_lab") or EC.url_contains("dashboard"))
    
    driver.get(f"{BASE_URL}/lab/certificate/1/upload")
    
    file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "sertifikat_uji")))
    
    test_file_path = os.path.abspath("dummy_virus.exe")
    if not os.path.exists(test_file_path):
        with open(test_file_path, "w") as f:
            f.write("exe")
            
    file_input.send_keys(test_file_path)
    
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Upload Sertifikat')]")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "must be a file of type" in driver.page_source or "harus berupa file" in driver.page_source.lower() or "The sertifikat uji field must be a file" in driver.page_source

def test_rg_17_akses_dashboard_tanpa_hak_akses(driver):
    """RG-17: Mengakses dashboard tanpa hak akses role"""
    
    do_login(driver, "teknisi@example.com", "password")
    
    driver.get(f"{BASE_URL}/pemilik/dashboard")
    
    assert "403" in driver.page_source or "Unauthorized" in driver.page_source or "/pemilik/dashboard" not in driver.current_url

def test_rg_18_buka_notifikasi_kosong(driver):
    """RG-18: Membuka notifikasi yang tidak tersedia"""
    do_login(driver, "pemilik@example.com", "password")
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    driver.get(f"{BASE_URL}/pemilik/notifications")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    assert "tidak ada notifikasi" in driver.page_source.lower()

def test_rg_19_verifikasi_tanpa_hasil_pengujian(driver):
    """RG-19: Verifikasi tanpa hasil pengujian"""
    do_login(driver, "lab@example.com", "password")
    
    driver.get(f"{BASE_URL}/lab/certificate/99/upload")
    
    assert "belum diuji" in driver.page_source.lower() or "not allowed" in driver.page_source.lower() or "404" in driver.page_source

def test_rg_20_validasi_dashboard_monitoring_real_time(driver):
    """RG-20: Validasi Dashboard Monitoring Proyek Real-Time"""
    do_login(driver, "pemilik@example.com", "password")
    driver.get(f"{BASE_URL}/pemilik/dashboard")
    
    assert "Status" in driver.page_source
    
    logs = driver.get_log('browser')
    error_logs = [log for log in logs if log['level'] == 'SEVERE']
    
    assert len(error_logs) == 0