import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="DATA.ER",
    page_icon="🐬",
    layout="wide",
    initial_sidebar_state='collapsed'
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache()
def get_df():
    _df = pd.read_csv('./resource/superstore.csv')
    _df["Sales"] = _df["Sales"].apply(pd.to_numeric, errors='coerce').fillna(0.0)
    _df['Order Date'] = pd.to_datetime(_df['Order Date'])
    # df.iloc[df['Order Date'].sort_values().index,:]

    for i in range(len(_df)):
        _df['Order Date'][i] = str(_df['Order Date'][i].year) + '-' + str(_df['Order Date'][i].month)
    _df['Order Date'] = pd.to_datetime(_df['Order Date'])
    _df = _df.drop(columns=['Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Row ID'])
    _df = _df.drop_duplicates()
    _df['Year'] = _df['Order Date'].apply(lambda x: str(x)[0:4])
    return _df


def get_fig(*key):
    plt.style.use('seaborn')
    # categ = df.groupby(['Order Date', 'Ship Mode'])['Profit'].sum()
    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Ship Mode'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Ship Mode'])[obj].sum()
    year_month = []
    for i in range(len(categ)):
        if categ.index[i][0] in year_month:
            year_month.remove(categ.index[i][0])
        year_month.append(categ.index[i][0])
    yearmonth = []
    for i in range(len(year_month)):
        yearmonth.append(str(year_month[i].year) + '-' + str(year_month[i].month))
    year_month = yearmonth

    a = FirstClass = []
    b = SecondClass = []
    c = SameDay = []
    SameDay.append(0)
    SameDay.append(0)
    SameDay.append(0)
    SameDay.append(0)
    d = StandardClass = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'First Class':
            FirstClass.append(categ[i])
        if categ.index[i][1] == 'Second Class':
            SecondClass.append(categ[i])
        if categ.index[i][1] == 'Same Day':
            SameDay.append(categ[i])
        if categ.index[i][1] == 'Standard Class':
            StandardClass.append(categ[i])

    fig_ship_mode_analysis = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, marker='*', label='First Class')
    plt.plot(year_month, b, marker='^', label='Second Class')
    plt.plot(year_month, c, marker='s', label='Same Day')
    plt.plot(year_month, d, marker='*', label='Standard Class')
    plt.xlabel('Time', fontsize=0.05)
    plt.legend()
    # 主流还是standard class，technology 的销售情况和firstclass有关系，

    fig_ship_mode_count = plt.figure(figsize=(7, 6))
    plt.xticks(rotation=45)
    sns.countplot(x=df['Ship Mode'], palette='rocket')
    plt.title("Ship Mode count")

    # categ = df.groupby(['Order Date', 'Category'])['Sales'].sum()
    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Category'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Category'])[obj].sum()

    a = Furniture = []
    b = OfficeSupplies = []
    c = Technology = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'Furniture':
            Furniture.append(float(categ[i]))
        if categ.index[i][1] == 'Office Supplies':
            OfficeSupplies.append(categ[i])
        if categ.index[i][1] == 'Technology':
            Technology.append(categ[i])
    fig_fur_off_tec = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, marker='*', label='Furniture')
    plt.plot(year_month, b, marker='^', label='Office Supplies')
    plt.plot(year_month, c, marker='s', label='Technology')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()
    # 三条曲线相似，说明利润与三种类型的商品本身的区别关系不大，而在于外部市场环境，或企业内部统一的流程或程序

    if len(y) > 0:
        fig_cat_pro = plt.figure(figsize=(5, 4))
        df[df['Year'].isin(y)].groupby('Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=15)
        fig_subcat_pro = plt.figure(figsize=(5, 4))
        df[df['Year'].isin(y)].groupby('Sub-Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=70)
        fig_subcat_count = plt.figure(figsize=(7, 6))
        plt.xticks(rotation=45)
        sns.countplot(x=df[df['Year'].isin(y)]['Sub-Category'], palette='rocket')
        plt.title("Sub-Category count")
    else:
        fig_cat_pro = plt.figure(figsize=(5, 4))
        df.groupby('Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=15)
        fig_subcat_pro = plt.figure(figsize=(5, 4))
        df.groupby('Sub-Category')['Profit'].sum().plot(kind='bar', title='Category Profit', rot=70)
        fig_subcat_count = plt.figure(figsize=(7, 6))
        plt.xticks(rotation=45)
        sns.countplot(x=df['Sub-Category'], palette='rocket')
        plt.title("Sub-Category count")

    fig_fot = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=30)
    furn = ['Bookcases', 'Chairs', 'Furnishings', 'Tables']
    value1 = [-3724.1105, 26323.1308, 12951.1558, -17500.7573]
    offsu = ['Appliances', 'Art', 'Binders', 'Envelopes', 'Fasteners', 'Labels', 'Paper', 'Storage', 'Supplies']
    value2 = [18066.4649, 6481.5983, 30268.0106, 6946.6567, 936.7418, 5441.9123, 33735.1894, 21247.6690, -1201.9387]
    tech = ['Accessories', 'Copiers', 'Machines', 'Phones']
    value3 = [41601.5363, 55557.8269, 3384.7569, 44440.8206]
    plt.bar(furn, value1, width=0.2, label='Furniture')
    plt.bar(offsu, value2, width=0.2, label='Office Supplies')
    plt.bar(tech, value3, width=0.2, label='Technology')
    plt.legend()

    # categ = df.groupby(['Order Date', 'Segment'])['Profit'].sum()

    if obj == 'Margin':
        categ = df.groupby(['Order Date', 'Segment'])[['Profit', 'Sales']].sum()
        categ['Margin'] = categ['Profit'] / categ['Sales']
        categ = categ['Margin']
    else:
        categ = df.groupby(['Order Date', 'Segment'])[obj].sum()

    a = Consumer = []
    b = Corporate = []
    c = HomeOffice = []
    for i in range(len(categ)):
        if categ.index[i][1] == 'Consumer':
            Consumer.append(float(categ[i]))
        if categ.index[i][1] == 'Corporate':
            Corporate.append(categ[i])
        if categ.index[i][1] == 'Home Office':
            HomeOffice.append(categ[i])
    fig_seg_line = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.plot(year_month, a, label='Consumer')
    plt.plot(year_month, b, label='Corporate')
    plt.plot(year_month, c, label='Home Office')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()

    fig_seg_bar = plt.figure(figsize=(19, 6))
    plt.xticks(rotation=60)
    plt.bar(year_month, a, label='Consumer')
    plt.bar(year_month, b, label='Corporate')
    plt.bar(year_month, c, label='Home Office')
    plt.xlabel('Time', fontsize=0.01)
    plt.legend()

    # ten_ = df.groupby('City')['Profit'].sum().sort_values().tail(10)

    if obj == 'Margin':
        ten_ = df.groupby('City')[['Profit', 'Sales']].sum()
        ten_['Margin'] = ten_['Profit'] / ten_['Sales']
        ten_ = ten_['Margin'].sort_values().tail(10)
    else:
        ten_ = df.groupby('City')[obj].sum().sort_values().tail(10)

    value = ten_.values.tolist()
    ten = ten_.index.tolist()

    fig_city_pro = plt.figure(figsize=(15, 8))
    # 绘制条形图
    plt.barh(range(len(value)), value, height=0.5, color='orange')  # 区别于竖的条形图 不能使用width
    # 设置字符串到X轴
    plt.yticks(range(len(value)), ten)
    # for a, b in enumerate(value):
    #     plt.text(a+0.1, b+1,a,ha='left',va='bottom')
    plt.grid(alpha=0.3)

    def city_profit(category):
        fig_city = plt.figure(figsize=(5, 4))
        category_1 = df[df['Category'] == category]
        # category_1.groupby('City')['Profit'].sum().sort_values(ascending=False)[:5].plot(kind='bar',
        #                                                                                  title="Top 5 Cities that made the most profit in {}".format(
        #                                                                                      category), rot=15)

        if obj == 'Margin':
            category_1 = category_1.groupby('City')[['Profit', 'Sales']].sum()
            category_1['Margin'] = category_1['Profit'] / category_1['Sales']
            category_1 = category_1['Margin']
            category_1.sort_values(ascending=False)[:5].plot(kind='bar',
                                                             title="Top 5 Cities that made the most {} in {}".format(
                                                                 obj,
                                                                 category), rot=15)
        else:
            category_1.groupby('City')[obj].sum().sort_values(ascending=False)[:5].plot(kind='bar',
                                                                                        title="Top 5 Cities that made the most {} in {}".format(
                                                                                            obj,
                                                                                            category), rot=15)
        return fig_city

    fig_city_pro_tec = city_profit('Technology')
    fig_city_pro_fur = city_profit('Furniture')
    fig_city_pro_sup = city_profit('Office Supplies')

    return fig_ship_mode_analysis, fig_ship_mode_count, fig_fur_off_tec, fig_cat_pro, fig_subcat_pro, fig_subcat_count, fig_fot, fig_seg_line, fig_seg_bar, fig_city_pro, fig_city_pro_tec, fig_city_pro_fur, fig_city_pro_sup


# fig_cus_order = plt.figure(figsize=(5, 4))
# df['Customer ID'].value_counts()[:15].plot(kind='barh', title='Customer ID & Product Ordered')

df = get_df()
cids = set(df['Customer ID'])
years = list(df['Order Date'])
years = set([str(y)[0:4] for y in years])
y = []
# 前端展示部分
st.title('Business Analysis of Retail')
st.image('./resource/WechatIMG98.jpeg')
tab = st.sidebar.radio('',
                       ["Ship Mode Analysis"
                           , "Product Analysis"
                           , "Segment Analysis"
                           , "Region Analysis"
                        # , "Customer ID & Product Ordered"
                        ])
if tab == 'Ship Mode Analysis':
    st.subheader('Ship Mode Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[0])
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(get_fig(df, obj)[1])
    with c2:
        cid = st.text_input('Please Input a Customer ID')
        query = st.button('Query')
        if query:
            dfc = df[df['Customer ID'] == cid]
            if len(dfc) == 0:
                st.warning('The customer id you input does not exist, so show all.')
                st.dataframe(df)
            else:
                st.dataframe(df[df['Customer ID'] == cid])
                total_profit = df[df['Customer ID'] == cid]['Profit'].sum()
                st.metric('Total Profit', round(total_profit,2))
elif tab == 'Product Analysis':
    st.subheader('Product Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[2])
    y = st.multiselect('Please Choose Year', years)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.pyplot(get_fig(df, obj, y)[3])
    with c2:
        st.pyplot(get_fig(df, obj, y)[4])
    with c3:
        st.pyplot(get_fig(df, obj, y)[5])
    st.pyplot(get_fig(df, obj)[6])
elif tab == 'Segment Analysis':
    st.subheader('Segment Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[7])
        st.write(obj)
        st.pyplot(get_fig(df, obj)[8])
elif tab == 'Region Analysis':
    st.subheader('Region Analysis')
    c1, c2 = st.columns([1, 10])
    with c1:
        obj = st.radio('', ['Profit', 'Sales', 'Margin'])
    with c2:
        st.write(obj)
        st.pyplot(get_fig(df, obj)[9])
    c1, c2, c3 = st.columns(3)
    with c1:
        st.pyplot(get_fig(df, obj)[10])
    with c2:
        st.pyplot(get_fig(df, obj)[11])
    with c3:
        st.pyplot(get_fig(df, obj)[12])
# elif tab == 'Customer ID & Product Ordered':
#     st.subheader('Customer ID & Product Ordered')
#     st.pyplot(fig_cus_order)
