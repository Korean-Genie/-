import streamlit as st
import pandas as pd
import datetime

# 파일 업로드 함수
def load_data():
    uploaded_file = st.file_uploader("직원 데이터 파일을 업로드하세요 (Excel 또는 CSV)", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
    return None

# 메인 애플리케이션
def main():
    st.title("직원 관리 시스템")

    # 데이터 로드
    df = load_data()

    if df is not None:
        # 날짜 형식 변환
        date_columns = ['입사일', '퇴사일']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col]).dt.date

        # 사이드바에 페이지 선택 옵션 추가
        page = st.sidebar.selectbox("페이지 선택", ["직원 검색", "고용 상태판"])

        if page == "직원 검색":
            employee_search(df)
        elif page == "고용 상태판":
            employment_status_board(df)

def employee_search(df):
    st.header("직원 검색")

    # 검색 입력
    search_term = st.text_input("직원 이름 또는 직원 번호로 검색:")

    if search_term:
        # 이름 또는 직원 번호로 검색
        result = df[(df['이름'].str.contains(search_term, case=False, na=False)) | 
                    (df['직원 번호'].astype(str).str.contains(search_term, na=False))]

        if not result.empty:
            for _, employee in result.iterrows():
                st.subheader(f"{employee['이름']} ({employee['직원 번호']})")
                st.write(f"고용 상태: {'재직 중' if employee['고용 상태'] == '재직 중' else '퇴사'}")
                st.write(f"정규직/비정규직: {employee['정규직/비정규직 여부']}")
                st.write(f"직위: {employee['직위']}")
                st.write(f"직급: {employee['직급']}")
                st.write(f"소속: {employee['소속']}")
                st.write(f"부서: {employee['부서']}")
                st.write(f"전화번호: {employee['전화번호']}")
                st.write(f"이메일: {employee['이메일']}")
                st.write("---")
        else:
            st.warning("검색 결과가 없습니다.")

def employment_status_board(df):
    st.header("고용 상태판")

    # 현재 날짜
    current_date = datetime.date.today()

    # 기간 필터
    filter_option = st.selectbox("기간 선택", ["전체", "특정 연도", "특정 월"])
    
    if filter_option == "특정 연도":
        selected_year = st.selectbox("연도 선택", range(current_date.year, 2000, -1))
        df = df[df['입사일'].dt.year == selected_year]
    elif filter_option == "특정 월":
        selected_month = st.selectbox("월 선택", range(1, 13))
        df = df[df['입사일'].dt.month == selected_month]

    # 재직 중인 직원
    current_employees = df[df['고용 상태'] == '재직 중']
    st.subheader("현재 재직 중인 직원")
    st.dataframe(current_employees[['이름', '정규직/비정규직 여부', '직위', '입사일', '부서']])

    # 올해 퇴사한 직원
    resigned_employees = df[(df['고용 상태'] == '퇴사') & (df['퇴사일'].dt.year == current_date.year)]
    st.subheader("올해 퇴사한 직원")
    st.dataframe(resigned_employees[['이름', '정규직/비정규직 여부', '직위', '퇴사일', '퇴사 경로']])

if __name__ == "__main__":
    main()
