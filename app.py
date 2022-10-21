import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(
    page_title="REPETER",
    page_icon="🎈",
    layout="wide"
)

st.session_state.ptags = ['P-HBReconstruction', "P-PE/MCap/JAngle", "P-Kinematics", "P-InvKinem"]
st.session_state.mtags = ['M-SingleCam/Img', 'M-MultiCam/Img', 'M-Video','M-Marker', "M-Kinect" ]
st.session_state.ftags = ['F-Sports', 'F-Automotive', 'F-Medical', "F-Dance", "F-Workplace"]
st.session_state.btags = ['B-Head', 'B-Core', 'B-Arm', 'B-LBody', "B-UBody", "something"]
st.session_state.otags= ["O-Comp", "O-Review"]
st.session_state.rtags= ['R-High','R-Medium', 'R-Low']
st.session_state.tags = [ st.session_state.rtags, st.session_state.ptags, st.session_state.mtags,  st.session_state.ftags, st.session_state.btags, st.session_state.otags]
max_cols = len(st.session_state.tags )

keywords = ["reconstruction", "angle", "kinemat", "pose", "estimation", "motion", "capture", "camera", "video", "image", "marker", "markerless", "kinect", "depth", "2d", "3d"]


if "record_index" not in st.session_state:
    st.session_state.record_index = 0

if "processed" not in st.session_state:
    st.session_state.processed = {}

if "uid_tag_map" not in st.session_state:
    st.session_state.uid_tag_map = {}

if "tag_placeholders" not in st.session_state:
    st.session_state.tag_placeholders = {}

pickle_filename = "uid_tag.pickle"
def load_excelsheet(path):
    df = pd.read_excel(path)
    df= df.reset_index().rename(columns={"index":"uid"})
    st.session_state.df_list = df.to_dict(orient="records")
    st.session_state.ann_list = []

def load_uid_tag():
    if os.path.exists(pickle_filename):
        with open(pickle_filename, 'rb') as handle:
            st.session_state.uid_tag_map = pickle.load(handle)

def create_tags(uid):
    cols = st.columns(max_cols)
    atags_for_uid = st.session_state.uid_tag_map.get(uid, [])

    for i in range(max_cols):
        with cols[i]:
            for tag in st.session_state.tags[i]:
                placeholder = st.empty()
                if tag in atags_for_uid:
                    status = placeholder.checkbox(tag, value=True)
                else:
                    status = placeholder.checkbox(tag)
                st.session_state.tag_placeholders[tag] =  [placeholder, status]
                
def reset_annotated_tags(uid):
    marked_tags_for_uid = st.session_state.uid_tag_map.get(st.session_state.record_index, [])
    for tags in st.session_state.tags :
        for tag in tags:
            st.session_state.tag_placeholders[tag][0].empty()
            if tag in marked_tags_for_uid:
                st.session_state.tag_placeholders[tag][0].checkbox(tag, key=tag, value=True)
                st.session_state.tag_placeholders[tag][1] = True
            else:
                st.session_state.tag_placeholders[tag][0].checkbox(tag, key=tag)
                st.session_state.tag_placeholders[tag][1] = False
                    
def get_marked_tags_from_sess():
    return  [ key for key in st.session_state.tag_placeholders.keys() if st.session_state.tag_placeholders[key][1]]

def save_uid_tag():
    with open(pickle_filename, 'wb') as handle:
            pickle.dump(st.session_state.uid_tag_map, handle, protocol=pickle.HIGHEST_PROTOCOL) 

def highlight_text(text):
    words = text.split(" ")
    new_words = []
    for word in words:
        if word.lower() in keywords:
            new_words.append("**"+word+"**")
        else:
            new_words.append(word)
    return " ".join(new_words)



#main
st.title("REPETER: RElevant PapEr TaggER")
top_cols = st.columns(2)

with top_cols[0]:
    path_to_excelsheet = st.text_input(
            "Excel Sheet Path",
            "C:\\Users\\VEXU9T\\OneDrive - Scania CV\\02_PhD\\01_Courses\\2022-Autumn\\LiteratureReview\\Output\\scopus_wos_combined.xlsx" )

with top_cols[1]:
    if st.button("Save"):
        save_uid_tag()


if path_to_excelsheet:
    load_excelsheet(path_to_excelsheet)
    load_uid_tag()

create_tags(st.session_state.record_index)

# Every form must have a submit button.
butt_cols = st.columns(12)
with butt_cols[0]:
    if st.button("Submit"):
        marked_tags_from_sess = get_marked_tags_from_sess()
        st.session_state.uid_tag_map[st.session_state.record_index] = marked_tags_from_sess
        st.session_state.record_index += 1
        reset_annotated_tags(st.session_state.record_index)
        save_uid_tag()
        #st.markdown(st.session_state.uid_tag_map)
        #st.markdown(marked_tags_from_sess)


with butt_cols[1]:
    prev = st.button("Prev")
    if prev:
        st.session_state.record_index -= 1
        marked_tags_for_uid = st.session_state.uid_tag_map.get(st.session_state.record_index, [])
        reset_annotated_tags(st.session_state.record_index)
        #st.markdown(st.session_state.uid_tag_map)

with butt_cols[2]:
    prev = st.button("Next")
    if prev:
        print(st.session_state.record_index)
        st.session_state.record_index += 1
        marked_tags_for_uid = st.session_state.uid_tag_map.get(st.session_state.record_index, [])
        reset_annotated_tags(st.session_state.record_index)
        #st.markdown(st.session_state.uid_tag_map)
        print(st.session_state.record_index)


total_annotated_records = len(st.session_state.uid_tag_map)
st.markdown(str(st.session_state.record_index+1)+"/"+str(len(st.session_state.df_list)), total_annotated_records)
st.markdown("**"+st.session_state.df_list[st.session_state.record_index]["Title"]+"**")
st.markdown(highlight_text(st.session_state.df_list[st.session_state.record_index]["Abstract"]))
st.markdown(", ".join([st.session_state.df_list[st.session_state.record_index]["Document Type"], str(st.session_state.df_list[st.session_state.record_index]["Year"]) ]) )

