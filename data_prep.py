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
        col2.error('Unsupported file format. Please use a CSV file with either comma or semicolon as the delimiter.')
        return None

    if file.type == 'text/csv':
        df = pd.read_csv(file, sep=delimiter)
    elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file)
    return df

def main():
    st.title("Mini App for EasyFlow")
    col1, col2 = st.columns(2)
    col2.subheader(':blue[Upload your data here!]')
    uploaded_file = col2.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])

    col1.info(":red[**Important note**:] If you don't have the correct format for EasyFlow such as the requirement below, you can use this miniapp to make one with your .csv or .xlsx data. ")
    col1.image('labelsize.png')
    if uploaded_file is not None:        

        df = read_file(uploaded_file)
        original_col_names = df.columns.tolist()

        col2.write("### Select Columns")

        label_col = col2.selectbox("Select :red[ Label] Column", original_col_names, key='1')

        col_names_2 = [col for col in original_col_names if col != label_col]
        volume_col = col2.selectbox('Select :red[Volume/ Size] Column', col_names_2, key='2')

        col_names_3 = [col for col in col_names_2 if col != volume_col]
        intensity_col = col2.selectbox('Select :red[Pixel Intensity] Column', col_names_3, key='3')

        if col2.button("Show Data"):
            processed_df = df[[label_col, volume_col, intensity_col]]
            col2.write(processed_df.head(3))

            col1.write("### Download Processed Data")

            csv = processed_df.to_csv(index=False)

            name_file = col1.text_input("Name your file here:", "ready_for_easyflow")

            col1.download_button(
                label="Download ready file for EasyFlow!",
                data=csv,
                file_name=f"{name_file}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    st.set_page_config(layout='wide', page_title='Data preparation', page_icon='🌐')
    main()
