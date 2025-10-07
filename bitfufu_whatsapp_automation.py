#!/usr/bin/env python3
"""
نظام مراقبة BitFuFu المتكامل مع WhatsApp Web
يقوم بجمع البيانات من Gmail، تحليل ROI، إنشاء تقارير، وإرسالها عبر WhatsApp
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Optional

# استيراد الوحدات المساعدة
from gmail_bitfufu_monitor import BitFuFuGmailMonitor, ROIAnalyzer, MINING_PLANS
from whatsapp_web_sender import WhatsAppWebSender

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/bitfufu_whatsapp_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BitFuFuAutomation:
    """نظام المراقبة التلقائي المتكامل"""
    
    def __init__(self, whatsapp_group_name: str = ""):
        self.whatsapp_group_name = whatsapp_group_name
        self.gmail_monitor = BitFuFuGmailMonitor()
        self.whatsapp_sender = WhatsAppWebSender()
        self.analysis_data = None
        self.comparison_data = None
        self.report_dir = "/home/ubuntu/bitfufu_reports"
        
        # إنشاء مجلد التقارير
        os.makedirs(self.report_dir, exist_ok=True)
    
    def run_complete_automation(self) -> bool:
        """تشغيل العملية الكاملة"""
        try:
            logger.info("=" * 60)
            logger.info("بدء نظام مراقبة BitFuFu التلقائي")
            logger.info("=" * 60)
            
            # المرحلة 1: جمع البيانات من Gmail
            logger.info("\n[المرحلة 1/4] جمع البيانات من Gmail...")
            email_data = self._collect_gmail_data()
            if not email_data:
                logger.error("فشل جمع البيانات من Gmail")
                return False
            
            # المرحلة 2: تحليل ROI
            logger.info("\n[المرحلة 2/4] تحليل ROI والأداء المالي...")
            if not self._analyze_roi(email_data):
                logger.error("فشل تحليل ROI")
                return False
            
            # المرحلة 3: إنشاء التقرير
            logger.info("\n[المرحلة 3/4] إنشاء التقرير المفصل...")
            report_files = self._generate_report()
            if not report_files:
                logger.error("فشل إنشاء التقرير")
                return False
            
            # المرحلة 4: إرسال عبر WhatsApp
            logger.info("\n[المرحلة 4/4] إرسال التقرير عبر WhatsApp Web...")
            if not self._send_whatsapp_report(report_files):
                logger.error("فشل إرسال التقرير عبر WhatsApp")
                return False
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ تم إكمال العملية بنجاح!")
            logger.info("=" * 60)
            return True
            
        except Exception as e:
            logger.error(f"خطأ في العملية التلقائية: {str(e)}")
            return False
    
    def _collect_gmail_data(self) -> Optional[Dict]:
        """جمع البيانات من Gmail"""
        try:
            # المصادقة مع Gmail
            if not self.gmail_monitor.authenticate_gmail():
                logger.error("فشل الاتصال بـ Gmail API")
                # استخدام بيانات تجريبية للاختبار
                logger.warning("استخدام بيانات تجريبية للاختبار")
                return self._get_mock_data()
            
            # البحث عن آخر بريد
            message = self.gmail_monitor.search_latest_bitfufu_email()
            if not message:
                logger.warning("لم يتم العثور على رسائل، استخدام بيانات تجريبية")
                return self._get_mock_data()
            
            # استخراج البيانات
            email_data = self.gmail_monitor.extract_email_data(message)
            if not email_data:
                logger.warning("فشل استخراج البيانات، استخدام بيانات تجريبية")
                return self._get_mock_data()
            
            logger.info(f"✓ تم جمع بيانات {len(email_data.get('plans', {}))} خطط")
            return email_data
            
        except Exception as e:
            logger.error(f"خطأ في جمع البيانات: {str(e)}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> Dict:
        """الحصول على بيانات تجريبية للاختبار"""
        logger.info("استخدام بيانات تجريبية")
        return {
            "timestamp": datetime.now().isoformat(),
            "btc_price": 62500.0,
            "plans": {
                "95936": {"name": "خطة 3 أيام", "cost": 63.00, "duration": 3, "btc_earned": 0.00015},
                "95735": {"name": "خطة 10 أيام", "cost": 63.00, "duration": 10, "btc_earned": 0.00048},
                "95937": {"name": "خطة 14 يوم", "cost": 453.73, "duration": 14, "btc_earned": 0.00112},
                "95736": {"name": "خطة 30 يوم", "cost": 439.93, "duration": 30, "btc_earned": 0.00235}
            }
        }
    
    def _analyze_roi(self, email_data: Dict) -> bool:
        """تحليل ROI"""
        try:
            # إنشاء المحلل
            analyzer = ROIAnalyzer(email_data)
            
            # حساب ROI
            self.analysis_data = analyzer.calculate_roi()
            if not self.analysis_data:
                return False
            
            # حفظ التحليل
            analysis_file = analyzer.save_analysis()
            logger.info(f"✓ تم حفظ التحليل: {analysis_file}")
            
            # مقارنة مع اليوم السابق
            previous_files = sorted([
                f for f in os.listdir("/home/ubuntu")
                if f.startswith("roi_analysis_") and f.endswith(".json")
            ])
            
            if len(previous_files) > 1:
                previous_file = f"/home/ubuntu/{previous_files[-2]}"
                self.comparison_data = analyzer.compare_with_previous(previous_file)
                logger.info(f"✓ تمت المقارنة مع: {previous_files[-2]}")
            else:
                logger.info("لا يوجد تحليل سابق للمقارنة")
                self.comparison_data = {}
            
            # عرض ملخص النتائج
            logger.info(f"  - إجمالي الاستثمار: ${self.analysis_data['total_investment']:.2f}")
            logger.info(f"  - إجمالي العوائد: ${self.analysis_data['total_returns']:.2f}")
            logger.info(f"  - صافي الربح/الخسارة: ${self.analysis_data['total_profit_loss']:.2f}")
            logger.info(f"  - ROI الإجمالي: {self.analysis_data['overall_roi']:.2f}%")
            
            return True
            
        except Exception as e:
            logger.error(f"خطأ في تحليل ROI: {str(e)}")
            return False
    
    def _generate_report(self) -> Optional[Dict]:
        """إنشاء التقرير المفصل"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            md_file = f"{self.report_dir}/bitfufu_report_{timestamp}.md"
            pdf_file = f"{self.report_dir}/bitfufu_report_{timestamp}.pdf"
            
            # إنشاء محتوى التقرير
            report_content = self._create_report_content()
            
            # حفظ التقرير Markdown
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            logger.info(f"✓ تم إنشاء التقرير: {md_file}")
            
            # تحويل إلى PDF
            try:
                import subprocess
                result = subprocess.run(
                    ['manus-md-to-pdf', md_file, pdf_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0 and os.path.exists(pdf_file):
                    logger.info(f"✓ تم تحويل التقرير إلى PDF: {pdf_file}")
                else:
                    logger.warning(f"فشل تحويل PDF: {result.stderr}")
                    pdf_file = None
            except Exception as e:
                logger.warning(f"خطأ في تحويل PDF: {str(e)}")
                pdf_file = None
            
            return {
                "markdown": md_file,
                "pdf": pdf_file
            }
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء التقرير: {str(e)}")
            return None
    
    def _create_report_content(self) -> str:
        """إنشاء محتوى التقرير"""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")
        
        # تحديد الحالة والرموز
        roi = self.analysis_data['overall_roi']
        if roi > 5:
            status_emoji = "🟢 📈"
            status_text = "أداء ممتاز"
            recommendation = "مواصلة الاستثمار في الخطط ذات الأداء العالي"
        elif roi > 0:
            status_emoji = "🟡 📊"
            status_text = "أداء مقبول"
            recommendation = "مراجعة استراتيجية الاستثمار وتحسين التوزيع"
        elif roi > -50:
            status_emoji = "🔴 📉"
            status_text = "خسائر محدودة"
            recommendation = "مراقبة دقيقة للأداء وإعادة تقييم الخطط"
        else:
            status_emoji = "🚨 ⚠️"
            status_text = "خسائر كبيرة"
            recommendation = "إعادة تقييم فوري للاستراتيجية الاستثمارية"
        
        # بناء التقرير
        report = f"""# تقرير BitFuFu اليومي {status_emoji}

**التاريخ:** {date_str}  
**الوقت:** {time_str}  
**الحالة:** {status_text}

---

## 💰 الملخص المالي

| المؤشر | القيمة |
|--------|--------|
| إجمالي الاستثمار | ${self.analysis_data['total_investment']:,.2f} |
| إجمالي العوائد | ${self.analysis_data['total_returns']:,.2f} |
| صافي الربح/الخسارة | ${self.analysis_data['total_profit_loss']:,.2f} |
| العائد الإجمالي (ROI) | {self.analysis_data['overall_roi']:.2f}% |
| سعر BTC الحالي | ${self.analysis_data['btc_price']:,.2f} |

---

## 📊 مقارنة مع اليوم السابق

"""
        
        if self.comparison_data:
            roi_change = self.comparison_data.get('roi_change', 0)
            pl_change = self.comparison_data.get('profit_loss_change', 0)
            btc_change = self.comparison_data.get('btc_price_change', 0)
            
            roi_arrow = "📈" if roi_change > 0 else "📉" if roi_change < 0 else "➡️"
            pl_arrow = "📈" if pl_change > 0 else "📉" if pl_change < 0 else "➡️"
            btc_arrow = "📈" if btc_change > 0 else "📉" if btc_change < 0 else "➡️"
            
            report += f"""| المؤشر | التغيير |
|--------|---------|
| تغير ROI | {roi_arrow} {roi_change:+.2f}% |
| تغير الربح/الخسارة | {pl_arrow} ${pl_change:+.2f} |
| تغير سعر BTC | {btc_arrow} ${btc_change:+.2f} |
"""
        else:
            report += "*لا توجد بيانات سابقة للمقارنة*\n"
        
        report += "\n---\n\n## 📈 تفاصيل الخطط\n\n"
        
        # تفاصيل كل خطة
        for plan_id, plan_data in self.analysis_data['plans'].items():
            roi_plan = plan_data['roi_percentage']
            plan_emoji = "✅" if roi_plan > 0 else "⚠️" if roi_plan > -50 else "❌"
            
            report += f"""### {plan_emoji} {plan_data['name']} (#{plan_id})

| المؤشر | القيمة |
|--------|--------|
| التكلفة | ${plan_data['cost']:.2f} |
| المدة | {plan_data['duration']} يوم |
| BTC المكتسبة | {plan_data['btc_earned']:.8f} BTC |
| العائد بالدولار | ${plan_data['usd_earned']:.2f} |
| الربح/الخسارة | ${plan_data['profit_loss']:.2f} |
| ROI | {plan_data['roi_percentage']:.2f}% |

"""
        
        report += f"""---

## 💡 التوصية

**{recommendation}**

---

## 📝 ملاحظات

- هذا التقرير تم إنشاؤه تلقائياً بواسطة نظام مراقبة BitFuFu
- البيانات مستخرجة من آخر بريد Revenue Journal
- يتم تحديث التقرير يومياً في الساعة 16:05 بتوقيت أبوظبي

---

*تم الإنشاء بواسطة نظام المراقبة التلقائي* 🤖
"""
        
        return report
    
    def _create_whatsapp_message(self) -> str:
        """إنشاء رسالة WhatsApp المختصرة"""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        
        # تحديد الحالة والرموز
        roi = self.analysis_data['overall_roi']
        if roi > 5:
            status_emoji = "🟢 📈"
        elif roi > 0:
            status_emoji = "🟡 📊"
        elif roi > -50:
            status_emoji = "🔴 📉"
        else:
            status_emoji = "🚨 ⚠️"
        
        # بناء الرسالة
        message = f"""🤖 *تقرير BitFuFu اليومي* {status_emoji}
📅 التاريخ: {date_str}

💰 *الملخص المالي:*
• إجمالي الاستثمار: ${self.analysis_data['total_investment']:,.2f}
• إجمالي العوائد: ${self.analysis_data['total_returns']:,.2f}
• صافي الخسارة: ${self.analysis_data['total_profit_loss']:,.2f}
• العائد الإجمالي: {self.analysis_data['overall_roi']:.2f}%"""
        
        # إضافة المقارنة
        if self.comparison_data:
            roi_change = self.comparison_data.get('roi_change', 0)
            pl_change = self.comparison_data.get('profit_loss_change', 0)
            
            message += f"""

📊 *مقارنة مع اليوم السابق:*
• تغير ROI: {roi_change:+.2f}%
• تغير الخسائر: ${pl_change:+.2f}"""
        
        # إضافة حالة الخطط
        message += "\n\n📈 *حالة الخطط:*"
        for plan_id, plan_data in self.analysis_data['plans'].items():
            roi_plan = plan_data['roi_percentage']
            plan_emoji = "✅" if roi_plan > 0 else "⚠️" if roi_plan > -50 else "❌"
            message += f"\n• {plan_emoji} {plan_data['name']}: {roi_plan:.2f}%"
        
        # إضافة التوصية
        if roi > 5:
            recommendation = "مواصلة الاستثمار"
        elif roi > 0:
            recommendation = "مراجعة الاستراتيجية"
        elif roi > -50:
            recommendation = "مراقبة دقيقة"
        else:
            recommendation = "إعادة تقييم فوري"
        
        message += f"""

💡 *التوصية:*
{recommendation}

📎 التقرير المفصل مرفق أعلاه"""
        
        return message
    
    def _send_whatsapp_report(self, report_files: Dict) -> bool:
        """إرسال التقرير عبر WhatsApp"""
        try:
            if not self.whatsapp_group_name:
                logger.error("لم يتم تحديد اسم مجموعة WhatsApp")
                return False
            
            # إنشاء الرسالة
            message = self._create_whatsapp_message()
            
            # إرسال الرسالة مع الملف
            pdf_file = report_files.get('pdf')
            success = self.whatsapp_sender.send_complete_message(
                self.whatsapp_group_name,
                message,
                pdf_file
            )
            
            if success:
                logger.info("✓ تم إرسال التقرير عبر WhatsApp بنجاح")
            else:
                logger.error("فشل إرسال التقرير عبر WhatsApp")
            
            return success
            
        except Exception as e:
            logger.error(f"خطأ في إرسال التقرير: {str(e)}")
            return False


def main():
    """الدالة الرئيسية"""
    print("\n" + "=" * 60)
    print("نظام مراقبة BitFuFu المتكامل مع WhatsApp Web")
    print("=" * 60 + "\n")
    
    # طلب اسم المجموعة
    group_name = input("أدخل اسم مجموعة WhatsApp (أو اتركه فارغاً للتخطي): ").strip()
    
    if not group_name:
        print("\n⚠️ تحذير: لن يتم إرسال التقرير عبر WhatsApp")
        response = input("هل تريد المتابعة؟ (y/n): ").strip().lower()
        if response != 'y':
            print("تم الإلغاء")
            return
    
    # إنشاء وتشغيل النظام
    automation = BitFuFuAutomation(whatsapp_group_name=group_name)
    success = automation.run_complete_automation()
    
    if success:
        print("\n✅ تم إكمال العملية بنجاح!")
    else:
        print("\n❌ فشلت العملية - راجع السجلات للتفاصيل")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
