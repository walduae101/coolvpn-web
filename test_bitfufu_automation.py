#!/usr/bin/env python3
"""
سكريبت اختبار نظام مراقبة BitFuFu
"""

import sys
from bitfufu_whatsapp_automation import BitFuFuAutomation

def main():
    print("\n" + "=" * 60)
    print("اختبار نظام مراقبة BitFuFu")
    print("=" * 60 + "\n")
    
    # إنشاء النظام بدون إرسال WhatsApp
    automation = BitFuFuAutomation(whatsapp_group_name="")
    
    print("تشغيل العملية (بدون إرسال WhatsApp)...\n")
    
    # تشغيل المراحل بدون WhatsApp
    try:
        # المرحلة 1: جمع البيانات
        print("[1/3] جمع البيانات...")
        email_data = automation._collect_gmail_data()
        if not email_data:
            print("❌ فشل جمع البيانات")
            return False
        print("✓ تم جمع البيانات\n")
        
        # المرحلة 2: تحليل ROI
        print("[2/3] تحليل ROI...")
        if not automation._analyze_roi(email_data):
            print("❌ فشل تحليل ROI")
            return False
        print("✓ تم تحليل ROI\n")
        
        # المرحلة 3: إنشاء التقرير
        print("[3/3] إنشاء التقرير...")
        report_files = automation._generate_report()
        if not report_files:
            print("❌ فشل إنشاء التقرير")
            return False
        print("✓ تم إنشاء التقرير\n")
        
        # عرض النتائج
        print("=" * 60)
        print("النتائج:")
        print("=" * 60)
        print(f"التقرير Markdown: {report_files['markdown']}")
        print(f"التقرير PDF: {report_files['pdf']}")
        print(f"\nإجمالي الاستثمار: ${automation.analysis_data['total_investment']:.2f}")
        print(f"إجمالي العوائد: ${automation.analysis_data['total_returns']:.2f}")
        print(f"صافي الربح/الخسارة: ${automation.analysis_data['total_profit_loss']:.2f}")
        print(f"ROI الإجمالي: {automation.analysis_data['overall_roi']:.2f}%")
        print("=" * 60)
        
        # عرض رسالة WhatsApp
        print("\nرسالة WhatsApp المقترحة:")
        print("-" * 60)
        print(automation._create_whatsapp_message())
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("✅ تم الاختبار بنجاح!")
    else:
        print("❌ فشل الاختبار")
    print("=" * 60 + "\n")
    sys.exit(0 if success else 1)
