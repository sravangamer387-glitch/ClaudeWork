# Phase 1 · Market, Rules and Manufacturing Base

Status: complete. Evidence tags: **[S]** found in web research (secondary sources, often consultancy/marketing pages); **[K]** from my background knowledge, not re-verified; **(assumption)** my estimate.

## 1. Market
- India's toy market is estimated at about **$2.1–2.8 billion**, growing about **6.4–9.5 % a year** (estimates differ by report). Educational toys: about **$2.3 billion** in 2025 at **~8 % CAGR**. Electronic toys are named as the **fastest-growing segment** in several reports; one smart-toys report claims ~25.7 % CAGR, which looks like an outlier. No source gave a clean "electronic toys only" figure. [S]
- Demand drivers cited: activity-based learning in NEP 2020, STEM interest, e-commerce and quick commerce growth in Tier 2/3 cities. [S]
- Sources: [IMARC – India toys market](https://imarcgroup.com/indian-toys-market), [IMARC – India educational toys](https://www.imarcgroup.com/india-educational-toys-market), [The Week – educational toys sector](https://www.theweek.in/news/biz-tech/2026/08/01/indias-educational-toys-sector-trends-challenges-and-prospects.amp.html), [Market Research Future – India smart toys](https://www.marketresearchfuture.com/reports/india-smart-toys-market-62831).
- **Gap:** I could not find a ranked list of best-selling electronic toys on Amazon.in or Flipkart. The Metricscart Amazon.in Toys & Games bestseller report may have it – check before final decisions. [Metricscart](https://metricscart.com/bestseller-reports/amazon-in/categories/Toys%20%26%20Games/)

## 2. Rules that decide what you can sell
| Topic | What we know | Source/Status |
|---|---|---|
| ISI mark | Mandatory for all toys sold in India; **electric toys are tested to IS 15644** (battery-operated, transformer, dual-supply); non-electric parts to IS 9873 | [S] [evtlindia](https://www.evtlindia.com/isi/product-list/bis-certification-for-safety-of-electric-toys-is-15644/), [Alephindia](https://alephindia.in/isi-product/safety-of-electric-toys-is-15644-2006.php), [Intertek 2026 manual](https://www.intertek.com/products-retail/insight-bulletins/2026/india-bis-toy-safety-product-manual/) |
| Model grouping | One model can represent a family if same power supply layout, chassis, power requirement and battery type/size – **design a platform and certify the family** | [S] same sources |
| Timeline | Domestic manufacturers about 30–35 working days (consultancy claim); foreign makers via FMCS about 180 working days | [S] unverified |
| Radio (Bluetooth, 2.4 GHz RC, walkie-talkie) | Likely needs WPC/ETA equipment approval and may need restricted-band licensing for walkie-talkies. **My searches found nothing on this – verify before any wireless product.** | [K] verify |
| GST | Non-electric toys 5 %, electronic toys 18 % from 22 Sep 2025 | [S] [Tally](https://tallysolutions.com/gst/new-gst-rates-september-2025-business-impact/); verify |
| Import duty | Raised to 60–70 % in 2020–21; **reduced from 70 % to 20 % on certain electronic toys from 1 May 2025** (Finance Bill 2025). Imports may be cheaper again; BIS rules still apply. Check Finance Act 2026. | [S] [Business Standard](https://bsppd.business-standard.com/article/economy-policy/govt-hikes-import-duty-on-toys-to-70-to-boost-domestic-manufacturing-123020101712_1.html), [IndiaSeaTradeNews](https://indiaseatradenews.com/indias-toy-import-curbs-yield-success-exports-stagnate/) |
| E-waste | E-Waste (Management) Rules 2022 (from 1 Apr 2023) reportedly cover toys; producers need EPR; hazardous-substance limits apply; micro enterprises reportedly excluded. Batteries fall under the Battery Waste Management Rules 2022. | [S] [Mondaq](https://www.mondaq.com/india/waste-management/1535662/navigating-indias-e-waste-regulation); verify with CPCB |
| Lithium cells | Cell/battery certification burden likely (BIS cell standard). Not confirmed by search. **Prefer AA/AAA or sealed alkaline packs; avoid lithium in Wave 1.** | [K] verify |
| Enforcement | BIS seized uncertified toys at Amazon/Flipkart warehouses and stores. | [S] [Inc42](https://inc42.com/buzz/bis-raids-amazon-flipkart-warehouses-for-selling-non-certified-products) |

## 3. Manufacturing base in and near Hyderabad
Electronics assembly leads (all **unverified directory/blog claims**; request samples and audit):
- **Tescom** – EMS/PCBA, automated SMT with AOI/SPI/X-ray, Bengaluru and Hyderabad [S] [IndiaMART](https://m.indiamart.com/tescom-bengaluru)
- **Accord Power Digital Products** – Patancheru, small-batch power PCBs/control panels [S]
- **Metro Circuits** – IDA Pashamylaram, through-hole assembly, rigid PCB fab, MOQ 1 [S]
- **Argus Embedded Systems** – Hyderabad [S] (services not stated)
- Directories to find more: [IndiaMART EMS](https://m.indiamart.com/impcat/electronics-manufacturing-service.html), [SMT job work](https://m.indiamart.com/impcat/smt-job-work.html)
- Plastic enclosures: injection moulders already listed in `gravity-toys/00-research-and-sourcing.md` (Efficient Technocrafts, Ashok Brand, DSC Plastic Industries, Device Generation) [S]
- Component sourcing: Indian distributors and Shenzhen markets for modules, voice-chip ICs, motors, speakers [K]
- Testing labs: Bharat Test House, Krishna Metallurgical Laboratories (IS 15644 coverage claimed), Intertek Bengaluru [S]

## 4. Phase 1 conclusions
1. The strongest opening is **Indian-language and curriculum-linked electronic toys**, not generic RC cars or gadgets.
2. **Avoid radio, lithium and under-3 products in Wave 1** to cut compliance risk.
3. Design on **shared platforms** (one audio board, one motor board) and certify product families.
4. Open questions to close before spending: WPC/ETA rules; battery certification; e-waste EPR threshold; 2026 import duty; real bestseller data.
