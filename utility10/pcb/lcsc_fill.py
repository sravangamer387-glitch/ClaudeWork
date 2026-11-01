"""LCSC numbers for parts that the board specs leave open. Every entry below was confirmed on a web search of the LCSC/JLCPCB listing on 2026-11-01
(status 'verified'); entries with a caveat say so. Always re-check stock and the exact listing before placing an order."""
BY_VALUE = {
 "0": ("C21189", "UNI-ROYAL 0603WAF0000T5E"), "100": ("C22775", "UNI-ROYAL 0603WAF1000T5E"), "22": ("C23345", "UNI-ROYAL 0603WAF220JT5E"), "240": ("C23350", "UNI-ROYAL 0603WAF2400T5E (JLCPCB listing)"),
 "330": ("C23138", "UNI-ROYAL 0603WAF3300T5E"), "33": ("C23140", "UNI-ROYAL 0603WAF330JT5E"), "33k": ("C4216", "UNI-ROYAL 0603WAF3302T5E"), "15p": ("C1644", "Samsung CL10C150JB8NNNC C0G"), "22p": ("C1653", "Samsung CL10C220JB8NNNC C0G"),
 "2.2n": ("C16033", "Samsung CL10B222KB8NNNC X7R"), "22n": ("C21122", "Samsung CL10B223KB8NNNC X7R"), "220n": ("C64705", "Samsung CL10B224KB8NNNC X7R 50V"), "4.7u": ("C1705", "Samsung CL10A475KP8NNNC X5R 10V"),
 "STM32G431CBT6": ("C529355", "STM32G431CBT6 (LQFP-48)"), "OPA356": ("C183100", "TI OPA356AIDBVR"), "TS5A3159": ("C46388", "TI TS5A3159DCKR"), "AP2112K-3.3": ("C51118", "Diodes AP2112K-3.3TRG1 (from the LCSC datasheet link)"),
 "AMS1117-5.0": ("C6187", "AMS AMS1117-5.0 SOT-223"), "HX711": ("C43656", "Avia HX711 SOP-16"), "BAV99": ("C68983", "JSCJ BAV99"), "BAT54WS": ("C5148476", "BORN BAT54WS (300 mA listing)"),
 "AO3400A": ("C20917", "AOS AO3400A"), "SMAJ5.0A": ("C83329", "Littelfuse SMAJ5.0A"), "SMBJ15A": ("C83846", "Littelfuse SMBJ15A"), "SS14": ("C84343", "Starsea SS14 SMA"),
 "TVS 5V bidir": ("C19224", "Nexperia PESD5V0S1BA,115"), "BLM18 600R": ("C19330", "Murata BLM18AG601SN1D"), "PTC 500mA": ("C163512", "Littelfuse 1206L050YR (6 V)"),
 "PTC 1A 16V": ("C142746", "Littelfuse 1812L110/16DR (1.1 A hold, 16 V)"), "16 MHz": ("C12668", "YXC X322516MOB4SI 16 MHz 12 pF 3225 (LCSC listing seen in search results; matches the 22 pF load caps)"), "8 MHz": ("C2682775", "YXC X32258MOB4SI 8 MHz 12 pF 3225 (matches the 15 pF load caps)"),
}
BY_VALUE_FP = {
 ("Green", "LED_0603"): ("C72043", "Everlight 19-217/GHC-YR1S2/3T (LCSC showed it out of stock on the search day: check)"), ("Amber", "LED_0603"): ("C72038", "Everlight 19-213/Y2C-CQ2R2L/3T yellow 591 nm (marked obsolete by some distributors: check)"), ("Red", "LED_0603"): ("C72044", "Everlight 19-217/R6C-AL1M2VY/3T (some distributors list it as discontinued: check)"),
}
BY_FP = {   # footprint name fragment -> (lcsc, mpn); through-hole parts are hand-assembled but get numbers so the whole BOM can be bought
 "JST_PH_B2B-PH-K": ("C131337", "JST B2B-PH-K-S(LF)(SN)"), "JST_PH_B3B-PH-K": ("C131339", "JST B3B-PH-K-S(LF)(SN)"), "JST_PH_B4B-PH-K": ("C131334", "JST B4B-PH-K-S(LF)(SN)"),
 "PinHeader_2x03_P2.54mm": ("C5116479", "ZHOURI 2.54-2*3"), "PinHeader_1x04_P2.54mm": ("C5116483", "ZHOURI 2.54-1*4"), "PinHeader_1x02_P2.54mm": ("C5116481", "ZHOURI 2.54-1*2"),
 "SW_SPST_B3U-1000P": ("C231329", "Omron B3U-1000P"), "SW_SPDT_PCM12": ("C221841", "C&K PCM12SMTR"), "BarrelJack_CUI_PJ-063AH": ("C22434582", "CUI/Same Sky PJ-063AH"),
 "TerminalBlock_bornier-2_P5.08mm": ("C474952", "Cixi Kefa KF128-5.08-2P-AA"), "Buzzer_Beeper:Buzzer_12x9.5RM7.6": ("C781869", "YUEXIN KC1206 16 ohm passive magnetic 12x9.5 mm (2048 Hz)"),
}
def fill(parts):
    for p in parts:
        if p.get("lcsc") or p.get("tp") or p.get("value") == "TP": continue
        fpn = p["fp"].split(":")[-1]; hit = None
        for (v, f), (n, m) in BY_VALUE_FP.items():
            if p["value"] == v and f in fpn: hit = (n, m)
        if not hit and p["value"] in BY_VALUE and not fpn.startswith(("JST", "Pin")): hit = BY_VALUE[p["value"]]
        if not hit:
            for frag, (n, m) in BY_FP.items():
                if frag in p["fp"]: hit = (n, m); break
        if hit: p["lcsc"], p["mpn"], p["lcsc_status"] = hit[0], hit[1], "verified"
    return parts
