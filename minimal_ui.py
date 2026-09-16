"""
title: Minimal UI Extension
author: Your Name
version: 0.1.0
type: extension
description: Hides all UI elements for non-admin users to provide a minimal chat interface.
"""

import json

class Extension:
    class Valves:
        # این بخش به ادمین اجازه می‌دهد بدون تغییر کد، تنظیمات را تغییر دهد
        hide_sidebar: bool = True
        hide_model_selector: bool = True
        hide_logo: bool = True
        hide_navbar: bool = False
        admin_bypass: bool = True  # اگر True باشد، ادمین رابط کامل را می‌بیند

    def __init__(self):
        self.valves = self.Valves()

    def assets(self) -> dict:
        """
        این متد به‌صورت خودکار توسط Open WebUI فراخوانی می‌شود
        و محتوای JS و CSS را در سراسر برنامه تزریق می‌کند.
        """
        # --- اسکریپت JavaScript برای تشخیص نقش کاربر ---
        js_code = """
        (async function() {
            try {
                // دریافت اطلاعات کاربر جاری از API داخلی
                const response = await fetch('/api/v1/auths/');
                const user = await response.json();
                
                // بررسی ادمین بودن
                const isAdmin = user.role === 'admin';
                
                // اگر ادمین است و می‌خواهیم رابط کامل را ببیند
                if (isAdmin) {
                    document.body.classList.add('owui-admin-user');
                } else {
                    document.body.classList.add('owui-normal-user');
                }
            } catch (e) {
                // در صورت خطا، فرض می‌کنیم کاربر عادی است
                document.body.classList.add('owui-normal-user');
            }
        })();
        """

        # --- استایل CSS برای مخفی کردن المان‌ها ---
        # فقط برای کاربران عادی اعمال می‌شود
        css_rules = []
        if self.valves.hide_sidebar:
            css_rules.append("body.owui-normal-user #sidebar { display: none !important; }")
        if self.valves.hide_model_selector:
            css_rules.append("body.owui-normal-user #model-selector { display: none !important; }")
        if self.valves.hide_logo:
            css_rules.append("body.owui-normal-user header img, body.owui-normal-user nav img { display: none !important; }")
            css_rules.append("body.owui-normal-user #splash-screen img { display: none !important; }")
        if self.valves.hide_navbar:
            css_rules.append("body.owui-normal-user nav { display: none !important; }")

        css_code = "\n".join(css_rules)

        return {
            "js": js_code,
            "css": css_code
        }