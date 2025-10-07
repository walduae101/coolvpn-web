#!/usr/bin/env python3
"""
وحدة إرسال الرسائل عبر WhatsApp Web باستخدام Selenium
"""

import os
import time
import json
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/whatsapp_web.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WhatsAppWebSender:
    """مرسل رسائل WhatsApp Web"""
    
    def __init__(self, profile_dir: str = "/home/ubuntu/.chrome_whatsapp_profile"):
        self.profile_dir = profile_dir
        self.driver = None
        self.config_file = "/home/ubuntu/whatsapp_config.json"
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """تحميل إعدادات WhatsApp"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"خطأ في تحميل الإعدادات: {str(e)}")
            return {}
    
    def _save_config(self):
        """حفظ إعدادات WhatsApp"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطأ في حفظ الإعدادات: {str(e)}")
    
    def initialize_browser(self, headless: bool = False) -> bool:
        """تهيئة متصفح Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument(f"--user-data-dir={self.profile_dir}")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            if headless:
                chrome_options.add_argument("--headless=new")
            
            # تثبيت ChromeDriver تلقائياً
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("تم تهيئة المتصفح بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تهيئة المتصفح: {str(e)}")
            return False
    
    def open_whatsapp_web(self, wait_for_login: bool = True) -> bool:
        """فتح WhatsApp Web"""
        try:
            if not self.driver:
                logger.error("المتصفح غير مهيأ")
                return False
            
            logger.info("فتح WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            if wait_for_login:
                # انتظار تحميل WhatsApp Web
                logger.info("انتظار تحميل WhatsApp Web...")
                time.sleep(10)
                
                # التحقق من تسجيل الدخول
                try:
                    # البحث عن عنصر يدل على تسجيل الدخول
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                    )
                    logger.info("تم تسجيل الدخول بنجاح")
                    return True
                except:
                    logger.warning("قد تحتاج إلى مسح QR Code")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"خطأ في فتح WhatsApp Web: {str(e)}")
            return False
    
    def search_contact(self, contact_name: str) -> bool:
        """البحث عن جهة اتصال أو مجموعة"""
        try:
            logger.info(f"البحث عن: {contact_name}")
            
            # البحث عن مربع البحث
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            
            # مسح البحث السابق
            search_box.clear()
            time.sleep(1)
            
            # كتابة اسم الجهة
            search_box.send_keys(contact_name)
            time.sleep(2)
            
            # النقر على النتيجة الأولى
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{contact_name}"]'))
            )
            first_result.click()
            time.sleep(2)
            
            logger.info(f"تم فتح المحادثة مع: {contact_name}")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن الجهة: {str(e)}")
            return False
    
    def send_message(self, message: str) -> bool:
        """إرسال رسالة نصية"""
        try:
            logger.info("إرسال الرسالة...")
            
            # البحث عن مربع الرسالة
            message_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # تقسيم الرسالة إلى أسطر وإرسالها
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    # استخدام Shift+Enter للسطر الجديد
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
            
            time.sleep(1)
            
            # إرسال الرسالة
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)
            
            logger.info("تم إرسال الرسالة بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرسال الرسالة: {str(e)}")
            return False
    
    def attach_file(self, file_path: str) -> bool:
        """إرفاق ملف"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"الملف غير موجود: {file_path}")
                return False
            
            logger.info(f"إرفاق الملف: {file_path}")
            
            # النقر على زر الإرفاق
            attach_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
            )
            attach_button.click()
            time.sleep(1)
            
            # اختيار "Document"
            document_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
            )
            document_button.send_keys(os.path.abspath(file_path))
            time.sleep(3)
            
            # النقر على زر الإرسال
            send_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            time.sleep(3)
            
            logger.info("تم إرفاق وإرسال الملف بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرفاق الملف: {str(e)}")
            return False
    
    def close_browser(self):
        """إغلاق المتصفح"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("تم إغلاق المتصفح")
        except Exception as e:
            logger.error(f"خطأ في إغلاق المتصفح: {str(e)}")
    
    def send_complete_message(self, contact_name: str, message: str, 
                            pdf_file: Optional[str] = None) -> bool:
        """إرسال رسالة كاملة مع ملف PDF اختياري"""
        try:
            # تهيئة المتصفح
            if not self.initialize_browser(headless=False):
                return False
            
            # فتح WhatsApp Web
            if not self.open_whatsapp_web():
                logger.error("فشل فتح WhatsApp Web")
                self.close_browser()
                return False
            
            # البحث عن الجهة
            if not self.search_contact(contact_name):
                logger.error(f"فشل البحث عن: {contact_name}")
                self.close_browser()
                return False
            
            # إرفاق الملف أولاً إذا كان موجوداً
            if pdf_file and os.path.exists(pdf_file):
                if not self.attach_file(pdf_file):
                    logger.warning("فشل إرفاق الملف، سيتم إرسال الرسالة فقط")
            
            # إرسال الرسالة
            if not self.send_message(message):
                logger.error("فشل إرسال الرسالة")
                self.close_browser()
                return False
            
            # إغلاق المتصفح
            self.close_browser()
            
            logger.info("تم إرسال الرسالة الكاملة بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إرسال الرسالة الكاملة: {str(e)}")
            self.close_browser()
            return False


def main():
    """الدالة الرئيسية للاختبار"""
    logger.info("اختبار إرسال WhatsApp Web")
    
    sender = WhatsAppWebSender()
    
    # رسالة اختبار
    test_message = """🤖 *اختبار نظام BitFuFu*
📅 التاريخ: 07/10/2025

هذه رسالة اختبارية من نظام المراقبة التلقائية."""
    
    # إرسال الرسالة (يتطلب اسم المجموعة)
    contact_name = input("أدخل اسم المجموعة أو الجهة: ")
    sender.send_complete_message(contact_name, test_message)


if __name__ == "__main__":
    main()
