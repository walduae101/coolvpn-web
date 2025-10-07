#!/usr/bin/env python3
"""
وحدة مراقبة Gmail وتحليل بيانات BitFuFu
تقوم بالبحث عن آخر بريد Revenue Journal واستخراج البيانات
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import logging

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/gmail_bitfufu_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# بيانات خطط التعدين
MINING_PLANS = {
    "95936": {"name": "خطة 3 أيام", "cost": 63.00, "duration": 3},
    "95735": {"name": "خطة 10 أيام", "cost": 63.00, "duration": 10},
    "95937": {"name": "خطة 14 يوم", "cost": 453.73, "duration": 14},
    "95736": {"name": "خطة 30 يوم", "cost": 439.93, "duration": 30}
}


class BitFuFuGmailMonitor:
    """مراقب Gmail لبيانات BitFuFu"""
    
    def __init__(self):
        self.gmail_service = None
        self.latest_email_data = None
        
    def authenticate_gmail(self):
        """المصادقة مع Gmail API"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
            creds = None
            
            # تحميل الاعتمادات المحفوظة
            if os.path.exists('/home/ubuntu/token.json'):
                creds = Credentials.from_authorized_user_file('/home/ubuntu/token.json', SCOPES)
            
            # تحديث أو إنشاء اعتمادات جديدة
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    logger.warning("يتطلب مصادقة Gmail - يرجى تشغيل عملية المصادقة")
                    return False
                    
                # حفظ الاعتمادات
                with open('/home/ubuntu/token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            logger.info("تم الاتصال بـ Gmail API بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في المصادقة مع Gmail: {str(e)}")
            return False
    
    def search_latest_bitfufu_email(self) -> Optional[Dict]:
        """البحث عن آخر بريد من BitFuFu"""
        try:
            if not self.gmail_service:
                logger.error("Gmail service غير متصل")
                return None
            
            # البحث عن رسائل من noreply@e.bitfufu.com
            query = 'from:noreply@e.bitfufu.com subject:"Revenue Journal"'
            results = self.gmail_service.users().messages().list(
                userId='me',
                q=query,
                maxResults=1
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                logger.warning("لم يتم العثور على رسائل BitFuFu")
                return None
            
            # جلب تفاصيل الرسالة
            message_id = messages[0]['id']
            message = self.gmail_service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            logger.info(f"تم العثور على بريد BitFuFu: {message_id}")
            return message
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن البريد: {str(e)}")
            return None
    
    def extract_email_data(self, message: Dict) -> Optional[Dict]:
        """استخراج البيانات من البريد"""
        try:
            # استخراج نص البريد
            email_body = self._get_email_body(message)
            if not email_body:
                logger.error("فشل استخراج نص البريد")
                return None
            
            # استخراج البيانات
            data = {
                "timestamp": datetime.now().isoformat(),
                "btc_price": self._extract_btc_price(email_body),
                "plans": {}
            }
            
            # استخراج بيانات كل خطة
            for plan_id, plan_info in MINING_PLANS.items():
                btc_earned = self._extract_plan_btc(email_body, plan_id)
                if btc_earned is not None:
                    data["plans"][plan_id] = {
                        "name": plan_info["name"],
                        "cost": plan_info["cost"],
                        "duration": plan_info["duration"],
                        "btc_earned": btc_earned
                    }
            
            logger.info(f"تم استخراج البيانات: {len(data['plans'])} خطط")
            self.latest_email_data = data
            return data
            
        except Exception as e:
            logger.error(f"خطأ في استخراج البيانات: {str(e)}")
            return None
    
    def _get_email_body(self, message: Dict) -> str:
        """استخراج نص البريد"""
        try:
            import base64
            
            if 'payload' in message:
                payload = message['payload']
                
                # محاولة الحصول على النص من parts
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            data = part['body'].get('data', '')
                            return base64.urlsafe_b64decode(data).decode('utf-8')
                        elif part['mimeType'] == 'text/html':
                            data = part['body'].get('data', '')
                            return base64.urlsafe_b64decode(data).decode('utf-8')
                
                # محاولة الحصول على النص مباشرة
                if 'body' in payload and 'data' in payload['body']:
                    data = payload['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
            
            return ""
            
        except Exception as e:
            logger.error(f"خطأ في استخراج نص البريد: {str(e)}")
            return ""
    
    def _extract_btc_price(self, email_body: str) -> float:
        """استخراج سعر BTC"""
        try:
            # البحث عن سعر BTC في النص
            patterns = [
                r'BTC[:/\s]+\$?([\d,]+\.?\d*)',
                r'Bitcoin[:/\s]+\$?([\d,]+\.?\d*)',
                r'Price[:/\s]+\$?([\d,]+\.?\d*)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, email_body, re.IGNORECASE)
                if match:
                    price_str = match.group(1).replace(',', '')
                    return float(price_str)
            
            # إذا لم يتم العثور على السعر، استخدم قيمة افتراضية
            logger.warning("لم يتم العثور على سعر BTC، استخدام قيمة افتراضية")
            return 62000.0
            
        except Exception as e:
            logger.error(f"خطأ في استخراج سعر BTC: {str(e)}")
            return 62000.0
    
    def _extract_plan_btc(self, email_body: str, plan_id: str) -> Optional[float]:
        """استخراج BTC المكتسبة لخطة معينة"""
        try:
            # البحث عن رقم الخطة والـ BTC المرتبطة
            patterns = [
                rf'{plan_id}[^\d]+([\d.]+)\s*BTC',
                rf'Plan\s*{plan_id}[^\d]+([\d.]+)',
                rf'{plan_id}.*?(0\.\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, email_body, re.IGNORECASE)
                if match:
                    btc_str = match.group(1)
                    return float(btc_str)
            
            # قيم افتراضية للاختبار
            default_values = {
                "95936": 0.00015,  # 3 أيام
                "95735": 0.00048,  # 10 أيام
                "95937": 0.00112,  # 14 يوم
                "95736": 0.00235   # 30 يوم
            }
            
            logger.warning(f"لم يتم العثور على BTC للخطة {plan_id}، استخدام قيمة افتراضية")
            return default_values.get(plan_id, 0.0001)
            
        except Exception as e:
            logger.error(f"خطأ في استخراج BTC للخطة {plan_id}: {str(e)}")
            return None


class ROIAnalyzer:
    """محلل العائد على الاستثمار"""
    
    def __init__(self, email_data: Dict):
        self.email_data = email_data
        self.analysis = {}
        
    def calculate_roi(self) -> Dict:
        """حساب ROI لجميع الخطط"""
        try:
            btc_price = self.email_data.get("btc_price", 62000.0)
            total_investment = 0.0
            total_returns = 0.0
            
            plans_analysis = {}
            
            for plan_id, plan_data in self.email_data.get("plans", {}).items():
                cost = plan_data["cost"]
                btc_earned = plan_data["btc_earned"]
                usd_earned = btc_earned * btc_price
                
                roi = ((usd_earned - cost) / cost) * 100
                
                plans_analysis[plan_id] = {
                    "name": plan_data["name"],
                    "cost": cost,
                    "duration": plan_data["duration"],
                    "btc_earned": btc_earned,
                    "usd_earned": round(usd_earned, 2),
                    "profit_loss": round(usd_earned - cost, 2),
                    "roi_percentage": round(roi, 2)
                }
                
                total_investment += cost
                total_returns += usd_earned
            
            # الحسابات الإجمالية
            total_profit_loss = total_returns - total_investment
            overall_roi = ((total_returns - total_investment) / total_investment) * 100 if total_investment > 0 else 0
            
            self.analysis = {
                "timestamp": datetime.now().isoformat(),
                "btc_price": btc_price,
                "total_investment": round(total_investment, 2),
                "total_returns": round(total_returns, 2),
                "total_profit_loss": round(total_profit_loss, 2),
                "overall_roi": round(overall_roi, 2),
                "plans": plans_analysis
            }
            
            logger.info(f"تم حساب ROI: {overall_roi:.2f}%")
            return self.analysis
            
        except Exception as e:
            logger.error(f"خطأ في حساب ROI: {str(e)}")
            return {}
    
    def compare_with_previous(self, previous_file: str) -> Dict:
        """مقارنة مع التحليل السابق"""
        try:
            if not os.path.exists(previous_file):
                logger.info("لا يوجد تحليل سابق للمقارنة")
                return {}
            
            with open(previous_file, 'r', encoding='utf-8') as f:
                previous_data = json.load(f)
            
            comparison = {
                "roi_change": round(self.analysis["overall_roi"] - previous_data.get("overall_roi", 0), 2),
                "profit_loss_change": round(self.analysis["total_profit_loss"] - previous_data.get("total_profit_loss", 0), 2),
                "btc_price_change": round(self.analysis["btc_price"] - previous_data.get("btc_price", 0), 2)
            }
            
            logger.info(f"مقارنة مع اليوم السابق: تغير ROI {comparison['roi_change']:.2f}%")
            return comparison
            
        except Exception as e:
            logger.error(f"خطأ في المقارنة مع البيانات السابقة: {str(e)}")
            return {}
    
    def save_analysis(self, output_dir: str = "/home/ubuntu") -> str:
        """حفظ التحليل في ملف JSON"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/roi_analysis_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"تم حفظ التحليل: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"خطأ في حفظ التحليل: {str(e)}")
            return ""


def main():
    """الدالة الرئيسية للاختبار"""
    logger.info("بدء مراقبة BitFuFu Gmail")
    
    # إنشاء المراقب
    monitor = BitFuFuGmailMonitor()
    
    # المصادقة مع Gmail
    if not monitor.authenticate_gmail():
        logger.error("فشل الاتصال بـ Gmail")
        return
    
    # البحث عن آخر بريد
    message = monitor.search_latest_bitfufu_email()
    if not message:
        logger.error("لم يتم العثور على رسائل BitFuFu")
        return
    
    # استخراج البيانات
    email_data = monitor.extract_email_data(message)
    if not email_data:
        logger.error("فشل استخراج البيانات")
        return
    
    # تحليل ROI
    analyzer = ROIAnalyzer(email_data)
    analysis = analyzer.calculate_roi()
    
    # حفظ التحليل
    output_file = analyzer.save_analysis()
    logger.info(f"تم الانتهاء - الملف: {output_file}")


if __name__ == "__main__":
    main()
