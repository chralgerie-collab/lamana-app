import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Lamana Delivery",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    "<style>body { direction: rtl; text-align: right; }</style>",
    unsafe_allow_html=True,
)

st.title("🛡️ نظام Lamana Delivery الذكي للتسيير")
st.subheader("مستودع أولاد فايت - لوحة التحكم للمسيّر")

st.sidebar.header("📊 الإعدادات المالية الثابتة")
loyer = st.sidebar.number_input("كراء المستودع شهرياً (دج)", value=50000)
factures = st.sidebar.number_input("الإنترنت والكهرباء شهرياً (دج)", value=4000)

st.sidebar.header("📦 العمليات اليومية")
nb_colis = st.sidebar.number_input("عدد الطرود المسلمة اليوم", value=50, step=1)

tarif_total_marchand = 600
part_livreur = 350
part_agent_depot = 50
coût_emballage = 20

revenu_journalier_brut = nb_colis * tarif_total_marchand
depense_livreurs_jour = nb_colis * part_livreur
depense_agent_jour = nb_colis * part_agent_depot
depense_emballage_jour = nb_colis * coût_emballage
gain_net_lamana_jour = (
    revenu_journalier_brut
    - (
        depense_livreurs_jour
        + depense_agent_jour
        + depense_emballage_jour
    )
)

jours_travail = 26
ca_mensuel = revenu_journalier_brut * jours_travail
frais_mensuels_variables = (
    depense_livreurs_jour + depense_agent_jour + depense_emballage_jour
) * jours_travail
frais_fixes_mensuels = loyer + factures
profit_net_mensuel = ca_mensuel - (
    frais_mensuels_variables + frais_fixes_mensuels
)

col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="📈 المدخول الشهري الإجمالي", value=f"{ca_mensuel:,.0f} دج")
with col2:
  st.metric(
      label="📉 مجموع المصاريف (عمال + كراء)",
      value=f"{(frais_mensuels_variables + frais_fixes_mensuels):,.0f} دج",
  )
with col3:
  st.metric(
      label="💰 صافي ربح نسيم (شهرياً)", value=f"{profit_net_mensuel:,.0f} دج"
  )

st.markdown("---")
st.subheader("📋 كشف حساب التوزيع اليومي للموزعين والعمال")
data = {
    "البيان": [
        "مستحقات الموزعين اليومية",
        "مستحقات عامل المستودع اليومية",
        "تكلفة مواد التغليف اليومية",
        "صافي الفائدة اليومية للشركة",
    ],
    "المبلغ بالدينار (دج)": [
        depense_livreurs_jour,
        depense_agent_jour,
        depense_emballage_jour,
        gain_net_lamana_jour,
    ],
    "المبلغ بالسنتيم": [
        depense_livreurs_jour * 100,
        depense_agent_jour * 100,
        depense_emballage_jour * 100,
        gain_net_lamana_jour * 100,
    ],
}
df = pd.DataFrame(data)
st.table(df)
