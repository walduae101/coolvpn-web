# نظام مراقبة BitFuFu المتكامل مع WhatsApp Web

## نظرة عامة

نظام مراقبة تلقائي يومي لرسائل BitFuFu Revenue Journal مع إرسال تقارير شاملة عبر WhatsApp Web.

## المميزات

- 🔍 **مراقبة Gmail التلقائية** - استخراج بيانات التعدين من رسائل BitFuFu
- 📊 **تحليل ROI المتقدم** - حساب العائد على الاستثمار لكل خطة
- 📈 **مقارنة الأداء** - مقارنة تلقائية مع اليوم السابق
- 📄 **تقارير PDF احترافية** - تقارير مفصلة باللغة العربية
- 📱 **إرسال WhatsApp تلقائي** - رسائل منسقة مع رموز تعبيرية ذكية
- ⏰ **جدولة يومية** - تشغيل تلقائي في الوقت المحدد
- 🔐 **أمان وخصوصية** - جلسات محفوظة محلياً بدون كلمات مرور

## التثبيت السريع

```bash
# استنساخ المستودع
git clone https://github.com/walduae101/coolvpn-web.git
cd coolvpn-web

# تثبيت المتطلبات
pip3 install selenium webdriver-manager google-auth \
    google-auth-oauthlib google-auth-httplib2 \
    google-api-python-client

# تثبيت Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update && sudo apt-get install -y google-chrome-stable
```

## الاستخدام

### اختبار النظام
```bash
python3 test_bitfufu_automation.py
```

### تشغيل يدوي
```bash
python3 bitfufu_whatsapp_automation.py
```

### إعداد الجدولة اليومية
```bash
./setup_cron.sh
```

## الملفات الرئيسية

| الملف | الوصف |
|------|-------|
| `bitfufu_whatsapp_automation.py` | السكريبت الرئيسي المتكامل |
| `gmail_bitfufu_monitor.py` | وحدة مراقبة Gmail وتحليل ROI |
| `whatsapp_web_sender.py` | وحدة إرسال WhatsApp Web |
| `test_bitfufu_automation.py` | سكريبت الاختبار |
| `setup_cron.sh` | إعداد الجدولة اليومية |
| `BITFUFU_GUIDE.md` | دليل الاستخدام الشامل |

## خطط التعدين المراقبة

| رقم الخطة | الاسم | التكلفة | المدة |
|-----------|-------|---------|-------|
| 95936 | خطة 3 أيام | $63.00 | 3 أيام |
| 95735 | خطة 10 أيام | $63.00 | 10 أيام |
| 95937 | خطة 14 يوم | $453.73 | 14 يوم |
| 95736 | خطة 30 يوم | $439.93 | 30 يوم |

## العملية التلقائية

1. **جمع البيانات** - البحث في Gmail عن آخر بريد Revenue Journal
2. **تحليل ROI** - حساب العائد على الاستثمار ومقارنة الأداء
3. **إنشاء التقرير** - تقرير شامل بصيغة Markdown و PDF
4. **إرسال WhatsApp** - رسالة مختصرة + ملف PDF عبر WhatsApp Web

## التوقيت

- **الجدولة:** يومياً في الساعة 16:05 بتوقيت أبوظبي (12:05 UTC)
- **المدة المتوقعة:** 3-5 دقائق لكل تشغيل

## المتطلبات

- Python 3.11+
- Google Chrome
- اتصال إنترنت مستقر
- حساب Gmail (اختياري للبيانات الحقيقية)
- حساب WhatsApp (للإرسال)

## الأمان

- ✅ جلسات محفوظة محلياً فقط
- ✅ لا يتم تخزين كلمات مرور
- ✅ أذونات ملفات محدودة
- ✅ تشغيل في وضع headless

## الدعم

راجع `BITFUFU_GUIDE.md` للحصول على:
- دليل الاستخدام الكامل
- إعداد Gmail API
- إعداد WhatsApp Web
- استكشاف الأخطاء
- الصيانة والتنظيف

## الترخيص

مشروع خاص - جميع الحقوق محفوظة

---

*تم إنشاؤه بواسطة نظام Manus AI* 🤖
