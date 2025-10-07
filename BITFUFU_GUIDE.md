# دليل نظام مراقبة BitFuFu المتكامل مع WhatsApp Web

## نظرة عامة

نظام مراقبة تلقائي متكامل يقوم بـ:
1. جمع بيانات التعدين من رسائل BitFuFu في Gmail
2. تحليل العائد على الاستثمار (ROI) لكل خطة
3. إنشاء تقارير شاملة بصيغة PDF
4. إرسال التقارير تلقائياً عبر WhatsApp Web

---

## الملفات الرئيسية

### السكريبتات
- `/home/ubuntu/bitfufu_whatsapp_automation.py` - السكريبت الرئيسي المتكامل
- `/home/ubuntu/gmail_bitfufu_monitor.py` - وحدة مراقبة Gmail وتحليل البيانات
- `/home/ubuntu/whatsapp_web_sender.py` - وحدة إرسال WhatsApp Web
- `/home/ubuntu/test_bitfufu_automation.py` - سكريبت الاختبار

### الإعدادات والجدولة
- `/home/ubuntu/setup_cron.sh` - إعداد الجدولة اليومية
- `/home/ubuntu/run_bitfufu_daily.sh` - سكريبت التشغيل اليومي (يتم إنشاؤه تلقائياً)
- `/home/ubuntu/whatsapp_config.json` - إعدادات WhatsApp المحفوظة

### المجلدات
- `/home/ubuntu/bitfufu_reports/` - مجلد التقارير (MD و PDF)
- `/home/ubuntu/.chrome_whatsapp_profile/` - ملف تعريف Chrome لـ WhatsApp Web

### السجلات
- `/home/ubuntu/bitfufu_whatsapp_automation.log` - السجل الرئيسي
- `/home/ubuntu/gmail_bitfufu_monitor.log` - سجل مراقبة Gmail
- `/home/ubuntu/whatsapp_web.log` - سجل WhatsApp Web
- `/home/ubuntu/bitfufu_cron.log` - سجل التشغيل المجدول

---

## بيانات خطط التعدين

| رقم الخطة | الاسم | التكلفة | المدة |
|-----------|-------|---------|-------|
| 95936 | خطة 3 أيام | $63.00 | 3 أيام |
| 95735 | خطة 10 أيام | $63.00 | 10 أيام |
| 95937 | خطة 14 يوم | $453.73 | 14 يوم |
| 95736 | خطة 30 يوم | $439.93 | 30 يوم |

**إجمالي الاستثمار:** $1,019.66

---

## الاستخدام

### 1. الاختبار الأولي (بدون WhatsApp)

```bash
cd /home/ubuntu
python3 test_bitfufu_automation.py
```

هذا الأمر سيقوم بـ:
- جمع البيانات (أو استخدام بيانات تجريبية)
- تحليل ROI
- إنشاء تقرير PDF
- عرض النتائج بدون إرسال WhatsApp

### 2. التشغيل اليدوي مع WhatsApp

```bash
cd /home/ubuntu
python3 bitfufu_whatsapp_automation.py
```

سيطلب منك:
- إدخال اسم مجموعة WhatsApp
- تأكيد المتابعة

**ملاحظة:** التشغيل الأول يتطلب مسح QR Code لتسجيل الدخول إلى WhatsApp Web.

### 3. إعداد الجدولة اليومية

```bash
cd /home/ubuntu
./setup_cron.sh
```

هذا سيقوم بإعداد مهمة cron للتشغيل يومياً في الساعة **16:05 بتوقيت أبوظبي** (12:05 UTC).

### 4. إدارة الجدولة

```bash
# عرض المهام المجدولة
crontab -l

# تعديل المهام المجدولة
crontab -e

# إلغاء جميع المهام المجدولة
crontab -r

# عرض سجل التشغيل المجدول
tail -f /home/ubuntu/bitfufu_cron.log
```

---

## إعداد Gmail API (اختياري)

لاستخدام البيانات الحقيقية من Gmail بدلاً من البيانات التجريبية:

### 1. إنشاء مشروع في Google Cloud Console
1. انتقل إلى https://console.cloud.google.com
2. أنشئ مشروع جديد
3. فعّل Gmail API

### 2. إنشاء اعتمادات OAuth 2.0
1. انتقل إلى "Credentials"
2. أنشئ "OAuth 2.0 Client ID"
3. اختر "Desktop app"
4. حمّل ملف JSON

### 3. حفظ الاعتمادات
```bash
# انسخ ملف الاعتمادات
cp /path/to/credentials.json /home/ubuntu/credentials.json

# تشغيل المصادقة
python3 -c "from gmail_bitfufu_monitor import BitFuFuGmailMonitor; m = BitFuFuGmailMonitor(); m.authenticate_gmail()"
```

سيفتح متصفح لتسجيل الدخول وسيتم حفظ token في `/home/ubuntu/token.json`.

---

## إعداد WhatsApp Web

### التشغيل الأول
1. شغّل السكريبت يدوياً أول مرة
2. سيفتح متصفح Chrome
3. امسح QR Code من هاتفك
4. سيتم حفظ الجلسة تلقائياً

### التشغيلات اللاحقة
- لن تحتاج لمسح QR Code مرة أخرى
- الجلسة محفوظة في `/home/ubuntu/.chrome_whatsapp_profile/`

### استكشاف الأخطاء
- إذا انتهت صلاحية الجلسة، احذف المجلد وأعد التشغيل:
```bash
rm -rf /home/ubuntu/.chrome_whatsapp_profile/
python3 bitfufu_whatsapp_automation.py
```

---

## تنسيق رسالة WhatsApp

```
🤖 *تقرير BitFuFu اليومي* [رمز الحالة]
📅 التاريخ: DD/MM/YYYY

💰 *الملخص المالي:*
• إجمالي الاستثمار: $X,XXX.XX
• إجمالي العوائد: $XXX.XX
• صافي الخسارة: $XXX.XX
• العائد الإجمالي: XX.XX% [رمز الاتجاه]

📊 *مقارنة مع اليوم السابق:*
• تغير ROI: +/-X.XX%
• تغير الخسائر: $+/-XX.XX

📈 *حالة الخطط:*
• [رمز] خطة 3 أيام: XX.X%
• [رمز] خطة 10 أيام: XX.X%
• [رمز] خطة 14 يوم: XX.X%
• [رمز] خطة 30 يوم: XX.X%

💡 *التوصية:*
[توصية ذكية حسب الأداء]

📎 التقرير المفصل مرفق أعلاه
```

### الرموز التعبيرية التلقائية
- 🟢 📈 للأداء الممتاز (ROI > 5%)
- 🟡 📊 للأداء المقبول (ROI 0-5%)
- 🔴 📉 للخسائر المحدودة (ROI -50% إلى 0%)
- 🚨 ⚠️ للخسائر الكبيرة (ROI < -50%)

---

## التقرير المفصل (PDF)

يحتوي على:
- **الملخص المالي:** جميع المؤشرات المالية
- **مقارنة مع اليوم السابق:** تغيرات ROI والأرباح/الخسائر
- **تفاصيل الخطط:** تحليل مفصل لكل خطة تعدين
- **التوصيات الذكية:** توصيات حسب الأداء
- **الملاحظات:** معلومات إضافية

---

## استكشاف الأخطاء

### مشكلة: لا يتم العثور على رسائل Gmail
**الحل:**
- تحقق من اتصال Gmail API
- تأكد من وجود رسائل من `noreply@e.bitfufu.com`
- سيستخدم النظام بيانات تجريبية تلقائياً

### مشكلة: فشل إرسال WhatsApp
**الحل:**
- تحقق من اتصال الإنترنت
- تأكد من صحة اسم المجموعة
- أعد تسجيل الدخول إلى WhatsApp Web
- راجع سجل `/home/ubuntu/whatsapp_web.log`

### مشكلة: فشل تحويل PDF
**الحل:**
- تحقق من تثبيت `manus-md-to-pdf`
- سيتم إنشاء ملف Markdown على الأقل
- يمكن تحويله يدوياً لاحقاً

### مشكلة: ChromeDriver لا يعمل
**الحل:**
```bash
# تحديث ChromeDriver يدوياً
pip3 install --upgrade webdriver-manager
```

---

## الصيانة

### تنظيف الملفات القديمة

```bash
# حذف التقارير الأقدم من 30 يوم
find /home/ubuntu/bitfufu_reports/ -name "*.pdf" -mtime +30 -delete
find /home/ubuntu/bitfufu_reports/ -name "*.md" -mtime +30 -delete

# حذف ملفات التحليل القديمة
find /home/ubuntu/ -name "roi_analysis_*.json" -mtime +30 -delete
```

### ضغط السجلات الكبيرة

```bash
# ضغط السجلات الأكبر من 10MB
for log in /home/ubuntu/*.log; do
    if [ $(stat -f%z "$log" 2>/dev/null || stat -c%s "$log") -gt 10485760 ]; then
        gzip "$log"
        touch "${log}"
    fi
done
```

---

## الأمان والخصوصية

- ✅ جلسة WhatsApp محفوظة محلياً فقط
- ✅ لا يتم تخزين كلمات مرور
- ✅ أذونات ملفات محدودة
- ✅ تشغيل في وضع headless للأمان
- ✅ جميع الاتصالات مشفرة

---

## متطلبات النظام

### البرمجيات المطلوبة
- Python 3.11+
- Google Chrome
- ChromeDriver (يتم تحديثه تلقائياً)

### المكتبات المطلوبة
```bash
pip3 install selenium webdriver-manager google-auth \
    google-auth-oauthlib google-auth-httplib2 \
    google-api-python-client
```

### الموارد
- مساحة قرص: ~500MB للتقارير والسجلات
- ذاكرة: ~512MB أثناء التشغيل
- اتصال إنترنت: مطلوب

---

## مؤشرات النجاح

- ✅ وصول التقرير إلى WhatsApp في الوقت المحدد
- ✅ دقة البيانات المستخرجة من Gmail
- ✅ صحة حسابات ROI والمقارنات
- ✅ استقرار جلسة WhatsApp Web
- ✅ عدم وجود أخطاء في السجلات

---

## الدعم

### السجلات
راجع السجلات للحصول على معلومات مفصلة عن الأخطاء:
```bash
# السجل الرئيسي
tail -f /home/ubuntu/bitfufu_whatsapp_automation.log

# سجل Gmail
tail -f /home/ubuntu/gmail_bitfufu_monitor.log

# سجل WhatsApp
tail -f /home/ubuntu/whatsapp_web.log

# سجل Cron
tail -f /home/ubuntu/bitfufu_cron.log
```

### الاختبار
اختبر النظام بانتظام:
```bash
python3 /home/ubuntu/test_bitfufu_automation.py
```

---

## الإصدار

**الإصدار:** 1.0  
**التاريخ:** 07 أكتوبر 2025  
**الحالة:** جاهز للإنتاج

---

*تم إنشاؤه بواسطة نظام Manus AI* 🤖
