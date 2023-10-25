import streamlit as st
import pandas as pd

def read_file(file):
    # Read the first line of the file to determine the delimiter
    first_line = file.readline().decode()
    file.seek(0)  # Reset file pointer to the beginning
    if ',' in first_line:
        delimiter = ','
    elif ';' in first_line:
        delimiter = ';'
    else:
        st.error('Unsupported file format. Please use a CSV file with either comma or semicolon as the delimiter.')
        return None

    if file.type == 'text/csv':
        df = pd.read_csv(file, sep=delimiter)
    elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
    return df

def main():
    st.title("Mini App for EasyFlow")
    col1, col2 = st.columns(2)
    uploaded_file = col1.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

    if uploaded_file is not None:        

        df = read_file(uploaded_file)
        original_col_names = df.columns.tolist()

        st.write("### Select Columns")

        label_col = col1.selectbox("Select :red[ Label] Column", original_col_names, key='1')

        col_names_2 = [col for col in original_col_names if col != label_col]
        volume_col = col1.selectbox('Select :red[Volume/ Size] Column', col_names_2, key='2')

        col_names_3 = [col for col in col_names_2 if col != volume_col]
        intensity_col = col1.selectbox('Select :red[Pixel Intensity] Column', col_names_3, key='3')

        if st.button("Show Data"):
            processed_df = df[[label_col, volume_col, intensity_col]]
            st.write(processed_df.head(10))

            st.write("### Download Processed Data")

            csv = processed_df.to_csv(index=False)

            name_file = st.text_input("Name your file here:", "ready_for_easyflow")

            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name=f"{name_file}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    st.set_page_config(layout='wide')
    main()
