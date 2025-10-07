#!/bin/bash
# سكريبت إعداد الجدولة اليومية لنظام مراقبة BitFuFu

echo "إعداد الجدولة اليومية..."

# إنشاء سكريبت wrapper للتشغيل
cat > /home/ubuntu/run_bitfufu_daily.sh << 'EOF'
#!/bin/bash
# سكريبت التشغيل اليومي

# تسجيل بداية التشغيل
echo "========================================" >> /home/ubuntu/bitfufu_cron.log
echo "بدء التشغيل: $(date)" >> /home/ubuntu/bitfufu_cron.log

# تشغيل السكريبت الرئيسي
cd /home/ubuntu
echo "test_group" | python3 /home/ubuntu/bitfufu_whatsapp_automation.py >> /home/ubuntu/bitfufu_cron.log 2>&1

# تسجيل نهاية التشغيل
echo "انتهى التشغيل: $(date)" >> /home/ubuntu/bitfufu_cron.log
echo "========================================" >> /home/ubuntu/bitfufu_cron.log
EOF

# جعل السكريبت قابل للتنفيذ
chmod +x /home/ubuntu/run_bitfufu_daily.sh

# إضافة مهمة cron (يومياً في 12:05 UTC = 16:05 بتوقيت أبوظبي)
CRON_JOB="5 12 * * * /home/ubuntu/run_bitfufu_daily.sh"

# التحقق من وجود المهمة
(crontab -l 2>/dev/null | grep -v "run_bitfufu_daily.sh"; echo "$CRON_JOB") | crontab -

echo "✓ تم إعداد الجدولة اليومية"
echo "  - الوقت: يومياً في 16:05 بتوقيت أبوظبي (12:05 UTC)"
echo "  - السكريبت: /home/ubuntu/run_bitfufu_daily.sh"
echo "  - السجل: /home/ubuntu/bitfufu_cron.log"
echo ""
echo "لعرض المهام المجدولة: crontab -l"
echo "لإلغاء الجدولة: crontab -r"
