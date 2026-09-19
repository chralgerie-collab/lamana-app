import pandas as pd
import streamlit as st

# إعداد واجهة التطبيق لتناسب اللغة العربية (من اليمين إلى اليسار)
st.set_page_config(
    page_title="Lamana Delivery",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    "<style>body { direction: rtl; text-align: right; }</style>",
    unsafe_allow_html=True,
)

st.title("🛡️ نظام Lamana Delivery المتكامل للتسيير")
st.subheader("مستودع أولاد فايت - تسيير الاستلام، التوزيع، والمالية")

# --- 1. القائمة الجانبية: الإعدادات الثابتة والمصاريف ---
st.sidebar.header("📊 الإعدادات المالية الثابتة")
loyer = st.sidebar.number_input("كراء المستودع شهرياً (دج)", value=50000)
factures = st.sidebar.number_input("الإنترنت والكهرباء شهرياً (دج)", value=4000)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ تكاليف التوزيع والتشغيل")
tarif_total_marchand = 600  # 500 توصيل + 100 تخزين وتغليف
part_livreur = 350
part_agent_depot = 50
coût_emballage = 20

# --- 2. إدارة قاعدة البيانات الحية للطرود (في المستودع) ---
if "db_colis" not in st.session_state:
  # وضع طرود تجريبية كبداية لتسهيل الفهم
  st.session_state.db_colis = pd.DataFrame([
      {
          "رمز الطرد": "LMN-001",
          "اسم التاجر": "صفحة الملابس الأنيقة",
          "بلدية التوصيل": "الشراقة",
          "هاتف الزبون": "0550123456",
          "سعر السلعة (دج)": 4500,
          "الموزع": "أحمد (موتو)",
          "حالة الطرد": "قيد التوصيل",
      },
      {
          "رمز الطرد": "LMN-002",
          "اسم التاجر": "صفحة الهواتف الذكية",
          "بلدية التوصيل": "باب الزوار",
          "هاتف الزبون": "0661987654",
          "سعر السلعة (دج)": 12000,
          "الموزع": "محمد (موتو)",
          "حالة الطرد": "تم التسليم",
      },
  ])

st.markdown("---")
st.header("📥 1. استلام الطرود الجديدة (تسجيل السلعة في المستودع)")

# استمارة إدخال الطرود صباحاً عند الاستلام
with st.form("form_ajout_colis", clear_on_submit=True):
  col1, col2, col3 = st.columns(3)
  with col1:
    code_colis = st.text_input(
        "رمز الطرد (مثال: LMN-003)",
        value=f"LMN-00{len(st.session_state.db_colis)+1}",
    )
    marchand = st.text_input("اسم التاجر / الصفحة")
  with col2:
    commune = st.text_input("بلدية التوصيل")
    phone = st.text_input("رقم هاتف الزبون")
  with col3:
    prix_selaa = st.number_input("سعر السلعة كاش (دج)", min_value=0, value=2000)
    livreur_nom = st.selectbox(
        "تعيين الموزع المسؤول", ["أحمد (موتو)", "محمد (موتو)", "ياسين (موتو)"]
    )

  submit_colis = st.form_submit_button("✅ تسجيل وتأكيد استلام الطرد في المستودع")

  if submit_colis and marchand and commune and phone:
    new_data = {
        "رمز الطرد": code_colis,
        "اسم التاجر": marchand,
        "بلدية التوصيل": commune,
        "هاتف الزبون": phone,
        "سعر السلعة (دج)": prix_selaa,
        "الموزع": livreur_nom,
        "حالة الطرد": "قيد التوصيل",
    }
    st.session_state.db_colis = pd.concat(
        [st.session_state.db_colis, pd.DataFrame([new_data])], ignore_index=True
    )
    st.success(f"تم تسجيل الطرد {code_colis} بنجاح وتحويله للتغليف!")

# --- 3. إدارة التوزيع والتحديث المسائي للطرود ---
st.markdown("---")
st.header("🏍️ 2. توزيع ومحاسبة الطرود (الفرز والتحيين المسائي للسيولة)")

st.write("تحديث حالة الطرود بعد عودة الموزعين مساءً إلى مستودع أولاد فايت:")

# عرض الجدول بطريقة تتيح لك تعديل الحالات مباشرة
edited_df = st.data_editor(
    st.session_state.db_colis,
    column_config={
        "حالة الطرد": st.column_config.SelectboxColumn(
            "حالة الطرد حية",
            options=["قيد التوصيل", "تم التسليم", "مسترجع"],
            required=True,
        )
    },
    disabled=[
        "رمز الطرد",
        "اسم التاجر",
        "بلدية التوصيل",
        "هاتف الزبون",
        "سعر السلعة (دج)",
        "الموزع",
    ],
    key="data_editor_colis",
)
st.session_state.db_colis = edited_df

# --- 4. الحسابات المالية الحية والأرباح الصافية الحقيقية ---
st.markdown("---")
st.header("💰 3. التقرير المالي الحي والأرباح الصافية")

# حساب أعداد الحالات الحقيقية من الجدول
total_recu = len(st.session_state.db_colis)
total_livre = len(st.session_state.db_colis[st.session_state.db_colis["حالة الطرد"] == "تم التسليم"])
total_retour = len(st.session_state.db_colis[st.session_state.db_colis["حالة الطرد"] == "مسترجع"])
total_en_cours = len(st.session_state.db_colis[st.session_state.db_colis["حالة الطرد"] == "قيد التوصيل"])

# الحسابات المالية الحقيقية القائمة على الطرود المسلمة بنجاح
revenu_brut_reel = total_livre * tarif_total_marchand
depense_livreurs_reel = total_livre * part_livreur
depense_agent_reel = total_recu * part_agent_depot  # العامل يأخذ حقه على كل طرد يفرزه ويغلفه دخل للمستودع
depense_emballage_reel = total_recu * coût_emballage

# صافي الربح اليومي الحقيقي
gain_net_jour_reel = revenu_brut_reel - (
    depense_livreurs_reel + depense_agent_reel + depense_emballage_reel
)

# الإسقاط الشهري بناءً على الوتيرة الحالية (26 يوم عمل)
ca_mensuel_estime = revenu_brut_reel * 26
total_frais_mensuels_estime = (
    (depense_livreurs_reel + depense_agent_reel + depense_emballage_reel) * 26
) + (loyer + factures)
profit_mensuel_net_estime = ca_mensuel_estime - total_frais_mensuels_estime

# عرض بطاقات الأداء المالي الحية في المستودع
c1, c2, c3, c4 = st.columns(4)
with c1:
  st.metric(label="📦 إجمالي الطرود بالمستودع", value=total_recu)
with c2:
  st.metric(label="✅ طرود تم تسليمها بنجاح", value=total_livre)
with c3:
  st.metric(label="⚠️ طرود مسترجعة (Retour)", value=total_retour)
with c4:
  st.metric(label="⏳ طرود قيد التوصيل في العاصمة", value=total_en_cours)

st.markdown("---")
cx1, cx2, cx3 = st.columns(3)
with cx1:
  st.metric(
      label="📈 الفائدة الصافية المحصلة اليوم كاش",
      value=f"{gain_net_jour_reel:,.0f} دج",
  )
with cx2:
  st.metric(
      label="📉 إسقاط مجموع المصاريف شهرياً",
      value=f"{total_frais_mensuels_estime:,.0f} دج",
  )
with cx3:
  st.metric(
      label="💰 أرباحك الصافية التقديرية (شهرياً)",
      value=f"{profit_mensuel_net_estime:,.0f} دج",
  )

st.markdown("---")
st.subheader("📋 تفصيل المستحقات والسيولة لليوم")
تفصيل_بيان = {
    "البيان العملياتي والمالي اليومي": [
        "مجموع عمولات الموزعين للدفع نقداً",
        "مستحقات عامل المستودع للتغليف والفرز",
        "تكلفة استهلاك مواد التغليف والعلب",
        "السيولة الصافية الباقية لشركة Lamana اليوم",
    ],
    "المبلغ بالدينار (دج)": [
        depense_livreurs_reel,
        depense_agent_reel,
        depense_emballage_reel,
        gain_net_jour_reel,
    ],
}
st.table(pd.DataFrame(تفصيل_بيان))
