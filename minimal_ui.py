"""
title: Minimal UI Filter
author: Your Name
version: 0.1.0
type: filter
description: Hides UI elements for non-admin users via CSS injection.
"""

from pydantic import BaseModel, Field
from typing import Optional

class Filter:
    class Valves(BaseModel):
        hide_sidebar: bool = Field(default=True, description="Hide sidebar for non-admins")
        hide_model_selector: bool = Field(default=True, description="Hide model selector for non-admins")
        hide_logo: bool = Field(default=True, description="Hide logo for non-admins")

    def __init__(self):
        self.valves = self.Valves()
        self.toggle = False  # غیرفعال کردن دکمه تاگل برای کاربر

    async def inlet(self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None) -> dict:
        # تشخیص ادمین بودن
        is_admin = __user__ and __user__.get("role") == "admin"
        
        if not is_admin and __event_emitter__:
            # تزریق CSS از طریق رویداد
            css_rules = []
            if self.valves.hide_sidebar:
                css_rules.append("#sidebar { display: none !important; }")
            if self.valves.hide_model_selector:
                css_rules.append("#model-selector { display: none !important; }")
            if self.valves.hide_logo:
                css_rules.append("header img, nav img, #splash-screen img { display: none !important; }")
            
            css = "\n".join(css_rules)
            await __event_emitter__({
                "type": "execute",
                "data": {
                    "code": f"""
                    (function() {{
                        let style = document.getElementById('minimal-ui-css');
                        if (!style) {{
                            style = document.createElement('style');
                            style.id = 'minimal-ui-css';
                            document.head.appendChild(style);
                        }}
                        style.textContent = `{css}`;
                    }})();
                    """
                }
            })
        
        return body
